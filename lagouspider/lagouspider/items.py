# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose, TakeFirst


def get_salary_min(value):
    """提取最低工资"""
    return int(re.search('(\d+)k-', value).group(1))*1000


def get_salary_max(value):
    """提取最高工资"""
    return int(re.search('-(\d+)k', value).group(1))*1000


def remove_line(value):
    """移除下划线"""
    return value.replace("/", "").strip()


def get_work_year_min(value):
    """获取最小年限"""
    try:
        return re.search('.*(\d+)-.*', value).group(1)
    except Exception as e:
        return 0


def get_work_year_max(value):
    """获取最大年限"""
    try:
        return re.search('-(\d+).*', value).group(1)
    except Exception as e:
        return 0


def get_pub_time(value):
    return re.search("(.*?)\xa0", value).group(1)


def remove_kwd(value):
    return value.replace("\xa0", " ")


class JobItemLoader(ItemLoader):
    """重写ItemLoader，从列表中提取第一个字段"""
    default_output_processor = TakeFirst()


class LagouspiderItem(scrapy.Item):
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    title = scrapy.Field()
    salary_min = scrapy.Field(input_processor=MapCompose(get_salary_min))
    salary_max = scrapy.Field(input_processor=MapCompose(get_salary_max))
    work_city = scrapy.Field(input_processor=MapCompose(remove_line))
    work_year_min = scrapy.Field(input_processor=MapCompose(get_work_year_min))
    work_year_max = scrapy.Field(input_processor=MapCompose(get_work_year_max))
    degree_need = scrapy.Field(input_processor=MapCompose(remove_line))
    job_type = scrapy.Field()
    publish_time = scrapy.Field(input_processor=MapCompose(get_pub_time))
    tags = scrapy.Field()
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field(input_processor=MapCompose(remove_kwd))

    def get_insert_sql(self):
        insert_sql = '''
                        insert into lagou_information(url, url_object_id, title, salary_min, salary_max, work_city, 
                        work_year_min, work_year_max, degree_need, job_type, publish_time, tags, job_advantage, job_desc)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        params = (self["url"], self["url_object_id"], self["title"], self["salary_min"], self["salary_max"],
                  self["work_city"], self["work_year_min"], self["work_year_max"], self["degree_need"],
                  self["job_type"], self["publish_time"], self["tags"], self["job_advantage"], self["job_desc"])
        return insert_sql, params




