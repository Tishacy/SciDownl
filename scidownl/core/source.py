# -*- encoding: utf-8 -*-
"""Source implementations."""
from typing import Union

from .base import BaseSource
from ..exception import EmptyDoiException, EmptyPmidException, EmptyTitleException


class DoiSource(BaseSource):
    """A DOI source dict."""

    DOI_PROTOCOLS = ["http://", "https://"]

    def __init__(self, doi: str):
        super().__init__()
        self.doi = self._clean_doi(doi)
        self.protocol = self._extract_protocol(doi)
        self.type = 'doi'
        self[self.type] = self.doi
        self['protocol'] = self.protocol

    @staticmethod
    def _clean_doi(doi: str) -> str:
        if doi is None:
            raise EmptyDoiException("Empty doi is given")
        if not isinstance(doi, str):
            raise TypeError(f"Doi must be a string, got a {type(doi)} instead")
        if len(doi) == 0:
            raise EmptyDoiException("Empty doi is given")

        for proto in DoiSource.DOI_PROTOCOLS:
            doi = doi.replace(proto, "")
        return doi

    @staticmethod
    def _extract_protocol(doi: str) -> str:
        for proto in DoiSource.DOI_PROTOCOLS:
            if proto in doi:
                return proto.split(":")[0]
        return "https"

    def get_doi(self):
        return self.doi

    def get_protocol(self):
        return self.protocol

    def __repr__(self):
        return f"DoiSource[type={self.type}, id={self.doi}]"


class PmidSource(BaseSource):
    """A PMID source dict."""
    def __init__(self, pmid: Union[str, int]):
        super().__init__()
        self.pmid = self._clean_pmid(pmid)
        self.type = 'pmid'
        self[self.type] = self.pmid

    @staticmethod
    def _clean_pmid(pmid: str) -> str:
        if pmid is None:
            raise EmptyPmidException("Empty pmid is given")
        if not isinstance(pmid, str) and not isinstance(pmid, int) \
                or isinstance(pmid, bool):
            raise TypeError(f"PMID must be either a string or an integer, got a {type(pmid)} instead")

        pmid_str = str(pmid)
        if len(pmid_str) == 0:
            raise EmptyPmidException("Empty pmid is given")
        return pmid_str

    def get_pmid(self):
        return self.pmid

    def __repr__(self):
        return f"PmidSource[type={self.type}, id={self.pmid}]"


class TitleSource(BaseSource):
    """A title source dict."""
    def __init__(self, title: str):
        super().__init__()
        self.title = self._clean_title(title)
        self.type = 'title'
        self[self.type] = self.title

    @staticmethod
    def _clean_title(title: str) -> str:
        if title is None:
            raise EmptyTitleException("Empty title is given")
        if not isinstance(title, str):
            raise TypeError(f"Title must be either a string or an integer, got a {type(title)} instead")

        title_str = str(title).strip()
        if len(title_str) == 0:
            raise EmptyTitleException("Empty title is given")
        return title_str

    def get_title(self):
        return self.title

    def __repr__(self):
        return f"TitleSource[type={self.type}, id={self.title}]"


source_classes = {
    'doi': DoiSource,
    'DOI': DoiSource,
    'pmid': PmidSource,
    'PMID': PmidSource,
    'title': TitleSource,
    'TITLE': TitleSource
}
