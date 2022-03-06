import re
import unittest

from scidownl.config import get_config
from scidownl.log import get_logger

logger = get_logger()


class TestConfig(unittest.TestCase):

    def test_config_ops(self):
        config = get_config()
        logger.debug(config.sections())
        self.assertGreaterEqual(len(config.sections()), 0)


if __name__ == '__main__':
    unittest.main()
