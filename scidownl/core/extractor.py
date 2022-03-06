# -*- encoding: utf-8 -*-
"""Extractor implementations."""
import re

from bs4 import BeautifulSoup

from .base import BaseExtractor, BaseInformation, BaseTask, BaseTaskStep
from .content import HtmlContent
from .information import PdfUrlTitleInformation, UrlInformation
from .chooser import scihub_url_choosers, AvailabilityFirstScihubUrlChooser
from ..exception import PdfTagNotFoundException, PdfUrlNotFoundException, ExtractException
from ..db.service import ScihubUrlService
from ..log import get_logger
from ..config import get_config

logger = get_logger()
configs = get_config()


def get_default_referer():
    scihub_url_chooser_type = configs['scihub.task']['scihub_url_chooser_type']
    chooser_cls = scihub_url_choosers.get(scihub_url_chooser_type, AvailabilityFirstScihubUrlChooser)
    chooser = chooser_cls()
    scihub_url = "https://sci-hub.se" if len(chooser) == 0 else chooser.next().url
    return scihub_url


class HtmlPdfExtractor(BaseExtractor, BaseTaskStep):
    """Pdf extractor to extract a pdf information from the html content.
    """

    # choose the first scihub url with the chooser defined in config.
    DEFAULT_REFERER = get_default_referer()

    def __init__(self, content: HtmlContent, task: BaseTask = None):
        BaseExtractor.__init__(self, content)
        BaseTaskStep.__init__(self, task)
        self.task = task
        self.service = ScihubUrlService()

        if self.task is not None:
            self.task.context['status'] = 'extracting'

        # using pdf_tag_selector, pdf_tag_attr in configs.
        self.pdf_tag_selector = configs['scihub.task.extractor']['pdf_tag_selector']
        self.pdf_tag_attr = configs['scihub.task.extractor']['pdf_tag_attr']
        self._parser = 'html.parser'

    def extract(self) -> PdfUrlTitleInformation:
        try:
            url = self._extract_url()
            title = self._extract_title()

            info = PdfUrlTitleInformation(url, title)
            logger.info(f"* Extracted information: {info}")
            if self.task is not None:
                self.task.context['info'] = info
        except Exception as e:
            if self.task is not None:
                self.task.context['status'] = 'extracting_failed'
                self.task.context['error'] = e
                scihub_url = self.task.context.get('referer', None)
                self.service.increment_failed_times(scihub_url)
            raise ExtractException(f"Error occurs when extracting: {e}")

        return info

    def _extract_url(self) -> str:
        raw_url = self._extract_raw_url()

        for prefix in UrlInformation.PROTOCOL_PREFIXES:
            if prefix in raw_url:
                return raw_url

        url = raw_url.split("#")[0]
        if url.startswith("//"):
            url = UrlInformation.DEFAULT_PROTOCOL_PREFIX + url[2:]
        elif url.startswith("/"):
            if self.task is None:
                referer = HtmlPdfExtractor.DEFAULT_REFERER
            else:
                referer = self.task.context.get('referer', HtmlPdfExtractor.DEFAULT_REFERER)
            url = referer + url
        return url

    def _extract_raw_url(self) -> str:
        """Extract pdf url from html content."""
        soup = BeautifulSoup(self.content.content, self._parser)
        pdf_tag = soup.select_one(self.pdf_tag_selector)
        if pdf_tag is None:
            raise PdfTagNotFoundException(f"No pdf tag was found in the given content "
                                          f"with the selector: {self.pdf_tag_selector}")
        raw_url = pdf_tag.attrs.get(self.pdf_tag_attr)
        if raw_url is None:
            raise PdfUrlNotFoundException(f"No pdf url was found in the pdf tag: {pdf_tag.get_text()} "
                                          f"with the attr {self.pdf_tag_attr}")
        return raw_url

    def _extract_title(self) -> str:
        """Extract title from html content."""
        soup = BeautifulSoup(self.content.content, self._parser)
        soup_title = soup.title
        if soup_title is None or len(soup_title.text) == 0 \
                or '|' not in soup_title.text:
            title = ""
        else:
            title = soup.title.text.split('|')[1]
        return self._clean_title(title)

    @staticmethod
    def _clean_title(title) -> str:
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # / \ : * ? " < > |
        title = re.sub(rstr, " ", title)[:200]
        return title.strip()

