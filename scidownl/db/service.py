# -*- coding: utf-8 -*-
"""Services to manipulate entities"""
from typing import List, Union

from sqlalchemy.orm import sessionmaker

from ..log import get_logger
from .entities import get_engine, ScihubUrl
from ..db.entities import create_tables

logger = get_logger()


class ScihubUrlService:
    def __init__(self, test: bool = False):
        create_tables()
        self.engine = get_engine(test=test)
        self.session_class = sessionmaker(bind=self.engine)

    def add_urls(self, urls: Union[List[ScihubUrl]]) -> None:
        if urls is None or len(urls) == 0:
            return
        session = self.session_class()
        for url in urls:
            try:
                session.add(url)
                session.commit()
            except Exception as e:
                session.rollback()
        session.close()

    def increment_success_times(self, url: str) -> None:
        if url is None or not isinstance(url, str):
            return
        session = self.session_class()
        try:
            session.query(ScihubUrl).filter_by(url=url).update({
                ScihubUrl.success_times: ScihubUrl.success_times + 1
            })
            session.commit()
        except Exception as e:
            logger.warning(f"Cannot increment success times: {url}, reason: {e}")
            session.rollback()
        session.close()

    def increment_failed_times(self, url: str) -> None:
        if url is None or not isinstance(url, str):
            return
        session = self.session_class()
        try:
            session.query(ScihubUrl).filter_by(url=url).update({
                ScihubUrl.failed_times: ScihubUrl.failed_times + 1
            })
            session.commit()
        except Exception as e:
            logger.warning(f"Cannot increment failed times: {url}, reason: {e}")
            session.rollback()
        session.close()

    def get_all_urls(self) -> List[ScihubUrl]:
        session = self.session_class()
        all_urls = session.query(ScihubUrl).all()
        session.close()
        return all_urls
