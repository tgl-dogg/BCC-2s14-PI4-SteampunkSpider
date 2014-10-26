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
            item['name'] = founds.xpath('//div[@class="persona_name"]').extract()
            item['idSteam'] = founds.xpath('//"]').extract()
            item['url'] = founds.xpath('//').extract()
            #   Os dois acima não sei de onde extrair, entretanto, eu tenho a ligeira impressão de que o teremos "antes", dado que acessamos o jogador pelo url dele, e o id pode sempre ser usado no url. De qualquer forma, este tipo de presunção é extremamente perigoso, então abaixo segue o formato onde eles se encontram, numerado em (1)
            #
            #
            item['level'] = founds.xpath('//span[@class="friendPlayerLevelNum"]').extract()
            item['description'] = founds.xpath('//div[@class="profile_summary"]').extract()
            item['realname'] = founds.xpath('//div[@class="header_real_name ellipsis"]').extract()
            item['vacBanCount'] = founds.xpath('//div[@class="profile_ban"]').extract()
            
            
            item['lastLogOut'] = founds.xpath('//div[@class="profile_in_game_name"]').extract() #isto pega uma string completa do tipo: Última vez online: há 24 mins ou Dísponível
            
            item['mainGroup'] = founds.xpath('//dic[@class="profile_group profile_primary_group"]').extract() #isto pega a string abaixo em (2)
            item['nacionalidade'] = founds.xpath('//img[@class="profile_flag"]').extract() #vem no formato escrito abaixo (3)
            print "item: "
            print item['name'] + item['idSteam'] + item['url'] + item['level'] + item['description'] + item['realname'] + item['lastLogOut'] + item['vacBanCount'] + item['mainGroup'] + item['nacionalidade']
            #yield item



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