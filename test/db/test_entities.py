import unittest

from scidownl.db.entities import get_engine, create_tables, ScihubUrl
from scidownl.log import get_logger

logger = get_logger()


class TestEntities(unittest.TestCase):

    def test_create_tables(self):
        create_tables(test=True)

    def test_orm(self):
        from sqlalchemy.orm import sessionmaker

        create_tables(test=True)
        engine = get_engine(echo=False, test=True)
        Session = sessionmaker(bind=engine)

        # Add
        items = [
            ScihubUrl(url="http://sci-hub.se"),
            ScihubUrl(url="https://sci-hub.sd"),
        ]
        session = Session()
        for item in items:
            try:
                session.add(item)
                session.commit()
            except Exception as e:
                session.rollback()
        session.close()

        # Query
        exist_url = ScihubUrl(url="http://sci-hub.se")
        non_exist_url = ScihubUrl(url="http://sci-hub.non-exist")
        session = Session()
        exist_rec = session.query(ScihubUrl).filter_by(url=exist_url.url).first()
        self.assertEqual(exist_url.url, exist_rec.url)
        non_exist_rec = session.query(ScihubUrl).filter_by(url=non_exist_url.url).first()
        self.assertIsNone(non_exist_rec)
        session.close()

        # Modify
        modify_url = ScihubUrl(url="http://sci-hub.se")
        session = Session()
        session.query(ScihubUrl).filter_by(url=modify_url.url).update({
            ScihubUrl.success_times: ScihubUrl.success_times + 1
        })
        session.commit()
        modified_success_times = session.query(ScihubUrl).filter_by(url=modify_url.url).first().success_times
        self.assertGreaterEqual(modified_success_times, 1)
        session.close()

        # Delete
        session = Session()
        urls = session.query(ScihubUrl).all()
        for url in urls:
            session.delete(url)
        session.commit()
        self.assertEqual(0, len(session.query(ScihubUrl).all()))
        session.close()


if __name__ == '__main__':
    unittest.main()
