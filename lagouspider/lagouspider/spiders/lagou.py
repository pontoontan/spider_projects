# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..utils.utils import get_url_obj
from ..items import JobItemLoader, LagouspiderItem


class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']

    rules = (
        Rule(LinkExtractor(allow=('zhaopin/.*',)), follow=True),
        Rule(LinkExtractor(allow=('gongsi/\d+.html',)), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
    )
    custom_settings = {
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_START_DELAY": 0.5,
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 3,
        'DEFAULT_REQUEST_HEADERS': {
            'Cookie': 'GA1.2.216116071.1544854465; user_trace_token=20181215141426-acbdeb27-0030-11e9-8cef-5254005c3644; LGUID=20181215141426-acbdeea8-0030-11e9-8cef-5254005c3644; index_location_city=%E5%85%A8%E5%9B%BD; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; JSESSIONID=ABAAABAAAGFABEF70F564B8430D3842C5389F2355B8E197; TG-TRACK-CODE=index_navigation; LGSID=20181230153204-013d921a-0c05-11e9-b455-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2FPython%2F%3FlabelWords%3Dlabel; SEARCH_ID=377d45219e5f4fd399c1e31cd3e78f0c; _gat=1; login=false; unick=""; _putrc=""; LG_LOGIN_USER_ID=""; LGRID=20181230160124-1a6ff1f7-0c09-11e9-b455-525400f775ce',
            'Host': 'www.lagou.com',
            'Origin': 'https://www.lagou.com',
            'Referer': 'https://www.lagou.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }
    }

    def parse_job(self, response):
        # 解析拉钩网的职位
        item_load = JobItemLoader(item=LagouspiderItem(), response=response)
        item_load.add_value("url", response.url)
        item_load.add_value("url_object_id", get_url_obj(response.url))
        item_load.add_xpath("title", "//div[@class='job-name']/@title")
        item_load.add_xpath("salary_min", "//dd[@class='job_request']/p/span[1]/text()")
        item_load.add_xpath("salary_max", "//dd[@class='job_request']/p/span[1]/text()")
        item_load.add_xpath("work_city", "//dd[@class='job_request']/p/span[2]/text()")
        item_load.add_xpath("work_year_min", "//dd[@class='job_request']/p/span[3]/text()")
        item_load.add_xpath("work_year_max", "//dd[@class='job_request']/p/span[3]/text()")
        item_load.add_xpath("degree_need", "//dd[@class='job_request']/p/span[4]/text()")
        item_load.add_xpath("job_type", "//dd[@class='job_request']/p/span[5]/text()")
        item_load.add_xpath("publish_time", "//p[@class='publish_time']/text()")
        item_load.add_xpath("tags", "///ul[@class='position-label clearfix']/li/text()")
        item_load.add_xpath("job_advantage", "//dd[@class='job-advantage']/p/text()")
        item_load.add_xpath("job_desc", "//div[@class='job-detail']/p/text()")

        lagou_item = item_load.load_item()
        yield lagou_item
