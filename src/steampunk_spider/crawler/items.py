# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class StoreItem(scrapy.Item):
    # Definição dos nossos itens como objetos (ORM)
    # name = scrapy.Field()
    url = scrapy.Field()	
    name = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    linux = scrapy.Field()
    mac = scrapy.Field()
    windows = scrapy.Field()
    release = scrapy.Field()
    size = scrapy.Field()
    developer = scrapy.Field()

    # esses itens são da zoeira, porque recebem mais de um valor (partiu fazer uma lista)
    tags = scrapy.Field()
    genre = scrapy.Field()
    # pass

class GroupItem(scrapy.Item):
	groupName = scrapy.Field()

	# Um grupo pode ter vários admins...
	# RE: Relaxa Danilo, a gente faz um código da zoeira aqui também ;)
	groupAdmin = scrapy.Field()


class PlayerItem(scrapy.Item):
	url = scrapy.Field()
	name = scrapy.Field()
	real_name = scrapy.Field()
	nationality = scrapy.Field()
	level = scrapy.Field()
	description = scrapy.Field()
	last_login = scrapy.Field()
	vac_ban = scrapy.Field()
	primary_group = scrapy.Field()

	# Esses itens também são da zoeira (gotta list'em all!)
	games = scrapy.Field()
	friends = scrapy.Field()
	groups = scrapy.Field()
	url = scrapy.Field()

class PostItem(scrapy.Item):
	title = scrapy.Field()
	text = scrapy.Field()
	owner = scrapy.Field()