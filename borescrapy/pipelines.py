# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import os
import sqlite3
import urllib2
import types


def get_download_video(item, start_video=47):
    name = item['name']

    # /video/C10405/c3cd9c3999e74c82b83ee9a06b430f63
    url_list = item['link'].split('/')
    video_id = url_list[len(url_list) - 1]

    # 2015/11/13
    if not len(item['date']) == 8:
        return
    date = item['date'][0:4] + '/' + item['date'][4:6] + '/' + item['date'][6:8]

    # http://vcntv.dnion.com/flash/mp4video47/TMS/2015/11/13/8d9824f36db5436c93374b4206061489_h264818000nero_aac32-1.mp4
    download_url = 'http://vcntv.dnion.com/flash/mp4video%d/TMS/%s/%s_h264818000nero_aac32-1.mp4' % (
        start_video, date, video_id)

    file_name = item['date'] + "_" + name + ".mp4"
    file_dir = 'E:/spider_video/ttys/'

    if os.path.exists(file_name):
        return

    # download
    for i in range(1, 10):
        # name
        file_name_part = file_dir + item['date'] + "_" + name + "_" + str(i) + ".mp4"

        if os.path.exists(file_name_part):
            continue

        # url
        download_url_part = download_url.replace('aac32-1', 'aac32-' + str(i))

        try:
            f = urllib2.urlopen(download_url_part)
            data = f.read()

            print ' ---------------- download_url_part = ' + download_url_part

            with open(file_name_part, "wb") as code:
                code.write(data)
        except urllib2.HTTPError, e:
            # 如果是404
            if e.code == 404:
                # 如果part数字为1，则代表url中的video数字错误
                if i == 1:
                    # video数字-1继续试验
                    get_download_video(item, start_video - 1)
                    break
                # 如果part数字不是1，则代表没有该part
                else:
                    # 结束循环
                    break

            print ' ---------------- download_url_part = ' + download_url_part + " error = " + str(e)


class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('data.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


class PrintPipeline(object):
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        print 'print line = ' + line
        return item


class SqlitePipeline(object):
    def __init__(self):
        self.sql = ''
        self.conn = sqlite3.connect('data.db')

    def close_spider(self, spider):
        self.conn.close()

    # name = scrapy.Field()
    # jingLuo = scrapy.Field()
    # jingLuoIndexDirection = scrapy.Field()
    # jingLuoIndex = scrapy.Field()
    # bodyArea = scrapy.Field()
    # wuShuType = scrapy.Field()
    # wuShuWuXing = scrapy.Field()
    # isYuanXueOfJingLuo = scrapy.Field()

    def process_item(self, item, spider):
        if self.sql == '':
            # 初始化table
            self.sql = 'CREATE TABLE DATA (ID INTEGER PRIMARY KEY, '
            for (key, value) in dict(item).items():
                # if isinstance(type(value), types.IntType):
                #     self.sql += (key + ' INTEGER, ')
                # elif isinstance(type(value), types.BooleanType):
                #     # boolean 用 int 型
                #     self.sql += (key + ' INTEGER, ')
                # else:
                #     self.sql += (key + ' TEXT,')

                self.sql += (key + ' TEXT,')

                print type(value)
            self.sql += ');'
            self.sql = self.sql.replace(',);', ');')

            print '------------- create Table = ' + self.sql

            self.conn.execute(self.sql)
            self.conn.commit()

        keys = ''
        values = ''
        for (key, value) in dict(item).items():
            keys += (', ' + key)
            values += (', \'' + value + '\'')

        insertSql = 'INSERT INTO DATA (' + keys[2:] + ') VALUES (' + values[2:] + ')'

        self.conn.execute(insertSql)
        self.conn.commit()

        return item
