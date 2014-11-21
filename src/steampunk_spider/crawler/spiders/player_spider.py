# -*- coding: utf-8 -*-
from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode

from crawler.items import PlayerItem
from crawler import my_utils as utils

import scrapy

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest

import re

####################################################################################
#################################### HOW TO RUN ####################################
# scrapy crawl playerspider -s JOBDIR=cache_02/player/playerspider-1 -o steam.json #
####################################################################################


def insert_nationality(db_conn, db_cursor, nationality):
    exist_check = ("SELECT id_nationality FROM nationality WHERE name LIKE \'%s\'" % nationality)
    db_cursor.execute(exist_check)

    data_exists = db_cursor.fetchone()
    if data_exists:
        id_nationality = data_exists[0]
    else:
        insert = ("INSERT INTO nationality "
              "(name) "
              "VALUES ('%s')" % nationality)

        db_cursor.execute(insert)
        db_conn.commit()

        id_nationality = db_cursor.lastrowid
   
    return id_nationality


def insert_player(db_conn, db_cursor, player):
    add_player = ("INSERT IGNORE INTO player "
              "(id_steam, url, username, real_name, description, level, last_login, vac_ban, fk_nationality, public, bcc) "
              "VALUES (%(id_steam)s, %(url)s, %(username)s, %(real_name)s, %(description)s, %(level)s, %(last_login)s, %(vac_ban)s, %(fk_nationality)s, %(public)s, %(bcc)s)")

    # print (add_player)

    data_player = {
        'id_steam': player['id_steam'],
        'url': player['url'],
        'username': player['username'],
        'real_name': player['real_name'],
        'description': player['description'],
        'level': player['level'],
        'last_login': player['last_login'],
        'vac_ban': player['vac_ban'],
        'fk_nationality': player['nationality'],
        'public': player['public'],
        'bcc': player['bcc'],
    }

    # print (data_player)

    db_cursor.execute(add_player, data_player)
    db_conn.commit()

class PlayerSpider(CrawlSpider):
    global db_conn
    global db_cursor

    name = "playerspider"
    allowed_domains = ["steamcommunity.com"]
    start_urls = [
        "http://steamcommunity.com/profiles/76561197961417376",
        "http://steamcommunity.com/profiles/76561198041876420",
        "http://steamcommunity.com/id/palmdesert",
        "http://steamcommunity.com/id/flushjackson",
        "http://steamcommunity.com/id/FurfagMasterRace",
        
        # pessoal do BCC:        
        # "http://steamcommunity.com/id/tgl_dogg",
        # "http://steamcommunity.com/id/andressahs",
        # "http://steamcommunity.com/id/ganopper",
        # "http://steamcommunity.com/id/crewzito",
        # "http://steamcommunity.com/id/LHSP",
        # "http://steamcommunity.com/id/attnk",
        # "http://steamcommunity.com/id/gabrielgfa1",
        # "http://steamcommunity.com/id/gabrielkoji",
        # "http://steamcommunity.com/id/vnavarro",
        # "http://steamcommunity.com/id/mariotoledo",
        # "http://steamcommunity.com/id/mirwox",
        # "http://steamcommunity.com/id/colares07",
        # "http://steamcommunity.com/id/LineZCL",
        # "http://steamcommunity.com/id/gabrielkoji",        
        # "http://steamcommunity.com/id/ezefranca/friends",
        # "http://steamcommunity.com/id/atilevil/friends",
        # "http://steamcommunity.com/id/fblanes11/friends",
        # "http://steamcommunity.com/id/dalbera/friends",
        # "http://steamcommunity.com/id/yarquenrey/friends",
        # "http://steamcommunity.com/id/daniloreborn/friends",
        # "http://steamcommunity.com/id/ricardomsj/friends",
        # "http://steamcommunity.com/id/caiomvs/friends",
        # "http://steamcommunity.com/profiles/76561198076462157",
        # "http://steamcommunity.com/profiles/76561198096883452",
        # "http://steamcommunity.com/profiles/76561198016047992",
        # "http://steamcommunity.com/profiles/76561197992683087",
        # "http://steamcommunity.com/profiles/76561198035026444",
        # "http://steamcommunity.com/profiles/76561197994541512",
        # "http://steamcommunity.com/profiles/76561197977061422",
        # "http://steamcommunity.com/profiles/76561198038259656",
        # "http://steamcommunity.com/profiles/76561198010836584",
        # "http://steamcommunity.com/profiles/76561198030971039",
        # "http://steamcommunity.com/profiles/76561198044708540", 
        # "http://steamcommunity.com/profiles/76561198066500019",
        # "http://steamcommunity.com/profiles/76561198147136494",
        # "http://steamcommunity.com/profiles/76561198067478519",
        # "http://steamcommunity.com/profiles/76561198111316291",
        # "http://steamcommunity.com/profiles/76561198143778305",
    ]

    # Esses itens também são da zoeira (gotta list'em all!)
    # games = scrapy.Field()
    # friends = scrapy.Field()

    # Tratar este caso:
    # http://steamcommunity.com/profiles/76561197991859336/friends/
    # http://steamcommunity.com/id/tgl_dogg/friends/
    rules = (
        Rule(
            LinkExtractor(
                allow=('(id|profiles)/([a-zA-Z_]|[0-9]){1,}', ),
                deny=('\?l', 'facebook', 'twitter', 'login', 'reddit', 'inventory', 'badges', 'gamecards', 'screenshots', 'videos', 'images', 'myworkshopfiles', 'stats', 'wishlist', 'recommended'),  
                ),
            callback='parse_player',
            # process_links='link_processor', 
            follow=False,
        ),
    )

    social_url = re.compile('(.+?)/(friends|groups|games)')

    print ("open database")
    db_conn = mysql.connector.connect(user='root', password='@TGL_Dogg', host='localhost', database='steampunk')
    db_cursor = db_conn.cursor()

    def spider_ended(spider):
        db_conn.close()
        db_cursor.close()
        print ("close database")

    dispatcher.connect(spider_ended, signals.spider_closed)

