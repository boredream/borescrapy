# -*- coding: utf-8 -*-

import scrapy
import sys
from borescrapy.items import TTYSItem


# scrapy crawl ttys
class TTYSSpider(scrapy.spiders.Spider):
    name = "ttys"
    allowed_domains = [""]
    start_urls = [
        # 8个
        "http://tv.cntv.cn/index.php?action=video-getVideoList&page=1&infoId=C10405000001&type=lanmu&flag=cu&videoId=9add24701ef241138186fa7cb8650b04&istiyu=0"
    ]
    for i in range(50, 200):
        page = "http://tv.cntv.cn/index.php?action=video-getVideoList&page=%s&infoId=C10405000001&type=lanmu&flag=cu&videoId=9add24701ef241138186fa7cb8650b04&istiyu=0" % str(i)
        start_urls.append(page)

    download_delay = 1

    def parse(self, response):
        page_index_start = response.url.find('page=') + len('page=')
        page_index_end = response.url.find('&infoId')

        current_page = response.url[page_index_start: page_index_end]

        print '-------------------- load page = ' + current_page

        reload(sys)
        sys.setdefaultencoding('utf-8')

        for sel in response.xpath('//dd/a'):
            item = TTYSItem()
            item['link_page'] = current_page

            s = sel.xpath('@title').extract()[0]
            ss = s.replace('《天天饮食》', '').replace('[天天饮食]', '').replace('天天饮食', '').strip()

            if ss.endswith('期'):
                # 翡翠白菜卷 2009年 第258期
                sss = ss.split(' ')
                if len(sss) == 3:
                    item['date'] = sss[1].decode('utf-8') + sss[2].decode('utf-8')
                    item['name'] = sss[0].decode('utf-8')
                else:
                    item['date'] = sss[1].decode('utf-8')
                    item['name'] = sss[0].decode('utf-8')

            elif len(ss.split(' ')) == 2:
                # 《天天饮食》 20120424 素蒸饼
                s1 = ss.split(' ')[0]
                s2 = ss.split(' ')[1]

                if s1.startswith('20'):
                    item['date'] = s1
                    item['name'] = s2.decode('utf-8')
                else:
                    item['date'] = s2
                    item['name'] = s1.decode('utf-8')

            elif len(ss.split(' ')) == 1:
                # [天天饮食] 司马怀府鸡
                item['name'] = ss.split(' ')[0].decode('utf-8')
                item['date'] = '未知'

            s = sel.xpath('@href').extract()
            item['link'] = s[0]

            yield item
