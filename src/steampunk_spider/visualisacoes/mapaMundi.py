from math import floor, modf
import mysql.connector
from mysql.connector import errorcode

imgMoney = "/Users/DaniloIkuta/Desktop/resources/money.png"
imgLv = "/Users/DaniloIkuta/Desktop/resources/steamLogo.png"

#def drawPlayers(x, y, players):

def drawLv(x, y, lv):
    resto, amt = modf(lv / 1000000)
    
    n = 0
    push()
    for i in range(0, int(amt)):
        image(imgLv, x, y)
        translate(32, 0)
        n += 1
        
        if n  >= 3:
            n = 0
            translate(-96, -32)
    
    nofill()
    nostroke()        
    r = rect(x, y, 32, 32 * resto)
    beginclip(r)
    image(imgLv, x, y)
    endclip()
    pop()
    
    stroke(0)
    fill(0)
    
def drawPrice(x, y, price):
    resto, amt = modf(price / 1000000)
    
    n = 0
    push()
    for i in range(0, int(amt)):
        image(imgMoney, x, y)
        translate(32, 0)
        n += 1
        
        if n  >= 3:
            n = 0
            translate(-96, 32)
    
    nofill()
    nostroke()        
    r = rect(x, y, 32, 32 * resto)
    beginclip(r)
    image(imgMoney, x, y)
    endclip()
    pop()
    
    stroke(0)
    fill(0)
    
def drawCountry(name, players, lv, price):
    x = y = 0
    if name == "us":
        x = 783
        y = 823
        
    elif name == "gb":
        x = 1858
        y = 657
        
    elif name == "ru":
        x = 2867
        y = 476
        
    elif name == "ca":
        x = 888
        y = 545
        
    elif name == "de":
        x = 2000
        y = 750
        
    elif name == "au":
        x = 3415
        y = 1795
        
    elif name == "se":
        x = 2056
        y = 532
        
    elif name == "br":
        x = 1285
        y = 1583
        
    elif name == "pl":
        x = 2088
        y = 718
        
    elif name == "fr":
        x = 1918
        y = 811
        
    font("Helvetica", 25)
    text(name, x - textwidth(name) / 2, y + textheight(name) / 4)
    
    drawPrice(x - textwidth(name) / 2, y + textheight(name) / 4, price)
    drawLv(x - textwidth(name) / 2, y - textheight(name) / 4 - 32, lv)

size(3958, 2596)
image("/Users/DaniloIkuta/Desktop/resources/worldmap.png", 0, 0)

DB_NAME = 'steampunk'

# Get database connection
db_conn = mysql.connector.connect(user='root', password='vaporAranha', host='localhost', database='steampunk')
# Get cursor to perform operations on our database
cursor = db_conn.cursor()

request = ("SELECT nationality.name AS country, COUNT(player.id_player) AS players, "
	"SUM(software.price) AS totalPrice, SUM(player.level) AS totalLv FROM "
		"((nationality INNER JOIN player ON nationality.id_nationality = player.fk_nationality) "
		"INNER JOIN rel_player_software ON player.id_player = rel_player_software.fk_player) "
        "INNER JOIN software ON software.id_software = rel_player_software.fk_software "
    "WHERE nationality.name NOT LIKE '00'"
    "GROUP BY nationality.name "
	"ORDER BY players DESC "
	"LIMIT 10")

cursor.execute(request)

for country, players, totalLv, totalPrice in cursor:
    drawCountry(country, players, totalLv, totalPrice)

cursor.close()
db_conn.close()

print ("connection ended")