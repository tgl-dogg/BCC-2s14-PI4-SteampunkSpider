# -*- coding: utf-8 -*-
import scrapy

from crawler.items import StoreItem

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest

from crawler import my_utils as utils

import re

class StoreSpider(CrawlSpider):
    name = "storespider"
    allowed_domains = ["store.steampowered.com"]
    start_urls = [
        #"http://store.steampowered.com/",
        #"http://store.steampowered.com/app/242700/",
        "http://store.steampowered.com/app/730/",
        # "http://store.steampowered.com/app/265590",
        # "http://store.steampowered.com/app/222880"
    ]
    rules = (
        Rule(
            LinkExtractor(
                #recommended/morelike/app/[0-9]{1,}'
                allow=('app/[0-9]{1,}'),
                deny=('\?l', 'facebook', 'twitter', 'login', 'reddit'),      
            ),
            
            callback='parse_items',
            process_links='link_processor', 
            # process_request='request_processor',
            follow=True
        ), 
    )

    software_url = re.compile('store.steampowered.com/app/[0-9]{1,}')
    recommended_url = re.compile('(.+?)/recommended')
    agecheck_url = re.compile('store.steampowered.com/agecheck/app/[0-9]{1,}')

    # Adicionar tolerância por gênero e tags para crawling
    
    # Edita as urls antes de crawlear
    def link_processor(self, links):
        for link in links:
            url = link.url

            is_software_url = re.search(self.software_url, url) != None
            is_recommended_url = re.search(self.recommended_url, url) != None

            # Remove o "?snr=" e outras sujeiras dos links da loja
            if (is_software_url or is_recommended_url):
                # store.steampowered.com/app/730/?snr=1_5_9__305
                # store.steampowered.com/recommended/morelike/app/730/?snr=blablabla
                # store.steampowered.com/app/100410/www.nevercenter.com/www.nevercenter.com/www.nevercenter.com/www.nevercenter.com/www.nevercenter.com/www.nevercenter.com/www.nevercenter.com/www.nevercenter.com/camerabag
                snr_url = re.compile('(.+?)app/[0-9]{1,}')
                results = re.search(snr_url, url)

                # Checa se a url realmente era de um item da loja
                if results:
                    # print results.group(0)
                    link.url = results.group(0)
        
        return links

    # def request_processor(self, request):
    #     is_agecheck_url = re.search(self.agecheck_url, request.url) != None        
        
    #     if (is_agecheck_url):
    #         return FormRequest(
    #                 url=request.url,
    #                 formdata={'ageDay': "1", 'ageMonth': "1", "ageYear" : "1995"},
    #                 callback=self.parse_items)
    #     else:     
    #         request.callback=self.parse_items
    #         return request

    def parse_items(self, response):
        is_recommended_url = re.search(self.recommended_url, response.url) != None
        
        # São urls com listagem de jogos, não parseamos elas, apenas visitamos para pegar mais jogos.
        if (is_recommended_url):
            return

        item = StoreItem()
        item['url'] = response.url
        
        # TODO checar se está vazio, se estiver não é um jogo.
        item['name'] = response.xpath('//div[@class="apphub_AppName"]/text()').extract()
        
        # TODO alterar valor null para 0,00
        item['price'] = utils.empty_validator(response.xpath('//meta[@itemprop="price"]/@content').extract())
        
        # Descrição está GG, se estiver comentado é para retirar a poluição do terminal.
        item['description'] = response.xpath('//div[@id="game_area_description"]/text()').extract()

        # Isso aqui tá funcionando que é uma belezinha
        item['mac'] = utils.os_validator(response.xpath('//div[contains(@data-os, "mac")]').extract())
        item['linux'] = utils.os_validator(response.xpath('//div[contains(@data-os, "lin")]').extract())
        item['windows'] = utils.os_validator(response.xpath('//div[contains(@data-os, "win")]').extract())

        # Release date está GG lek!
        item['release'] = response.xpath('//span[@class="date"]/text()').extract()
        
        # Não está completamente GG. Tratar o que vem do size pra pegar só o número (substring-before GB ou MB). Fica comentado por enquanto.
        # item['size'] = utils.empty_validator(response.xpath('substring-before(substring-after(//div[@class="sysreq_contents"], "Hard Drive"), " space")').extract())

        # Developer está GG lek!
        item['developer'] = response.xpath('//div[@class="details_block"]/a[contains(@href, "http://store.steampowered.com/search/?developer")]/text()').extract()

        # lembra que na definição de StoreItem tava escrito que esses são da zoeira? Então ;). 
        # Tags estão mais GG que nunca!
        item['tags'] = []
        tags = response.xpath('//div[@class="glance_tags popular_tags"]/a[contains(@href, "http://store.steampowered.com/tag")]/text()')
        for tag in tags:
            item['tags'].append(utils.whitespace_remover(tag.extract()))

        # Gêneros: ultra GG!
        item['genre'] = []
        genres = response.xpath('//div[@class="details_block"]/a[contains(@href, "http://store.steampowered.com/genre")]/text()')
        for genre in genres:         
            item['genre'].append(utils.whitespace_remover(genre.extract()))
        
        yield item

# Urls que ainda são problemáticas:
# http://store.steampowered.com/
# http://store.steampowered.com/agecheck/app/205930/

#old_widow
#@TGL_Doggbatata23

#doAgeGateSubmit(); return false;

# pegar todos os dados da store certinho
# fazer a parte de jogadores
# fazer a parte de fórum (posts)