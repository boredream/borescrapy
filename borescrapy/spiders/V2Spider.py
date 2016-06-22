# -*- coding: utf-8 -*-
import os
import urllib2

import scrapy


class V2Spider(scrapy.spiders.Spider):
    name = "v2"
    allowed_domains = []
    start_urls = [
        "http://v2new.com/v/original?play_count=desc&page=1"
    ]

    def parse(self, response):
        for sel in response.xpath('//div[@class="original-container"]'):
            name = sel.xpath('text()').extract()
            print "--------------------------- name " + name
            print "---------------------------  " + sel


class Lu720Spider(scrapy.spiders.Spider):
    name = "lu720"
    allowed_domains = []
    start_urls = [
        "http://www.720qq.cc/vod-type-id-1-pg-1.html"
    ]
    for i in range(2, 50):
        page = "http://www.720qq.cc/vod-type-id-1-pg-%s.html" % str(i)
        start_urls.append(page)

    file_dir = 'E:/spider_video/lu720/'

    def parse(self, response):
        for sel in response.xpath('//div[@class="citem film-box"]'):
            name = sel.xpath('div/div/a/@title').extract()[0]
            img_link = sel.xpath('div/a/img/@src').extract()[0]
            v_id = img_link.split('_')[len(img_link.split('_'))-1].replace('.jpg', '')
            v_link = "http://91kan2.345lu.cc/%s.mp4" % v_id

            file_name = self.file_dir + name + ".mp4"

            if os.path.exists(file_name):
                print ' ---------------- exsist name = ' + file_name
                continue

            try:
                f = urllib2.urlopen(v_link)
                data = f.read()

                print ' ---------------- download video name = ' + name

                with open(file_name, "wb") as code:
                    code.write(data)
            except urllib2.HTTPError, e:
                print ' ---------------- download video name = ' \
                      + name + " ~ error = " + str(e)


class Porn91(scrapy.spiders.Spider):
    name = "porn91"
    allowed_domains = []
    start_urls = [
        "http://fa.email.dao.91dizhi.at.gmail.com.9p3.club/v.php?category=rf&viewtype=basic&page=1"
    ]
    for i in range(2, 3):
        page = "http://fa.email.dao.91dizhi.at.gmail.com.9p3.club/v.php?category=rf&viewtype=basic&page=" + str(i)
        start_urls.append(page)

    file_dir = 'E:/spider_video/porn91/'

    def parse(self, response):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2"
        }

        yield scrapy.Request(response.url, headers=headers, callback=self.parseVideo)

    def parseVideo(self, response):
        for sel in response.xpath('//div[@class="listchannel"]'):
            name = sel.xpath('div/a/img/@title').extract()[0].replace(u'【申精】', '')
            img_link = sel.xpath('div/a/img/@src').extract()[0]
            v_id = img_link.split('_')[len(img_link.split('_')) - 1].replace('.jpg', '')
            v_link = "http://91kan.345lu.cc/%s.mp4" % v_id

            name = name.replace(u'?', '')
            name = name.replace(u'？', '')
            name = name.replace(u'"', '')
            name = name.replace(u'“', '')
            name = name.replace(u'”', '')
            name = name.replace(u'/', '')
            name = name.replace(u'\\', '')
            name = name.replace(u'<', '')
            name = name.replace(u'>', '')
            name = name.replace(u'*', '')
            name = name.replace(u'|', '')
            name = name.replace(u':', '')
            name = name.replace(u'：', '')
            file_name = self.file_dir + name + ".mp4"

            if os.path.exists(file_name):
                print ' ---------------- exsist name = ' + file_name
                continue

            self.downloadVideo(v_link, name, file_name)

    def downloadVideo(self, v_link, name, file_name, num = 8):
        try:
            v_link = v_link.replace("http://91kan", "http://91kan" + str(num))
            f = urllib2.urlopen(v_link)
            data = f.read()

            if len(data) < 2000:
                return

            print ' ---------------- download video name = ' + name + " .. link = " + v_link + " ... len = " + str(len(data))

            with open(file_name, "wb") as code:
                code.write(data)
        except urllib2.HTTPError, e:
            if e.code == 404:
                if num > 1:
                    self.downloadVideo(v_link, name, file_name, num - 1)
            else:
                print ' ---------------- error ' + name + " ~ error info = " + str(e)