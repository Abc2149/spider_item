# -*- coding: utf-8 -*-
import scrapy
from LagouSpider.items import LagouspiderItem
import json, time, random, re


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['http://www.lagou.com/']

    # https://www.lagou.com/jobs/positionAjax.json?city=%E5%B9%BF%E5%B7%9E&needAddtionalResult=false
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
        'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
    }
    url = 'https://www.lagou.com/jobs/positionAjax.json?'
    page = 1

    def start_requests(self):  # 构建开始请求地址
        yield scrapy.FormRequest(
            self.url, headers=self.headers,
            formdata={
                'needAddtionalResult': 'false',
                'city': '广州',
                'first': 'true',
                'pn': str(self.page),
                'kd': 'python',
            }, callback=self.parse
        )

    def parse(self, response):
        item = LagouspiderItem()
        data = json.loads(response.text)
        result = data['content']['positionResult']['result']   #  职位信息
        resultSize = data['content']['positionResult']['resultSize']  # 职位条数
        totalCount = data['content']['positionResult']['totalCount']  # 总职位条数

        for message in result:
            item['city'] = message['city']
            item['companyFullName'] = message['companyFullName']
            item['companySize'] = message['companySize']
            item['district'] = message['district']
            item['education'] = message['education']
            item['linestaion'] = message['linestaion']
            item['positionName'] = message['positionName']
            item['jobNature'] = message['jobNature']
            item['workYear'] = message['workYear']
            item['salary'] = message['salary']
            item['CreateTime'] = message['formatCreateTime']
            yield item

        time.sleep(random.randint(10, 30))
        if int(resultSize) == 15:
            allpage = int(totalCount) / int(resultSize) + 1  # 98/15 + 1    共7页
            if self.page < allpage:
                self.page += 1
                print('正在请求第%s页' % self.page)
                if self.page % 5 == 0:
                    time.sleep(20)           # 爬取5页数据之后会被禁止
                yield scrapy.FormRequest(
                    self.url, headers=self.headers,
                    formdata={
                        'needAddtionalResult': 'false',
                        'city': '广州',
                        'first': 'false',
                        'pn': str(self.page),
                        'kd': 'python',
                    }, callback=self.parse
                )


