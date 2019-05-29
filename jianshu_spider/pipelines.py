# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from twisted.enterprise import adbapi
from pymysql import cursors


class JianshuSpiderPipeline(object):
    def __init__(self):
        dbparams = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': '123456',
            'database': 'jianshu',
            'charset': 'utf8'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursot = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        self.cursot.execute(self.sql, (
        item['title'], item['content'], item['author'], item['avatar'], item['pub_time'], item['origin_url'],
        item['article_id']))
        self.conn.commit()

        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into article(id,title,content,author,avatar,pub_time,origin_url,article_id) values (null,%s,%s,%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql


#数据放在pipelines, 使用adbapi提供的连接池ConnectionPool把插入数据变成异步的
class JianshuTwistedPipeline(object):
    def __init__(self):
        dbparams = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': '123456',
            'database': 'jianshu',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor  # 指定游标
        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into article(id,title,content,author,avatar,pub_time,origin_url,article_id) values (null,%s,%s,%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        defer = self.dbpool.runInteraction(self.insert_item, item)
        defer.addErrback(self.handle_error, item, spider)

    def insert_item(self, cursor, item):
        cursor.execute(self.sql, (
        item['title'], item['content'], item['author'], item['avatar'], item['pub_time'], item['origin_url'],
        item['article_id']))

    def handle_error(self, error, item, spider):
        print('=' * 20 + 'error' + '=' * 20)
        print(error)
        print('=' * 20 + 'error' + '=' * 20)
