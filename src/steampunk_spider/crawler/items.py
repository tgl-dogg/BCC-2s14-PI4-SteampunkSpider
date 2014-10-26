# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class StoreItem(scrapy.Item):
    # Definição dos nossos itens como objetos (ORM)
    # name = scrapy.Field()	
    name = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    # pass

class GroupItem(scrapy.Item):
	groupName = scrapy.Field()
	#Um grupo pode ter vários admins...
	groupAdmin = scrapy.Field()