#scrapy crawl playerpider -s JOBDIR=crawls/somespider-1
    
    # def link_processor(self, links):

                  
    def parse_player(self, response):
        is_social_url = re.search(self.social_url, response.url) != None
        
        # São urls com listagem de jogos, não parseamos elas, apenas visitamos para pegar mais jogos.
        if (is_social_url):
            return

        id_steam = 0
        # Se eu fosse definir quão pesada esta gambiarra é, seria "2x(sua mãe)" #YourMotherJokes
        str_id_steam = response.xpath('substring-after(substring-before(//html, "personaname"), "steamid")').re('"([[0-9]{1,})"')
        if str_id_steam:
            id_steam = str_id_steam[0].strip().encode('utf-8')
        else:
            print ("invalid id")
            return

        nationality = "00"
        country_flag = response.xpath('//img[@class="profile_flag"]').re('(?:countryflags/)(.+?)(.gif)')
        if (country_flag):
            nationality = country_flag[0]

        username = ""
        search_name = response.xpath('//div[@class="persona_name"]/text()').extract()
        if search_name:
            username = search_name[0].strip().encode('utf-8')
        
        real_name = ""
        search_real_name = response.xpath('//div[@class="header_real_name ellipsis"]/text()').extract()
        if search_real_name:
            real_name = search_real_name[0].strip().encode('utf-8')

        last_login = ""
        time_stamp = response.xpath('//div[@class="profile_in_game_name"]/text()').extract()
        if time_stamp:
            last_login = time_stamp[0].strip().encode('utf-8')

        url = response.url
        level = utils.level_validator(response.xpath('//div[@class="persona_name persona_level"]//span[@class="friendPlayerLevelNum"]/text()').extract())
        description = utils.description_validator(response.xpath('//div[@class="profile_summary"]//text()').extract())
        vac_ban = utils.vac_ban_validator(response.xpath('//div[@class="profile_ban_status"]/text()').extract())
        public = utils.public_validator(response.xpath('//div[@class="profile_private_info"]/text()').extract())
        bcc = 0

        id_nationality = insert_nationality(db_conn, db_cursor, nationality)

        item = PlayerItem()
        item['url'] = url        
        item['id_steam'] = id_steam
        item['username'] = username
        item['level'] = level
        item['description'] = description
        item['real_name'] = real_name
        item['vac_ban'] = vac_ban
        item['last_login'] =  last_login
        item['nationality'] = id_nationality
        item['public'] = public
        item['bcc'] = bcc

        insert_player(db_conn, db_cursor, item)

        yield item