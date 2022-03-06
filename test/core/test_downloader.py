import os
import unittest

from scidownl.core.information import PdfUrlTitleInformation
from scidownl.core.downloader import UrlDownloader
from scidownl.log import get_logger

logger = get_logger()


class TestDownloader(unittest.TestCase):

    def test_download_information(self):
        url = "https://sci-hub.st/downloads/2020-01-20/c1/nademi2019.pdf"
        title = "Protein misfolding in endoplasmic reticulum stress with applications to renal diseases. Advances in Protein Chemistry and Structural Biology, 217–247"
        info = PdfUrlTitleInformation(url, title)

        downloader = UrlDownloader(info)
        out = 'test_paper.pdf'
        downloader.download(out)
        self.assertTrue(os.path.exists(out))
        os.remove(out)
        logger.debug(f"Remove the test paper file: {out}")


if __name__ == '__main__':
    unittest.main()
