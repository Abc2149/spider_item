# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 拉勾python职位信息
class LagouspiderItem(scrapy.Item):

    city = scrapy.Field()                        # 城市
    companyFullName = scrapy.Field()             # 公司
    companySize = scrapy.Field()                 # 公司规模
    district = scrapy.Field()                    # 地区
    education = scrapy.Field()                   # 教育程度
    linestaion = scrapy.Field()                  # 前往路线
    positionName = scrapy.Field()                # 职位
    jobNature = scrapy.Field()                   # 工作要求
    workYear = scrapy.Field()                    # 工作经验
    salary = scrapy.Field()                      # 薪资
    CreateTime = scrapy.Field()                  # 发布时间





