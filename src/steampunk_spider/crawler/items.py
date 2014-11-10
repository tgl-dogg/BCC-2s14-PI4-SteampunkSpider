# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class StoreItem(scrapy.Item):
    url = scrapy.Field()	
    id_software = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    linux = scrapy.Field()
    mac = scrapy.Field()
    windows = scrapy.Field()
    release_date = scrapy.Field()
    hdd_space = scrapy.Field()

class PlayerItem(scrapy.Item):
	url = scrapy.Field()
	id_steam = scrapy.Field()
	name = scrapy.Field()
	real_name = scrapy.Field()
	level = scrapy.Field()
	description = scrapy.Field()
	last_login = scrapy.Field()
	vac_ban = scrapy.Field()

class PostItem(scrapy.Item):
	title = scrapy.Field()
	text = scrapy.Field()
	owner = scrapy.Field()