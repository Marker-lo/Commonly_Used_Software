#!/usr/bin python
# coding:utf-8
# Created by yubiao.luo at 2021/7/13
import pandas as pd
from db_connection.session_mixin import SessionMixin
from db_connection.session_factories import info_factory


def main():
    info_db = SessionMixin()
    info_db.factory = info_factory
    with info_db.make_session() as session:
        # sql = 'SELECT col1, col2, col3 FROM table_name WHERE flowId=%(flowId)s;'
        # res = pd.read_sql_query(sql, con=session.bind, params={'flowId': 2056})
        # sql = 'SELECT col1, col2, col3 FROM table_name WHERE flowId IN %(flowIds)s;'
        # res = pd.read_sql_query(sql, con=session.bind, params={'flowIds': [2056, 2057, 2058]})
        sql = 'SELECT col1, col2, col3 FROM table_name WHERE flowId IN %(flowIds)s;'
        res = pd.read_sql_query(sql, con=session.bind, params={'flowIds': [2056, 2057, 2058]}, index_col='flowId')
    return res


if __name__ == '__main__':
    main()
