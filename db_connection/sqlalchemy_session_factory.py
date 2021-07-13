#!/usr/bin python
# coding:utf-8
# Created by yubiao.luo at 2021/7/13
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class SessionFactory:
    """SessionFactory is a wrapper around the functions that SQLAlchemy
    provides. The intention here is to let the user work at the session level
    instead of engines and connections.
    """

    def __init__(self, *args, **kwargs):
        self._engine = create_engine(*args, **kwargs)

        self._factory = sessionmaker()
        self._factory.configure(bind=self._engine)

    def make_session(self):
        return self._factory()

    @property
    def engine(self):
        return self._engine


def make_session_factory(*args, **kwargs):
    return SessionFactory(*args, **kwargs)
