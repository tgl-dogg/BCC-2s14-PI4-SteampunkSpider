# -*- coding: utf-8 -*-
import scrapy

from crawler.items import PlayerItem

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest

from crawler import my_utils as utils

import re

class PlayerSpider(CrawlSpider):
    name = "playerspider"
    allowed_domains = ["steamcommunity.com"]
    start_urls = [
        "http://steamcommunity.com/id/tgl_dogg",
        # "http://steamcommunity.com/profiles/76561197961417376",
        # "http://steamcommunity.com/profiles/76561198041876420",
        # "http://steamcommunity.com/id/palmdesert",
        # "http://steamcommunity.com/id/flushjackson",
        # "http://steamcommunity.com/id/FurfagMasterRace",
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
                deny=('\?l', 'facebook', 'twitter', 'login', 'reddit', 'inventory', 'badges', 'gamecards', 'screenshots', 'videos', 'images', 'myworkshopfiles', 'stats'),  
                ),
            callback='parse_player',
            # process_links='link_processor', 
            follow=True,
        ),
    )

    # def link_processor(self, links):

                  
    def parse_player(self, response):
        item = PlayerItem()

        # Evitar urls de inventário, etc.
        # Itens descomentados estão GG já
        url = response.url
        
        id_steam = 0
        # Se eu fosse definir quão pesada esta gambiarra é, seria "2x(sua mãe)" #YourMotherJokes
        str_id_steam = response.xpath('substring-after(substring-before(//html, "personaname"), "steamid")').re('"([[0-9]{1,})"')
        if str_id_steam:
            id_steam = int(str_id_steam[0])

        # <script type="text/javascript">
        #     g_rgProfileData = {"url":"http:\/\/steamcommunity.com\/profiles\/76561198128011421\/","steamid":"76561198128011421","personaname":"Bea.triz"};
        # </script>
        
        item['url'] = url        
        item['id_steam'] = id_steam
        # item['name'] = response.xpath('//div[@class="persona_name"]/text()').extract()[0].strip()

        # item['level'] = response.xpath('//div[@class="persona_name persona_level"]//span[@class="friendPlayerLevelNum"]/text()').extract()
        # item['description'] = utils.description_validator(response.xpath('//div[@class="profile_summary"]/text()').extract())
        # item['real_name'] = response.xpath('//div[@class="header_real_name ellipsis"]/text()').extract()[0].strip()
        # item['vac_ban'] = response.xpath('//div[@class="profile_ban_status"]/text()').extract()
        # item['last_login'] = response.xpath('//div[@class="profile_in_game_name"]/text()').extract() #isto pega uma string completa do tipo: Última vez online: há 24 mins ou Dísponível
        # nationality = response.xpath('//img[@class="profile_flag"]').re('(?:countryflags/)(.+?)(.gif)')[0] #vem no formato escrito abaixo (3)
            
        yield item



### (1)
### <script type="text/javascript">
###                g_rgProfileData = {"url":"http:\/\/steamcommunity.com\/profiles\/76561198071309654\/","steamid":"76561198071309654","personaname":"Hyukoroo","summary":"Nada informado."};
###
###

### (2)
### Quanto a grupos, o código vem assim (para o mainGroup)
### <div class="profile_group profile_primary_group">
### <div class="profile_group_avatar">
###    <a href="http://steamcommunity.com/groups/gamersunidosbrasil">
###

### (3)
###
### <div class="header_real_name ellipsis">
### Vinicius de Carvalho															&nbsp;
###     <img class="profile_flag" src="http://steamcommunity-a.akamaihd.net/public/images/countryflags/br.gif">
###         Sao Paulo, Sao Paulo, Brazil						</div>