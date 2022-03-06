import unittest

from scidownl.core.source import DoiSource, PmidSource
from scidownl.exception import EmptyDoiException, EmptyPmidException


class TestSource(unittest.TestCase):

    def test_create_doi_source(self):
        # Empty case: doi is None.
        with self.assertRaises(EmptyDoiException):
            DoiSource(None)

        # Empty case: doi is an empty string.
        with self.assertRaises(EmptyDoiException):
            DoiSource("")

        # Invalid type case: doi is not a string.
        with self.assertRaises(TypeError):
            DoiSource(2345783)

        # Correct case.
        cases = {
            'http_doi': 'http://doi.org/10.1145/1327452.1327492',
            'https_doi': 'https://doi.org/10.1145/1327452.1327492',
            'raw_doi': 'doi.org/10.1145/1327452.1327492'
        }
        doi_source = DoiSource(cases.get('http_doi'))
        self.assertEqual("doi.org/10.1145/1327452.1327492", doi_source.get_doi())
        self.assertEqual("http", doi_source.get_protocol())

        doi_source = DoiSource(cases.get('https_doi'))
        self.assertEqual("doi.org/10.1145/1327452.1327492", doi_source.get_doi())
        self.assertEqual("https", doi_source.get_protocol())

        doi_source = DoiSource(cases.get('raw_doi'))
        self.assertEqual("doi.org/10.1145/1327452.1327492", doi_source.get_doi())
        self.assertEqual("https", doi_source.get_protocol())

    def test_create_pmid_source(self):
        # Empty case: PMID is None.
        with self.assertRaises(EmptyPmidException):
            PmidSource(None)

        # Empty case: doi is an empty string.
        with self.assertRaises(EmptyPmidException):
            PmidSource("")

        # Invalid type case: doi is not a string.
        with self.assertRaises(TypeError):
            PmidSource(True)
            PmidSource([])
            PmidSource({})

        # Correct case.
        cases = {
            'PMID_str': '31928726',
            'PMID_number': 31928726,
        }
        pmid_source = PmidSource(cases.get('PMID_str'))
        self.assertEqual(cases.get('PMID_str'), pmid_source.get_pmid())

        pmid_source = PmidSource(cases.get('PMID_number'))
        self.assertEqual(str(cases.get('PMID_number')), pmid_source.get_pmid())


if __name__ == '__main__':
    unittest.main()
