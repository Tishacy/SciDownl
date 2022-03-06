# -*- encoding: utf-8 -*-
"""Information implementations."""

from .base import BaseInformation


class UrlInformation(BaseInformation):
    """Information of url"""
    PROTOCOL_PREFIXES = ["https://", "http://"]
    DEFAULT_PROTOCOL_PREFIX = PROTOCOL_PREFIXES[0]

    def __init__(self, url: str):
        BaseInformation.__init__(self)
        self.url = url
        self['url'] = self.url

    def get_url(self):
        return self.url


class TitleInformation(BaseInformation):
    """Information of title"""
    def __init__(self, title: str):
        BaseInformation.__init__(self)
        self.title = title
        self['title'] = self.title

    def get_title(self):
        return self.title


class PdfUrlTitleInformation(UrlInformation, TitleInformation):
    """Information with pdf url and title."""

    def __init__(self, url: str, title: str):
        UrlInformation.__init__(self, url)
        TitleInformation.__init__(self, title)
