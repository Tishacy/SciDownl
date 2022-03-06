# -*- encoding: utf-8 -*-
"""Source implementations."""
from typing import Union

from .base import BaseSource
from ..exception import EmptyDoiException, EmptyPmidException


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
            raise TypeError(f"Title must be either a string or an integer, got a {type(pmid)} instead")

        pmid_str = str(pmid)
        if len(pmid_str) == 0:
            raise EmptyPmidException("Empty pmid is given")
        return pmid_str

    def get_pmid(self):
        return self.pmid

    def __repr__(self):
        return f"DoiSource[type={self.type}, id={self.pmid}]"


source_classes = {
    'doi': DoiSource,
    'DOI': DoiSource,
    'pmid': PmidSource,
    'PMID': PmidSource
}
