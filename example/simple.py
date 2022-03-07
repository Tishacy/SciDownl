# -*- coding: utf-8 -*-

from scidownl import scihub_download


def download_one_paper():
    """Example of downloading one paper.
    The paper will be downloaded the ./paper/ directory, and
    the filename is one_paper.pdf
    """
    paper = "https://doi.org/10.1145/3375633"
    paper_type = "doi"
    out = "./paper/one_paper.pdf"
    scihub_download(paper, paper_type=paper_type, out=out)


def download_multi_papers():
    """Example of downloading multiple papers.
    All papers will be downloaded to the ./paper/ directory,
    and their filenames are the paper titles.
    """
    source = [
        ("https://doi.org/10.1145/3375633", 'doi', "./paper/"),
        ("31395057", 'pmid', "./paper/"),
        ("24686414", 'pmid', "./paper/"),
    ]
    for paper, paper_type, out in source:
        scihub_download(paper, paper_type=paper_type, out=out)


if __name__ == '__main__':
    download_one_paper()
    download_multi_papers()
