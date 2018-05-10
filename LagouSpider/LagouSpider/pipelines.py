# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class LagouspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    def __init__(self):
        self.conn = pymysql.Connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='root',
            db='lagouspider',
            charset='utf8',
        )
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        sql = "insert into lagou(city,companyFullName,companySize,district,education,linestaion,positionName,jobNature,workYear,salary,CreateTime)\
            VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (item['city'], item['companyFullName'], item['companySize'], item['district'],
            item['education'], item['linestaion'],item['positionName'], item['jobNature'],
            item['workYear'], item['salary'], item['CreateTime'])
        self.cur.execute(sql)
        self.conn.commit()
        return item
