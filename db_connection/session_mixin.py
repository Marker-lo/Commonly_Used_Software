#!/usr/bin python
# coding:utf-8
# Created by lex.li at 2020/10/30
from contextlib import contextmanager


class MissingFactoryError(Exception):
    pass


class SessionMixin(object):
    """
    session mixin
    """
    factory = None
    application = None

    @contextmanager
    def make_session(self, commit=True):
        session = None

        try:
            session = self._make_session()
            yield session
        except Exception:
            if session:
                session.rollback()
            raise
        else:
            if commit:
                session.commit()

        finally:
            if session:
                session.close()

    def make_connection(self):
        return self.get_engine().connect()

    def _make_session(self):
        factory = self.get_factory()

        if not factory:
            raise MissingFactoryError()

        return factory.make_session()

    def get_factory(self):
        if self.factory:
            return self.factory
        self.factory = self.application.settings.get('session_factory')
        return self.factory

    def get_engine(self):
        factory = self.get_factory()
        return factory.engine


def get_db_session(db_factory):
    db_session = SessionMixin()
    db_session.factory = db_factory
    return db_session
