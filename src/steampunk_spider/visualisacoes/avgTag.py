import mysql.connector
from mysql.connector import errorcode

font("Helvetica", 20)
align(CENTER)

def drawTexts(name, tam):
    translate(153, 0)
    
    fill(0, 0, 0, 1)
    text(name, -153, 942, 153)
    
    push()
    translate(0, HEIGHT - tam - 120)
    font("Helvetica", 18)
    s = "US$: %f" % (tam / 4)
    text(s, -153, 0, 153)
    pop()
    

def drawBars(name, tam):
    fill(random(), random(), random(), 1)
    rect(0, 922 - tam, 153, tam)
    
    drawTexts(name, tam)
    
def drawBuildings(name, tam):
    push()
    
    sh = tam / imagesize("/Users/DaniloIkuta/Desktop/resources/building.png").height
    
    scale(1, sh)
    
    image("/Users/DaniloIkuta/Desktop/resources/building.png", 0, 
        2 * tam / sh - (imagesize("/Users/DaniloIkuta/Desktop/resources/building.png").height / 2 *sh) + 190)
    pop()
    
    drawTexts(name, tam)

size(918, 1024)

stroke(0, 0, 0, 1)
strokewidth(1)

DB_NAME = 'steampunk'

# Get database connection
db_conn = mysql.connector.connect(user='root', password='vaporAranha', host='localhost', database='steampunk')
# Get cursor to perform operations on our database
cursor = db_conn.cursor()

request = ("SELECT tag.name AS nomeTag, AVG(software.price) AS precoMedio "
    "FROM (tag INNER JOIN rel_software_tag ON tag.id_tag = rel_software_tag.fk_tag) "
        "INNER JOIN software ON software.id_software = rel_software_tag.fk_software "
    "GROUP BY tag.name "
    "ORDER BY AVG(software.price) DESC")

cursor.execute(request)

i = 0
for nomeTag, precoMedio in cursor:
    if i < 3:
        drawBuildings(nomeTag, float(precoMedio * 4))
        
    elif nomeTag == "Free to Play" or nomeTag == "Lore-Rich" or nomeTag == "Wargame":
        drawBars(nomeTag, precoMedio * 4)
    i += 1
    
cursor.close()
db_conn.close()

print ("connection ended")

