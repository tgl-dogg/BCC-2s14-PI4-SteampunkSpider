# # -*- coding: utf-8 -*-
# from __future__ import print_function

# import mysql.connector
# from mysql.connector import errorcode

# from crawler import my_utils as utils
# from crawler.items import StoreItem

# import scrapy

# from scrapy import signals
# from scrapy.xlib.pydispatch import dispatcher
# from scrapy.contrib.spiders import CrawlSpider, Rule
# from scrapy.contrib.linkextractors import LinkExtractor
# from scrapy.selector import Selector
# from scrapy.http import Request, FormRequest

# import re

# # definir um update maroto

# def insert_software(db_conn, db_cursor, software):
#     add_software = ("INSERT INTO software "
#               "(id_software, url, name, price, description, linux, mac, windows, release_date, hdd_space) "
#               "VALUES (%(id_software)s, %(url)s, %(name)s, %(price)s, %(description)s, %(linux)s, %(mac)s, %(windows)s, %(release_date)s, %(hdd_space)s)")

#     data_software = {
#         'id_software': software['id_software'],
#         'url': software['url'],
#         'name': software['name'],
#         'price': software['price'],
#         'description': software['description'],
#         'linux': software['linux'],
#         'mac': software['mac'],
#         'windows': software['windows'],
#         'release_date': software['release_date'],
#         'hdd_space': software['hdd_space'],
#     }

#     # print (add_software)
#     # print (data_software)

#     db_cursor.execute(add_software, data_software)
#     db_conn.commit()

# def insert_genre(db_conn, db_cursor, genre):
#     # MySQL escapes \' with another '
#     genre = genre.replace("'", "''")

#     exist_check = ("SELECT id_genre FROM genre WHERE name LIKE \'%s\'" % genre)
#     db_cursor.execute(exist_check)
        
#     data_exists = db_cursor.fetchone()
#     if data_exists:
#         id_genre = data_exists[0]
#     else:
#         insert = ("INSERT INTO genre "
#                 "(name) "
#                 "VALUES ('%s')" % genre)

#         db_cursor.execute(insert)
#         db_conn.commit()

#         id_genre = db_cursor.lastrowid
    
#     return id_genre

# def insert_tag(db_conn, db_cursor, tag):
#     tag = tag.replace("'", "''")

#     exist_check = ("SELECT id_tag FROM tag WHERE name LIKE \'%s\'" % tag)
#     db_cursor.execute(exist_check)

#     data_exists = db_cursor.fetchone()
#     if data_exists:
#         id_tag = data_exists[0]
#     else:
#         insert = ("INSERT INTO tag "
#                 "(name) "
#                 "VALUES ('%s')" % tag)

#         db_cursor.execute(insert)
#         db_conn.commit()

#         id_tag = db_cursor.lastrowid

#     return id_tag

# def insert_developer(db_conn, db_cursor, developer):
#     developer = developer.replace("'", "''")

#     exist_check = ("SELECT id_developer FROM developer WHERE name LIKE \'%s\'" % developer)
#     db_cursor.execute(exist_check)

#     data_exists = db_cursor.fetchone()
#     if data_exists:
#         id_dev = data_exists[0]
#     else:
#         insert = ("INSERT INTO developer "
#               "(name) "
#               "VALUES ('%s')" % developer)

#         db_cursor.execute(insert)
#         db_conn.commit()

#         id_dev = db_cursor.lastrowid
   
#     return id_dev

# def insert_rel_software_genre(db_conn, db_cursor, id_software, id_genre):
#     add_rel = ("INSERT INTO rel_software_genre "
#               "(fk_genre, fk_software) "
#               "VALUES (%s, %s)" % (id_genre, id_software))

#     db_cursor.execute(add_rel)
#     db_conn.commit()

# def insert_rel_software_tag(db_conn, db_cursor, id_software, id_tag):
#     add_rel = ("INSERT INTO rel_software_tag "
#                 "(fk_tag, fk_software) "
#                 "VALUES (%s, %s)" % (id_tag, id_software))

#     db_cursor.execute(add_rel)
#     db_conn.commit()

