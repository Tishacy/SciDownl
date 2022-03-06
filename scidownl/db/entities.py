# -*- coding: utf-8 -*-
"""Entities of tables"""
import os

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from ..config import get_config

Base = declarative_base()
configs = get_config()


def get_engine(echo: bool = False, test: bool = False):
    """Returns the db engine.

    :param echo: if True, the Engine will log all statements.
    :param test: if True, using test db instead.
    :returns :class:`sqlalchemy._engine.Engine` instance.
    """
    par_dirpath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    dbname = 'test-scidownl.db' if test else configs['global_db']['db_name']
    db_path = os.path.join(par_dirpath, dbname)
    engine = create_engine(f'sqlite:///{db_path}?check_same_thread=False', echo=echo)
    return engine


def create_tables(test: bool = False):
    """Create all tables that are not exist.

    :param test: if True, using test db instead.
    """
    engine = get_engine(test=test)
    Base.metadata.create_all(engine, checkfirst=True)


class ScihubUrl(Base):
    __tablename__ = "scihub_url"

    url = Column(String(50), primary_key=True)
    success_times = Column(Integer, default=0)
    failed_times = Column(Integer, default=0)

    def __repr__(self):
        return f"<ScihubUrl(url={self.url}, " \
               f"success_times={self.success_times}, " \
               f"failed_times={self.failed_times})>"
