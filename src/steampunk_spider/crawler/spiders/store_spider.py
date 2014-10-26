import scrapy

from crawler.items import StoreItem

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest

import re

class StoreSpider(CrawlSpider):
    name = "storespider"
    allowed_domains = ["store.steampowered.com"]
    start_urls = [
        #"http://store.steampowered.com/",
        "http://store.steampowered.com/app/730",
        #"http://store.steampowered.com/app/265590",
        #"http://store.steampowered.com/app/222880"
    ]
    rules = (
        Rule(
            LinkExtractor(
                #recommended/morelike/app/[0-9]{1,}'
                allow=('app/[0-9]{1,}', ),
                deny=('\?l', '\?snr=1_5_9__205', 'facebook', 'twitter', 'login', 'reddit'),
                #allow_domains=('http://store.steampowered.com/recommended/morelike/app/', ),       
            ),
            
            callback='parse_items', 
            follow=True
        ), 
    )

    def parse_items(self, response):
        items_list = list();

        item = StoreItem()
        item['name'] = response.xpath('//div[@class="apphub_AppName"]/text()').extract()
        item['price'] = response.xpath('//meta[@itemprop="price"]/@content').extract()
        #item['description'] = response.xpath('text()').extract()
        
        items_list.append(item)

        yield item 

        # for founds in response.xpath('//script'):#.xpath('//ul/li'):
        #    item = StoreItem()
        #    item['name'] = founds.xpath('//div[@class="apphub_AppName"]').extract()
        #    #item['price'] = founds.xpath('//meta[@itemprop="price"]').extract()
        #    #item['description'] = founds.xpath('text()').extract()
        #    items_list.append(item) 
        #    #yield item

        # for i in items_list:
        #     print "\nitem: "
        #     print i
        #     print "\n"
        #     #yield i

        #print len(items_list)