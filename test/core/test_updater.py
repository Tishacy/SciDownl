import unittest

from scidownl.core.updater import CrawlingScihubDomainUpdater, SearchScihubDomainUpdater


class TestDomainUpdater(unittest.TestCase):

    def test_crawling_scihub_domain_updater_exclude_method(self):
        domain_urls = [
            "http://sci-hub.se",
            "https://sci-hub.fun",
            "http://sci-hub.fun",
        ]
        exclude_url_pattern = ".fun"
        updater = CrawlingScihubDomainUpdater()
        available_urls = updater._exclude_domain_urls(domain_urls, exclude_url_pattern)
        self.assertEqual(1, len(available_urls))
        self.assertEqual("http://sci-hub.se", available_urls[0])

    def test_crawling_scihub_domain_updater_update_domains(self):
        updater = CrawlingScihubDomainUpdater()
        domain_urls = updater.update_domains()
        self.assertTrue(len(domain_urls) != 0)

        updater = CrawlingScihubDomainUpdater("https://sci-hub.top/")
        domain_urls = updater.update_domains()
        self.assertTrue(len(domain_urls) != 0)

    def test_search_scihub_domain_updater_update_domains(self):
        updater = SearchScihubDomainUpdater()
        domain_urls = updater.update_domains()
        self.assertTrue(len(domain_urls) != 0)


if __name__ == '__main__':
    unittest.main()
