# -*- coding: utf-8 -*-
"""Entities of tables"""
import os


from ..config import get_config

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
    engine = open(db_path, 'r')
    return engine
