# -*- coding: utf-8 -*-
"""Services to manipulate entities"""
from typing import List, Union

# from sqlalchemy.orm import sessionmaker

from ..log import get_logger
from .entities import get_engine
# from ..db.entities import create_tables

logger = get_logger()


class ScihubUrlService:
    def __init__(self, test: bool = False):
        self.engine = get_engine(test=test)

    def increment_success_times(self, url: str) -> None:
        print(f"Success to fetch url: {url}")
 

    def increment_failed_times(self, url: str) -> None:
        print(f"Failed to fetch url: {url}")


    def get_all_urls(self) -> List[str]:
        with self.engine as conn:
            all_urls = conn.read().splitlines() 
        return all_urls
