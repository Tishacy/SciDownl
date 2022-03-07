# -*- coding: utf-8 -*-
"""High level APIs for human"""

from ..core.task import ScihubTask


def scihub_download(
        keyword: str,
        paper_type: str = 'doi',
        scihub_url: str = None,
        out: str = None
    ) -> None:
    """Download a paper from SciHub.

    :param keyword: a DOI or a PMID.
    :param paper_type: (optional) one of ['doi', 'pmid']
    :param scihub_url: (optional) a specific SciHub url used to download the paper.
        If None, automatically choose one from local saved domains.
        It's recommended to leave it None.
    :param out: Output directory or file path, which could be an
        absolute path or a relative path.
        Output directory examples:
         /absolute/path/to/download/, ./relative/path/to/download/
        Output file examples:
         /absolute/dir/paper.pdf, ../relative/dir/paper.pdf
        If None, paper will be downloaded to the current directory with the file
        name of the paper's title.
    """
    return ScihubTask(
        source_keyword=keyword,
        source_type=paper_type,
        scihub_url=scihub_url,
        out=out
    ).run()

