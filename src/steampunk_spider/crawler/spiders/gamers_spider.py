# -*- coding: utf-8 -*-
from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode

from crawler.items import GameItem
from crawler import my_utils as utils

import json

import scrapy

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest

import re

# Disclaimer:
# The following code has been based on a gist provided by madebyjazz in the following url:
# https://gist.github.com/madebyjazz/1090663
# PS: thank you, madebyjazz!

#####################################################################
############################ HOW TO RUN #############################
# scrapy crawl gamersspider -s JOBDIR=cache_02/player/gamersspider-1 #
#####################################################################


def insert_rel_player_software(db_conn, db_cursor, id_player, item):
    exist_check = ("SELECT name FROM software WHERE id_software=%s" % item['id_game'])
    db_cursor.execute(exist_check)

    exists = db_cursor.fetchone()
    if not exists:
        add_software = ("INSERT INTO software "
            "(id_software, url, name, description) "
            "VALUES (%(id_software)s, %(url)s, %(name)s, %(description)s)")

        data_software = {
            'id_software': item['id_game'],
            'url': item['url'],
            'name': item['name'],
            'description': item['description'],
        }

        db_cursor.execute(add_software, data_software)
        db_conn.commit()
    
    add_rel = ("INSERT IGNORE INTO rel_player_software "
        "(fk_player, fk_software, hours) "
        "VALUES (%(fk_player)s, %(fk_software)s, %(hours)s)")

    data_rel = {
        'fk_player': id_player,
        'fk_software': item['id_game'],
        'hours': item['hours'],
    }

    db_cursor.execute(add_rel, data_rel)
    db_conn.commit()


def next_player(db_cursor):
    players = []
    game_tab = "/games/?tab=all"

    query = "SELECT id_player, url FROM player where public=1 limit 5001,10000"
    db_cursor.execute(query)

    for id_player, url in db_cursor:
        players.append({'url': (url+game_tab), 'id':id_player})

    # players.append({'url':"http://steamcommunity.com/id/tgl_dogg/games/?tab=all", 'id':2345678})
    # players.append({'url':"http://steamcommunity.com/id/thecoinguy/games/?tab=all", 'id':66666666666})

    for player in players:
        yield player

class GamersSpider(CrawlSpider):
    global db_conn
    global db_cursor

    name = "gamersspider"
    allowed_domains = ["steamcommunity.com"]
    start_urls = []

    print ("open database")
    db_conn = mysql.connector.connect(user='root', password='@TGL_Dogg', host='localhost', database='steampunk')
    db_cursor = db_conn.cursor()

    def spider_ended(spider):
        db_conn.close()
        db_cursor.close()
        print ("close database")

    dispatcher.connect(spider_ended, signals.spider_closed)

    players = next_player(db_cursor)
    current_player = players.next()

    def start_requests(self): 
        ## grab the first URL to being crawling
        start_url = self.current_player['url']
        
        print ('START_REQUESTS : start_url = %s' % start_url)
 
        request = Request(start_url, dont_filter=True)
        
        ### important to yield, not return (not sure why return doesn't work here)
        yield request
                  
    def parse(self, response):
        items = []
 
        json_games_raw = response.xpath('substring-before(substring-after(//html, "var rgGames = "), "];")').extract()
        
        if(json_games_raw[0]):
            id_player = self.current_player['id']

            json_games = (json_games_raw[0] + "]").encode('utf-8')
            games_dict = json.loads(json_games)
                        
            # Get all player owned games
            for game in games_dict:
                id_game = int(game['appid'])
                name = game['name'].encode('utf-8')
                url = "http://store.steampowered.com/app/" + str(id_game)

                hours = 0.0
                if ('hours_forever' in game):
                    hours = float(game['hours_forever'].replace(',',''))

                if hours < 1:
                    # Jogou menos de uma hora, provavelmente nem jogou direito, vamos parar por aqui
                    break;

                item = GameItem()
                item['id_game'] = id_game
                item['hours'] = hours
                item['name'] = name
                item['url'] = url
                item['description'] = "none"

                # print(item)
                insert_rel_player_software(db_conn, db_cursor, id_player, item)
        else:
            print ("failed to xpath")

        self.current_player = self.players.next()
        yield Request(self.current_player['url'])