import unittest

from scidownl.core.content import HtmlContent
from scidownl.core.extractor import HtmlPdfExtractor


class TestExtractor(unittest.TestCase):

    def test_html_pdf_extractor(self):
        html_content = HtmlContent("""
        <head>
            <title>Sci-Hub | Protein misfolding in endoplasmic reticulum stress with applications to renal diseases. Advances in Protein Chemistry and Structural Biology, 217–247 | 10.1016/bs.apcsb.2019.08.001</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width">
            <script type="text/javascript" async="" src="https://mc.yandex.ru/metrika/watch.js"></script><script src="//sci-hub.st/misc/js/jquery-3.6.0.min.js"></script>
            <script src="//sci-hub.st/misc/js/snowflakes.min.js"></script>
        </head>
        <div id="article">
            <embed type="application/pdf" src="//sci-hub.st/downloads/2020-01-20/c1/nademi2019.pdf#navpanes=0&amp;view=FitH" id="pdf">
        </div>
        """)
        extractor = HtmlPdfExtractor(html_content)
        pdf_url_title_info = extractor.extract()
        self.assertEqual("https://sci-hub.st/downloads/2020-01-20/c1/nademi2019.pdf", pdf_url_title_info.get_url())
        self.assertEqual("Protein misfolding in endoplasmic reticulum stress with applications to renal diseases. "
                         "Advances in Protein Chemistry and Structural Biology, 217–247",
                         pdf_url_title_info.get_title())


if __name__ == '__main__':
    unittest.main()
