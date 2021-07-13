#!/usr/bin python
# coding:utf-8
# Created by yubiao.luo at 2021/7/13
from config.config import INFO_DB, DB_CONFIG
from db_connection.sqlalchemy_session_factory import make_session_factory

info_factory = make_session_factory(
    DB_CONFIG['url_fmt'].format(**INFO_DB),
    pool_recycle=DB_CONFIG['pool_recycle'],
    pool_pre_ping=True,
    pool_size=DB_CONFIG['pool_size'],
    echo=True
)
