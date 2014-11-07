# -*- coding: utf-8 -*-
import scrapy

from crawler.items import PlayerItem

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest

from crawler import my_utils as utils

import re

class DmozSpider(CrawlSpider):
    name = "playerspider"
    allowed_domains = ["steamcommunity.com"]
    start_urls = [
        "http://steamcommunity.com/id/tgl_dogg",
        "http://steamcommunity.com/id/palmdesert",
        "http://steamcommunity.com/id/flushjackson",
        "http://steamcommunity.com/profiles/76561197961417376",
    ]
    rules = (
        Rule(
            LinkExtractor(
                allow=('(id|profiles)/([a-zA-Z_]|[0-9]){1,}', ),
                deny=('\?l', 'facebook', 'twitter', 'login', 'reddit', 'inventory', 'badges', 'gamecards', 'screenshots', 'videos', 'images', 'myworkshopfiles'),  
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

        item['url'] = response.url
        item['name'] = response.xpath('//div[@class="persona_name"]/text()').extract()[0].strip()
        # item['idSteam'] = response.xpath('//"]').extract()
        
        #   Os dois acima não sei de onde extrair, 
        #   entretanto, eu tenho a ligeira impressão de que o teremos 
        # "antes", dado que acessamos o jogador pelo url dele, 
        # e o id pode sempre ser usado no url. De qualquer forma, 
        # este tipo de presunção é extremamente perigoso, 
        # então abaixo segue o formato onde eles se encontram, 
        # numerado em (1)
        #
        
        # Tá gg
        item['level'] = response.xpath('//div[@class="persona_name persona_level"]//span[@class="friendPlayerLevelNum"]/text()').extract()
        
        # Tá gg
        item['description'] = response.xpath('//div[@class="profile_summary"]/text()').extract()
        
        # Tá gg
        item['real_name'] = response.xpath('//div[@class="header_real_name ellipsis"]/text()').extract()[0].strip()
        
        # Tá gg
        item['vac_ban'] = response.xpath('//div[@class="profile_ban_status"]/text()').extract()
            
        # Tá gg
        item['last_login'] = response.xpath('//div[@class="profile_in_game_name"]/text()').extract() #isto pega uma string completa do tipo: Última vez online: há 24 mins ou Dísponível
        
        # item['mainGroup'] = response.xpath('//dic[@class="profile_group profile_primary_group"]').extract() #isto pega a string abaixo em (2)
        
        # Tá gg já
        item['nationality'] = response.xpath('//img[@class="profile_flag"]').re('(?:countryflags/)(.+?)(.gif)')[0] #vem no formato escrito abaixo (3)
            
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