# -*- encoding: utf-8 -*-
"""Task implementations."""
import os.path

from .base import BaseTask, ScihubUrlChooser
from .source import DoiSource, source_classes
from .crawler import ScihubCrawler
from .extractor import HtmlPdfExtractor
from .downloader import UrlDownloader
from .chooser import AvailabilityFirstScihubUrlChooser, scihub_url_choosers
from .updater import CrawlingScihubDomainUpdater
from ..log import get_logger
from ..config import get_config
from ..db.service import ScihubUrlService

logger = get_logger()
configs = get_config()

scihub_url_chooser_type = configs['scihub.task']['scihub_url_chooser_type']
default_chooser_cls = scihub_url_choosers.get(scihub_url_chooser_type, AvailabilityFirstScihubUrlChooser)


class ScihubTask(BaseTask):

    def __init__(self,
                 source_keyword: str,
                 source_type: str = 'doi',
                 scihub_url: str = None,
                 scihub_url_chooser_cls=default_chooser_cls,
                 out: str = None):
        super().__init__()
        self.source_keyword = source_keyword
        self.scihub_url_chooser_cls = scihub_url_chooser_cls
        self.scihub_url_chooser = self.scihub_url_chooser_cls()
        self.scihub_url = scihub_url
        self.source_class = source_classes.get(source_type, DoiSource)
        self.out = out
        self.context['status'] = 'initialized'
        self.service = ScihubUrlService()
        self.updater = CrawlingScihubDomainUpdater()

    def run(self):
        if self.scihub_url is not None:
            logger.info(f"Choose the scihub url: {self.scihub_url}")
            return self._run(self.scihub_url)

        # Update scihub domains if empty.
        if len(self.scihub_url_chooser) == 0:
            self.updater.update_domains()
            self.scihub_url_chooser = self.scihub_url_chooser_cls()

        for i, scihub_url in enumerate(self.scihub_url_chooser):
            try:
                logger.info(f"Choose scihub url [{i}]: {scihub_url.url}")
                return self._run(scihub_url.url)
            except Exception as e:
                logger.warning(f"Error occurs, task status: {self.context['status']}, error: {self.context['error']}")
                continue
        logger.error(f"Failed to download the paper: {self.source_keyword}. Please try again.")

    def _run(self, scihub_url):
        source = self.source_class(self.source_keyword)
        crawler = ScihubCrawler(source, scihub_url, self)
        content = crawler.crawl()

        extractor = HtmlPdfExtractor(content, self)
        pdf_url_title_info = extractor.extract()

        if self.out is None:
            # Using title as the filename and save to current directory.
            out = pdf_url_title_info['title'] + '.pdf'
        else:
            dirpath, filename = os.path.split(self.out)
            if dirpath != '' and not os.path.exists(dirpath):
                os.makedirs(dirpath)
            if len(filename) == 0:
                filename = pdf_url_title_info['title'] + '.pdf'
            if not filename.endswith("pdf") and not filename.endswith("PDF"):
                filename += '.pdf'
            out = os.path.join(dirpath, filename)

        downloader = UrlDownloader(pdf_url_title_info, self)
        downloader.download(out)
        scihub_url = self.context.get('referer', None)
        self.service.increment_success_times(scihub_url)
