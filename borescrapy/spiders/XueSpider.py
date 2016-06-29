# -*- coding: utf-8 -*-

from scrapy.spider import BaseSpider
from borescrapy.items import XueItem


class XueSpider(BaseSpider):
    name = "xue"

    start_urls = ["http://www.a-hospital.com/w/%E7%A9%B4%E4%BD%8D"]

    def parse(self, response):
        items = []

        # 经络穴位
        jingluo = response.xpath('//table[@class="nowraplinks collapsible uncollapsed navbox-inner"]')[0]

        for sel in jingluo.xpath('tr[3]/td/table/tr'):
            ths = sel.xpath('th')
            if len(ths) == 0:
                continue

            jingluoname = ths[0].xpath('div/a/text()')[0].extract()
            jingLuoIndexDirection = ''
            if u'手' in jingluoname and u'阴' in jingluoname:
                jingLuoIndexDirection = u'从胸到手'
            elif u'手' in jingluoname and u'阳' in jingluoname:
                jingLuoIndexDirection = u'从手到头'
            elif u'足' in jingluoname and u'阴' in jingluoname:
                jingLuoIndexDirection = u'从足到腹'
            elif u'足' in jingluoname and u'阳' in jingluoname:
                jingLuoIndexDirection = u'从头到足'
            else:
                jingLuoIndexDirection = u'待补充'

            jingLuoIndex = 0
            for xue in sel.xpath('td/div/ul/li'):
                item = XueItem()
                body_name = xue.xpath('a/text()')[0].extract()
                item['name'] = body_name
                item['jingLuo'] = jingluoname
                item['jingLuoIndexDirection'] = jingLuoIndexDirection
                item['jingLuoIndex'] = str(jingLuoIndex)
                items.append(item)

                jingLuoIndex += 1

        functionTypes = [
            u'解表穴',
            u'清心热穴',
            u'清肺热穴',
            u'清肝胆热穴',
            u'清胃肠热穴',
            u'清三焦热穴',
            u'清热解毒穴',
            u'止咳平喘化痰穴',
            u'消食导滞穴',
            u'益气壮阳穴',
            u'补阴穴',
            u'温里穴',
            u'平肝息风穴',
            u'理气穴',
            u'理血穴',
            u'调经止带穴',
            u'利水通淋穴',
            u'安神穴',
            u'开窍苏厥穴',
            u'利目穴',
            u'利鼻穴',
            u'利耳穴',
            u'利口舌咽喉穴',
            u'通利诸窍穴',
            u'袪风除湿穴',
            u'舒筋活络穴',
        ]

        functionXues = []
        for sel in response.xpath('//div[@id="bodyContent"]/p'):
            if len(sel.xpath('a')) < 3:
                continue

            xues = ''
            isAllXue = True
            for xue in sel.xpath('a'):
                xue = xue.xpath('text()').extract()[0]
                if u'穴' not in xue:
                    isAllXue = False
                    break

                xues += (',' + xue)

            xues = xues[1:]

            if isAllXue:
                functionXues.append(xues)

        # 穴位-功能 字典
        xueFunctionDict = {}
        for index in range(0, len(functionTypes)):
            for xue in functionXues[index].split(','):
                if xue[-1] == u'穴':
                    xue = xue[0: len(xue) - 1]
                xueFunctionDict[xue] = functionTypes[index]

        # 穴位-部位 字典
        xueBodyDict = {}
        body = response.xpath('//table[@class="nowraplinks collapsible uncollapsed navbox-inner"]')[1]
        for index in range(0, len(body.xpath('tr'))):
            sel = body.xpath('tr')[index]

            ths = sel.xpath('th')
            tds = sel.xpath('td')
            if len(ths) == 0 or len(tds) == 0:
                continue

            body_name = ths[0].xpath('text()')[0].extract()
            if body_name == u'腹部':
                body_name = u'腹部胸部'

            if body_name == u'头部':
                index = 0
                for header in tds[0].xpath('table/tr'):
                    ths = header.xpath('th')
                    if len(ths) == 0:
                        continue

                    index += 1
                    body_part = header.xpath('th/div/text()')[0].extract()
                    if index == 3:
                        body_part = u'侧面'

                    for xue in header.xpath('td/div/ul/li/a'):
                        xue = xue.xpath('text()')[0].extract()
                        if xue[-1] == u'穴':
                            xue = xue[0: len(xue) - 1]
                        xueBodyDict[xue] = body_name + body_part
            else:
                for xue in tds[0].xpath('div/ul/li/a'):
                    xue = xue.xpath('text()')[0].extract()
                    if xue[-1] == u'穴':
                        xue = xue[0: len(xue) - 1]
                    xueBodyDict[xue] = body_name

        # 穴位-五输穴 字典
        xueWuShuTypeDict = {}
        # 穴位-五输穴五行 字典
        wuShuWuXingDict = {}
        wushu = response.xpath('//table[@class="wikitable"]')[0]
        for index in range(1, len(wushu.xpath('tr'))):
            sels = wushu.xpath('tr')[index]

            # 所属经络阴阳
            isYin = (u'阴' in sels.xpath('td/a/text()')[0].extract())

            # 井穴
            xueWuShuTypeDict[sels.xpath('td/a/text()')[1].extract()] = u'井穴'
            wuShuWuXingDict[sels.xpath('td/a/text()')[1].extract()] = (u'木' if isYin else u'金')
            # 荥穴
            xueWuShuTypeDict[sels.xpath('td/a/text()')[2].extract()] = u'荥穴'
            wuShuWuXingDict[sels.xpath('td/a/text()')[1].extract()] = (u'火' if isYin else u'水')
            # 输穴
            xueWuShuTypeDict[sels.xpath('td/a/text()')[3].extract()] = u'输穴'
            wuShuWuXingDict[sels.xpath('td/a/text()')[1].extract()] = (u'土' if isYin else u'木')
            # 经穴
            xueWuShuTypeDict[sels.xpath('td/a/text()')[4].extract()] = u'经穴'
            wuShuWuXingDict[sels.xpath('td/a/text()')[1].extract()] = (u'金' if isYin else u'火')
            # 合穴
            xueWuShuTypeDict[sels.xpath('td/a/text()')[5].extract()] = u'合穴'
            wuShuWuXingDict[sels.xpath('td/a/text()')[1].extract()] = (u'水' if isYin else u'土')

        for item in items:
            name = item['name']
            if name in xueFunctionDict:
                item['functionType'] = xueFunctionDict[name]
            if name in xueBodyDict:
                item['bodyArea'] = xueBodyDict[name]
            if name in xueWuShuTypeDict:
                item['wuShuType'] = xueWuShuTypeDict[name]
            if name in wuShuWuXingDict:
                item['wuShuWuXing'] = wuShuWuXingDict[name]
            yield item