# def insert_rel_software_developer(db_conn, db_cursor, id_software, id_developer):
#     add_rel = ("INSERT INTO rel_software_developer "
#               "(fk_developer, fk_software) "
#               "VALUES (%s, %s)" % (id_developer, id_software))

#     db_cursor.execute(add_rel)
#     db_conn.commit()

# def parse_storeitem(self, response, db_conn, db_cursor):
#     url = response.url

#     # no name, no game    
#     name_list = response.xpath('//div[@class="apphub_AppName"]/text()').extract()
#     name = name_list[0].encode('utf-8')
#     if (not name):
#         return

#     id_software = 0
#     id_regex = re.compile('([0-9]{1,})')
#     id_search = re.search(id_regex, str(url))
#     id_software = int(id_search.groups(0)[0])    

#     # Checar se o item já existe é uma boa.
#     # check_software_item = ("SELECT COUNT(1) FROM software WHERE id_software=%s" % id_software) 
#     # db_cursor.execute(check_software_item)    
#     # if db_cursor.fetchone()[0]:
#     #     return

#     mac = utils.os_validator(response.xpath('//div[contains(@data-os, "mac")]').extract())
#     lin = utils.os_validator(response.xpath('//div[contains(@data-os, "lin")]').extract())
#     win = utils.os_validator(response.xpath('//div[contains(@data-os, "win")]').extract())
#     price = utils.price_validator(response.xpath('//meta[@itemprop="price"]/@content').extract())
#     description = utils.description_validator(response.xpath('//div[@id="game_area_description"]//text()').extract())

#     release_date = ""
#     release = response.xpath('//span[@class="date"]/text()').extract()
#     if (release):
#         release_date = str(release[0])

#     size = 0.0
#     size_str = utils.whitespace_remover(response.xpath('substring-after(//div[@class="sysreq_contents"], "Hard Drive:")').extract()[0].upper())
#     game_size = re.compile('([0-9]{1,})(MB|GB)')
#     src_size = re.search(game_size, size_str)

#     if (src_size):
#         size = float(str(src_size.groups(0)[0]))

#         if (str(src_size.groups(0)[1]) == "GB"):
#             size *= 1024

#     item = StoreItem()
#     item['url'] = url    
#     item['id_software'] = id_software
#     item['name'] = name
#     item['price'] = price
#     item['description'] = description
#     item['mac'] = mac
#     item['linux'] = lin
#     item['windows'] = win
#     item['release_date'] = release_date
#     item['hdd_space'] = size

#     # Insere informações de desenvolvedor, tag e gênero
#     developers = response.xpath('//div[@class="details_block"]/a[contains(@href, "http://store.steampowered.com/search/?developer")]/text()')
#     dev_ids = []
#     for dev in developers:
#         dev_ids.append(insert_developer(db_conn, db_cursor, dev.extract().strip()))

#     tag_ids = []
#     tags = response.xpath('//div[@class="glance_tags popular_tags"]/a[contains(@href, "http://store.steampowered.com/tag")]/text()')
#     for tag in tags:
#         tag_ids.append(insert_tag(db_conn, db_cursor, tag.extract().strip()))

#     genre_ids = []
#     genres = response.xpath('//div[@class="details_block"]/a[contains(@href, "http://store.steampowered.com/genre")]/text()')
#     for genre in genres:         
#         genre_ids.append(insert_genre(db_conn, db_cursor, genre.extract().strip()))

#     # Insere o jogo
#     insert_software(db_conn, db_cursor, item)

#     # Insere as relações do jogo
#     for id_genre in genre_ids:
#         insert_rel_software_genre(db_conn, db_cursor, id_software, id_genre)

#     for id_tag in tag_ids:
#         insert_rel_software_tag(db_conn, db_cursor, id_software, id_tag)

#     for id_dev in dev_ids:
#         insert_rel_software_developer(db_conn, db_cursor, id_software, id_dev)

#     return item
  
# # scrapy crawl spider -o steam.json
# # scrapy crawl somespider -s JOBDIR=crawls/somespider-1

# #old_widow
# #@TGL_Doggbatata23

# # fazer a parte de fórum (posts)

# class StoreSpider(CrawlSpider):
#     global db_conn
#     global db_cursor

