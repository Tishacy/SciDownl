import unittest

from scidownl.core.source import PmidSource, DoiSource
from scidownl.core.crawler import ScihubCrawler


class TestCrawler(unittest.TestCase):

    def test_scihub_crawl(self):
        scihub_url = "https://sci-hub.st"

        # Test crawling with PMID.
        pmid_source = PmidSource(31928726)
        ScihubCrawler(pmid_source, scihub_url).crawl()

        # Test crawling with DOI.
        doi_source = DoiSource('10.1016/bs.apcsb.2019.08.001')
        ScihubCrawler(doi_source, scihub_url).crawl()

        # Test crawling a non-exist PMID.
        pmid_source = PmidSource(0000)
        ScihubCrawler(pmid_source, scihub_url).crawl()


if __name__ == '__main__':
    unittest.main()
