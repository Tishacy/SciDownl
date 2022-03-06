import unittest

from scidownl.core.chooser import SimpleScihubUrlChooser, RandomScihubUrlChooser, AvailabilityFirstScihubUrlChooser


class TestChooser(unittest.TestCase):

    def test_simple_chooser(self):
        chooser = SimpleScihubUrlChooser()
        self.assertGreaterEqual(len(chooser), 0)

    def test_random_chooser(self):
        chooser = RandomScihubUrlChooser()
        self.assertGreaterEqual(len(chooser), 0)

    def test_availability_first_chooser(self):
        chooser = AvailabilityFirstScihubUrlChooser()
        self.assertGreaterEqual(len(chooser), 0)


if __name__ == '__main__':
    unittest.main()
