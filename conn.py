#!/usr/bin/env python
# encoding=utf-8

import MySQLdb
import MySQLdb.cursors


config = {
    'host':'localhost',
    'port':3306,
    'user':'root',
    'passwd':'1234',
    'db':'dota2',
    'charset':"utf8", #不加这个,在mysql中会以乱码显示中文
    'cursorclass':MySQLdb.cursors.DictCursor,

}

def connDB():
    db = MySQLdb.connect(**config)
    return db
