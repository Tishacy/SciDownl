# -*- coding: utf-8 -*-
"""Exceptions used in core."""


class EmptyDoiException(Exception):
    """Raised if empty Doi is given."""


class EmptyPmidException(Exception):
    """Raised if empty PMID is given."""


class CrawlException(Exception):
    """Raised if error occurs when crawling."""


class PdfTagNotFoundException(Exception):
    """Raised if no pdf tag is found."""


class PdfUrlNotFoundException(Exception):
    """Raised if no pdf url is found."""


class ExtractException(Exception):
    """Raised if error occurs when extracting."""


class DownloadException(Exception):
    """Raised if error occurs when downloading."""

