import shutil
import unittest

from scidownl.core.task import ScihubTask
from scidownl.log import get_logger
from scidownl.config import get_config

logger = get_logger()
configs = get_config()


class TestTask(unittest.TestCase):

    def test_run_tasks(self):
        tmp_paper_dir = './.tmp_paper/'
        cases = [
            ("10.1016/bs.apcsb.2019.08.001", 'doi', tmp_paper_dir),  # ./<title>.pdf
            ("10.3343/alm.2013.33.1.8", 'doi', tmp_paper_dir),
            ("31256946", 'pmid', tmp_paper_dir),
            ("18691502", 'pmid', tmp_paper_dir),
            ("33253586", 'pmid', tmp_paper_dir),
            ('10.1093/oxfordjournals.jmicro.a023417', 'doi', tmp_paper_dir),
            ('10.1002/chin.197335038', 'doi', tmp_paper_dir)
        ]
        for case in cases:
            task = ScihubTask(
                source_keyword=case[0],
                source_type=case[1],
                out=case[2]
            )
            try:
                task.run()
            except Exception as e:
                logger.error(f"final status: {task.context['status']}, error: {task.context['error']}")
        shutil.rmtree(tmp_paper_dir)

    def test_run_one_task(self):

        tmp_paper_dir = './.tmp_paper/'
        ScihubTask(
            source_keyword="10.1016/bs.apcsb.2019.08.001",
            source_type="doi",
            out=tmp_paper_dir
        ).run()
        shutil.rmtree(tmp_paper_dir)


if __name__ == '__main__':
    unittest.main()