#     name = "storespider"
#     allowed_domains = ["store.steampowered.com"]
#     start_urls = [
#         "http://store.steampowered.com/",
#         "http://store.steampowered.com/app/242700/",
#         "http://store.steampowered.com/app/209000"
#         "http://store.steampowered.com/app/730/",
#         "http://store.steampowered.com/app/321080/",
#         "http://store.steampowered.com/app/258817",
#         "http://store.steampowered.com/app/218620/",
#         "http://store.steampowered.com/app/265590",
#         "http://store.steampowered.com/app/222880",
#     ]

#     # Adicionar tolerância por gênero e tags para crawling
#     # http://store.steampowered.com/tag/en/Action/#os%5B%5D=linux&p=0&tab=NewReleases

#     # Tolerância pra essa url que é das da hora:
#     # http://store.steampowered.com/search/?developer=Level%20Up%20Labs%2C%20LLC

#     rules = (
#         Rule(
#             LinkExtractor(
#                 #recommended/morelike/app/[0-9]{1,}'
#                 allow=('app/[0-9]{1,}', 'store.steampowered.com/(tag|genre|search)'),
#                 deny=('\?l', 'facebook', 'twitter', 'login', 'reddit'),      
#             ),
            
#             callback='parse_items',
#             process_links='link_processor', 
#             process_request='request_processor',
#             follow=True
#         ), 
#     )

#     search_url = re.compile('store.steampowered.com/(tag|genre|search)')
#     software_url = re.compile('store.steampowered.com/app/[0-9]{1,}')
#     recommended_url = re.compile('(.+?)/recommended')
#     agecheck_url = re.compile('store.steampowered.com/agecheck/app/[0-9]{1,}')

#     print ("open database")
#     db_conn = mysql.connector.connect(user='root', password='@TGL_Dogg', host='localhost', database='steampunk')
#     db_cursor = db_conn.cursor()

#     # Fecha conexão com o banco após limpar
#     def spider_ended(spider):
#         db_conn.close()
#         db_cursor.close()
#         print ("close database")

#     dispatcher.connect(spider_ended, signals.spider_closed)

#     # Parser principal, vai decidir como vamos parsear os itens que recebemos
#     def parse_items(self, response):
#         is_recommended_url = re.search(self.recommended_url, response.url) != None
#         is_software_url = re.search(self.software_url, response.url) != None
#         is_search_url = re.search(self.search_url, response.url) != None
        
#         # São urls com listagem de jogos, não parseamos elas, apenas visitamos para pegar mais jogos.
#         if (is_recommended_url or is_search_url):
#             return

#         if (is_software_url):
#             yield parse_storeitem(self, response, db_conn, db_cursor)      


#     # Edita as urls antes de crawlear
#     def link_processor(self, links):
#         for link in links:
#             url = link.url

#             is_software_url = re.search(self.software_url, url) != None
#             is_recommended_url = re.search(self.recommended_url, url) != None

#             # Remove o "?snr=" e outras sujeiras dos links da loja
#             if (is_software_url or is_recommended_url):
#                 # store.steampowered.com/app/730/?snr=1_5_9__305
#                 # store.steampowered.com/recommended/morelike/app/730/?snr=blablabla
#                 # store.steampowered.com/app/100410/www.nevercenter.com/www.nevercenter.com/www.nevercenter.com/www.nevercenter.com/www.nevercenter.com/www.nevercenter.com/www.nevercenter.com/www.nevercenter.com/camerabag
#                 snr_url = re.compile('(.+?)app/[0-9]{1,}')
#                 results = re.search(snr_url, url)

#                 # Garante que não veio nada vazio
#                 if results:
#                     link.url = results.group(0)        
        
#         return links

#     # Faz um bypass nos jogos que tem restrição de idade
#     # PS: juro que todos os membros do grupo são maiores de 18
#     def request_processor(self, request):
#         is_agecheck_url = re.search(self.agecheck_url, request.url) != None        
        
#         if (is_agecheck_url):
#             return FormRequest(
#                     url=request.url,
#                     formdata={'ageDay': "1", 'ageMonth': "1", "ageYear" : "1995"},
#                     callback=self.parse_items)
#         else:
#             return request