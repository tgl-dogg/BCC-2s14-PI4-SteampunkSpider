# -*- coding: utf-8 -*-

import scrapy

from scrapy_glance.items import GroupItem

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest

class DmozSpider(CrawlSpider):
    name = "groupSpider"
    allowed_domains = ["http://steamcommunity.com/"]
    start_urls = [
        "http://steamcommunity.com/groups/bfgpg"
    ]
    rules = (
        Rule(
            LinkExtractor(
                allow=('app/[0-9]{1,}', ),
                #deny=('?l', )
                ), 
                callback='parse_items', 
                follow=False,
            ),
        )

    def parse_items(self, response):
        for founds in response.xpath('//script'):#.xpath('//ul/li'):
            item = ScrapyGlanceItem()
            item['groupName'] = founds.xpath('//div[@class="grouppage_header_name"]').extract()

            #Agora, como pegar só os admins são outros 500...
            item['groupAdmin'] = founds.xpath('//div[@class="playerAvatar online"]').extract()
                #founds.xpath('//div[@class="playerAvatar offline"]').extract(),
                #founds.xpath('//div[@class="playerAvatar in-game"]').extract()
            #item['description'] = founds.xpath('text()').extract()
            print "item: " 
            print item['groupName'] + item['groupAdmin']
            #yield item