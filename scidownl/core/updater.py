# -*- coding: utf-8 -*-
"""Implementations of DomainUpdater"""
import re
import string
from typing import Iterable, Union, List
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup

from .base import DomainUpdater
from ..log import get_logger
from ..config import get_config
from ..db.entities import ScihubUrl
from ..db.service import ScihubUrlService

logger = get_logger()
configs = get_config()


class CrawlingScihubDomainUpdater(DomainUpdater):
    """Updater of Scihub domains by crawling a domain source."""
    def __init__(self, domain_source_url: str = None):
        super().__init__()
        self.service = ScihubUrlService()

        # use strings defined in configs.
        self.domain_source_url = domain_source_url or configs['scihub.domain.updater.crawl']['scihub_domain_source']
        self._domain_url_pattern = configs['scihub.domain.updater.crawl']['scihub_url_pattern']
        self._exclude_url_pattern = configs['scihub.domain.updater.crawl']['exclude_url_pattern']

    def update_domains(self) -> Union[List, Iterable[ScihubUrl]]:
        html = requests.get(self.domain_source_url).text
        domain_urls = re.findall(self._domain_url_pattern, html)

        # Drop duplicates.
        domain_urls = list(set(domain_urls))
        # Exclude invalid urls.
        available_domain_urls = self._exclude_domain_urls(domain_urls)
        logger.info(f"Found {len(available_domain_urls)} valid SciHub domains in total: {available_domain_urls}")

        # Save to db.
        urls_to_save = [ScihubUrl(url=url) for url in available_domain_urls]
        self.service.add_urls(urls_to_save)
        logger.info(f"Saved {len(urls_to_save)} SciHub domains to local db.")
        return available_domain_urls

    def _exclude_domain_urls(self, domain_urls, exclude_url_pattern: str = None):
        exclude_url_pattern = exclude_url_pattern or self._exclude_url_pattern
        remain_urls = []
        for url in domain_urls:
            if not re.search(exclude_url_pattern, url):
                remain_urls.append(url)
        return remain_urls


class SearchScihubDomainUpdater(DomainUpdater):
    """Updater of Scihub domains by brute force search."""

    OK_STATUS_CODES = [200]

    def __init__(self, title_keyword_pattern: str = None, num_workers: int = None,
                 timeout: int = None):
        super().__init__()
        self.service = ScihubUrlService()

        # read from configs
        self._domain_prefixes = ["http://sci-hub.", "https://sci-hub."]
        self._keyword_pattern = title_keyword_pattern or \
            configs['scihub.domain.updater.search']['scihub_title_keyword_pattern']
        self._num_workers = num_workers or configs['scihub.domain.updater.search'].getint('num_workers')
        self._timeout = timeout or configs['scihub.domain.updater.search'].getint('check_timeout')

    def update_domains(self) -> Union[List, Iterable[str]]:
        search_urls = self._get_search_urls()
        logger.info(f"# Search valid SciHub domains from {len(search_urls)} urls")

        valid_urls = []
        with ThreadPoolExecutor(max_workers=self._num_workers) as executor:
            future_to_url = {
                executor.submit(self._check_valid_url, url, self._timeout): url
                for url in search_urls
            }
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    valid = future.result()
                    if valid:
                        valid_urls.append(url)
                except Exception as exc:
                    logger.error('%r generated an exception: %s' % (url, exc))

        logger.info(f"Found {len(valid_urls)} valid SciHub domains in total: {valid_urls}")
        # Save to db.
        urls_to_save = [ScihubUrl(url=url) for url in valid_urls]
        self.service.add_urls(urls_to_save)
        logger.info(f"Saved {len(urls_to_save)} SciHub domains to local db.")
        return valid_urls

    def _get_search_urls(self):
        letters = string.ascii_lowercase
        search_urls = []
        for first_letter in letters:
            for second_letter in letters:
                for prefix in self._domain_prefixes:
                    search_urls.append(prefix + first_letter + second_letter)
        return search_urls

    def _check_valid_url(self, url: str, timeout: int = 60) -> bool:
        try:
            res = requests.get(url, timeout=timeout)
        except Exception as e:
            # Cannot connect the specified url, skip it.
            return False

        if res.status_code not in SearchScihubDomainUpdater.OK_STATUS_CODES:
            return False

        content = res.content.decode()
        soup = BeautifulSoup(content, 'html.parser')
        if soup.title is not None and re.search(self._keyword_pattern, soup.title.text) is not None:
            logger.info(f"# Found a SciHub domain url: {url}")
            return True
        return False


scihub_domain_updaters = {
    'crawl': CrawlingScihubDomainUpdater,
    'search': SearchScihubDomainUpdater
}
