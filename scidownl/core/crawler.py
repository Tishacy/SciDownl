# -*- coding: utf-8 -*-
"""Crawler implementations."""
import requests

from .content import HtmlContent
from .base import BaseCrawler, BaseSource, BaseTaskStep, BaseTask, BaseContent
from ..log import get_logger
from ..exception import CrawlException
from ..db.service import ScihubUrlService

logger = get_logger()


class ScihubCrawler(BaseCrawler, BaseTaskStep):
    """Crawler of a scihub source."""

    OK_STATUS_CODES = [200]

    def __init__(self, source: BaseSource, scihub_url: str, task: BaseTask = None):
        BaseCrawler.__init__(self, source)
        BaseTaskStep.__init__(self, task)
        self.scihub_url = scihub_url
        self.sess = requests.Session()
        self.service = ScihubUrlService()

        if self.task is not None:
            self.task.context['source'] = source
            self.task.context['referer'] = scihub_url
            self.task.context['status'] = 'crawling'

    def crawl(self) -> HtmlContent:
        try:
            request_params = {
                'request': self.source[self.source.type]
            }
            res = self.sess.post(self.scihub_url, data=request_params)

            logger.info(f"<- Request: scihub_url={self.scihub_url}, source={self.source}")
            logger.info(f"-> Response: status_code={res.status_code}, content_length={len(res.content.decode())}")

            if res.status_code not in ScihubCrawler.OK_STATUS_CODES:
                raise RuntimeError(f"Error occurs when crawling source: {self.source}")

            content = HtmlContent(res.content.decode())

            if self.task is not None:
                self.task.context['content'] = content
                self.task.context['status'] = 'crawled'
            return content
        except Exception as e:
            if self.task is not None:
                self.task.context['status'] = 'crawling_failed'
                self.task.context['error'] = e
                self.service.increment_failed_times(self.scihub_url)
            raise CrawlException(f"Error occurs when crawling: {e}")

    def __del__(self):
        self.sess.close()
