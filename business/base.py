#!/usr/bin python
# coding:utf-8
# Created by yubiao.luo at 2019/8/28
import datetime
from sqlalchemy import and_, func
from sqlalchemy.sql.expression import asc, desc
from utils import constants


class AccessBase(object):
    """
    数据库访问
    """
    DATE_FORMAT = '%Y-%m-%d'
    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    DEFAULT_START = 0
    DEFAULT_COUNT = 100

    def __init__(self, session, logger):
        self.session = session
        self.logger = logger

    @classmethod
    def serialize(cls, v):
        if isinstance(v, datetime.datetime):
            v = v.strftime(cls.DATETIME_FORMAT)
        return v

    @staticmethod
    def build_query_condition(query, query_map):
        """
        build a query condition for filter
        :param query:
        :param query_map:
        :return:
        """
        if query is None:
            return and_()

        _condition = []
        for key, value in query.items():
            if value is not None and query_map.get(key) is not None:
                _sub_condition = query_map.get(key)
                if callable(_sub_condition):
                    _condition.append(_sub_condition(value))
                else:
                    continue
        return and_(*_condition)

    @staticmethod
    def build_sort_statement(sortkeys: (list, tuple), sort_map: dict):
        """
        build a sort statement for order by
        :param sort_map:
        :param sortkeys:
        :return:
        """
        _sort_stat = []
        if sortkeys and isinstance(sortkeys, (list, tuple)):
            for item in sortkeys:
                key = item.get('key')
                ascending = item.get('ascending', 0) in constants.TRUE_VALUES
                nullas = item.get('nullas')
                nullascending = item.get('nullascending')
                sort_method = asc if ascending else desc
                if key is not None and key in sort_map:
                    field = sort_map.get(key)
                    if nullas is not None:
                        field = func.ifnull(field, nullas)
                    if nullascending is not None:
                        _nullascending = nullascending in constants.TRUE_VALUES
                        _sort_method = asc if _nullascending else desc
                        _sort_stat.append(_sort_method(func.isnull(field)))
                    _sort_stat.append(sort_method(field))
        return _sort_stat
