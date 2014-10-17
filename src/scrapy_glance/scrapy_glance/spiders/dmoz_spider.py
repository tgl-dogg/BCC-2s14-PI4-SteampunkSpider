import scrapy

from scrapy_glance.items import ScrapyGlanceItem

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest

class DmozSpider(CrawlSpider):
    name = "steampowered"    
    allowed_domains = ["store.steampowered.com"]
    start_urls = [
        "http://store.steampowered.com/app/730",
        #"http://store.steampowered.com/app/265590",
        #"http://store.steampowered.com/app/222880"
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
            item['name'] = founds.xpath('//div[@class="apphub_AppName"]').extract()
            item['price'] = founds.xpath('//meta[@itemprop="price"]').extract()
            #item['description'] = founds.xpath('text()').extract()
            print "item: " 
            print item['name'] + item['price']
            #yield item