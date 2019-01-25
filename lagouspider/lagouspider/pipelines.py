# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi   # 将入库变成异步操作


class MysqlTwistedPipleline(object):
    """伯乐在线Pipleline"""
    def __init__(self, db_pool):
        self.db_pool = db_pool

    @classmethod
    def from_settings(cls, settings):
        """内置的方法自动调用settings"""
        db_params = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            password=settings["MYSQL_PASSWORD"],
            charset="utf8",
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        db_pool = adbapi.ConnectionPool("MySQLdb", **db_params)

        return cls(db_pool)

    def process_item(self, item, spider):
        """使用twisted异步插入数据值数据库"""
        query = self.db_pool.runInteraction(self.do_insert, item)    # runInteraction() 执行异步操作的函数
        query.addErrback(self.handle_error, item, spider)     # addErrback() 异步处理异常的函数

    def handle_error(self, failure, item, spider):
        """自定义处理异步插入数据的异常"""
        print(failure)

    def do_insert(self, cursor, item):
        """自定义执行具体的插入"""
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, (item["url"], item["url_object_id"], item["title"],
                                    item["salary_min"], item["salary_max"], item["work_city"],
                                    item["work_year_min"], item["work_year_max"], item["degree_need"],
                                    item["job_type"], item["publish_time"], item["tags"],
                                    item["job_advantage"], item["job_desc"]))
