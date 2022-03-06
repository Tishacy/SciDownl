import unittest


from scidownl.db.entities import create_tables, ScihubUrl
from scidownl.db.service import ScihubUrlService


class TestDBServices(unittest.TestCase):

    def setUp(self) -> None:
        create_tables(test=True)
        self.service = ScihubUrlService(test=True)

    def test_scihub_url_service_add_urls(self):
        urls = [
            ScihubUrl(url="http://sci-hub.se"),
            ScihubUrl(url="https://sci-hub.sd"),
        ]
        self.service.add_urls(urls)

    def test_scihub_url_service_incr_success_times(self):
        self.service.increment_success_times("http://sci-hub.se")

    def test_scihub_url_service_incr_failed_times(self):
        self.service.increment_failed_times("http://sci-hub.se")

    def test_scihub_url_service_get_all_urls(self):
        all_urls = self.service.get_all_urls()


if __name__ == '__main__':
    unittest.main()
