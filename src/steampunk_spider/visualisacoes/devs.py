import mysql.connector
from mysql.connector import errorcode
        
class VennCircle:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        
def drawNames(windows, mac, linux, name, tam):
    x = 0
    y = 0
    
    font("Helvetica", tam)
    
    fill(0.25, 0.25, 0.25, 0.8)
    
    if windows > 0.5 and not mac > 0.5 and not linux > 0.5:
        while True:
            x = random(WIDTH)
            y = random(HEIGHT)
            
            path = pathW.path.difference(pathL.path).difference(pathM.path)
            
            if path.contains(x, y):
                break
                
    elif mac > 0.5 and not windows > 0.5 and not linux > 0.5:
        while True:
            x = random(WIDTH)
            y = random(HEIGHT)
            
            path = pathM.path.difference(pathL.path).difference(pathW.path)
            
            if path.contains(x, y):
                break
                
    elif linux > 0.5 and not mac > 0.5 and not windows > 0.5:
        while True:
            x = random(WIDTH)
            y = random(HEIGHT)
            
            path = pathL.path.difference(pathL.path).difference(pathM.path)
            
            if path.contains(x, y):
                break
                
    elif windows > 0.5 and mac > 0.5 and not linux > 0.5:
        while True:
            x = random(WIDTH)
            y = random(HEIGHT)
            
            path = pathW.path.intersect(pathM.path).difference(pathL.path)
            
            if path.contains(x, y):
                break
                
    elif windows > 0.5 and not mac > 0.5 and linux > 0.5:
        while True:
            x = random(WIDTH)
            y = random(HEIGHT)
            
            path = pathW.path.intersect(pathL.path).difference(pathM.path)
            
            if path.contains(x, y):
                break
                
    elif linux > 0.5 and mac > 0.5 and not windows > 0.5:
        while True:
            x = random(WIDTH)
            y = random(HEIGHT)
            
            path = pathL.path.intersect(pathM.path).difference(pathW.path)
            
            if path.contains(x, y):
                break
                
    elif windows > 0.5 and linux > 0.5 and mac > 0.5:
        while True:
            x = random(WIDTH)
            y = random(HEIGHT)
            
            path = pathW.path.intersect(pathL.path).intersect(pathM.path)
            
            if path.contains(x, y):
                break
                
    else:
        return
                
    t = textpath(name, x, y)
    
    #for point in t:
    #    if not path.contains(point.x, point.y):
    #        print name
    #        return
            
    drawpath(t)


DB_NAME = 'steampunk'

# Get database connection
db_conn = mysql.connector.connect(user='root', password='vaporAranha', host='localhost', database='steampunk')
# Get cursor to perform operations on our database
cursor = db_conn.cursor()

request = ("SELECT developer.name AS nome, AVG(software.mac) AS mac, AVG(software.linux) AS linux, "
    "AVG(software.windows) AS windows, COUNT(software.id_software) AS total "
    "FROM (developer INNER JOIN rel_software_developer ON developer.id_developer = rel_software_developer.fk_developer) "
        "INNER JOIN software ON rel_software_developer.fk_software = software.id_software "
    "GROUP BY developer.name "
    "ORDER BY total DESC")

size(2048, 2048)

stroke(0, 0, 0, 1)
strokewidth(1)
    
fill(color(1, 0.5, 0.5, 0.5))
pathW = VennCircle('Windows', oval(400, 100, 1200, 1200))
    
fill(color(0.5, 1, 0.5, 0.5))
pathM = VennCircle('Mac', oval(400, 700, 800, 800))
    
fill(color(0.5, 0.5, 1, 0.5))
pathL = VennCircle('Linux', oval(800, 700, 800, 800))

cursor.execute(request)

for nome, mac, linux, windows, total in cursor:
    drawNames(windows, mac, linux, nome, total)

cursor.close()
db_conn.close()

print ("connection ended")