#!/usr/bin python
# coding:utf-8
# Created by yubiao.luo at 2021/7/13

INFO_DB = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'test',
    'pwd': 'test@pwd',
    'schema': 'dbName',
    'charset': 'utf8',
    'encoding': 'utf-8'
}

DB_CONFIG = {
    'url_fmt': 'mysql+pymysql://{user}:{pwd}@{host}:{port}/{schema}?charset={charset}',
    'pool_recycle': 3600,
    'pool_size': 10
}
