import math
from math import pi, radians, sin, cos, degrees
import mysql.connector
from mysql.connector import errorcode

size(1024, 1024)
stroke(0)
strokewidth(1)
nofill()

translate(512, 512)

beginpath(0, 0)
c = oval(-512, -512, 1024, 1024)
endpath(draw = False)

drawpath(c)
        
def createPath(ia, ea, pathName, tam):
    stroke(0)
    pi = (768 * cos(ia), 768 * sin(ia))
    pf = (768 * cos(ea), 768 * sin(ea))

    ma = ia + ((ea - ia) / 2)
    pm = (768 * cos(ma), 768 * sin(ma))
    
    pathArc = findpath([pi, pm, pf], 1)
    pathCone = findpath([pi, pf, (0, 0)], 0)
    
    path = c.intersect(pathArc.union(pathCone))
    drawpath(path)
    
    push()
    fill(0)
    font("Helvetica", tam / 8)
    align(CENTER)

    text(pathName, pm[0] / 2  - textmetrics(pathName, tam / 10)[0], pm[1] / 2 + textmetrics(pathName, tam / 10)[0])
    pop()

def drawGraph(winter, spring, summer, fall):
    total = float(winter + spring + summer + fall)
    aWinter = radians(winter / total * 360)
    aSpring = radians(spring / total * 360) + aWinter
    aSummer = radians(summer / total * 360) + aSpring
    
    angle = 0

    fill(0.94, .97, 1, 1)    
    createPath(0, aWinter, "Winter", winter)
    fill(1, .88, 1, 1)
    createPath(aWinter, aSpring, "Spring", spring)
    fill(1, 1, .05, 1)
    createPath(aSpring, aSummer, "Summer", summer)
    fill(.87, .46, .28, 1)
    createPath(aSummer, 2 * pi, "Fall", fall)
    
DB_NAME = 'steampunk'

# Get database connection
db_conn = mysql.connector.connect(user='root', password='vaporAranha', host='localhost', database='steampunk')
# Get cursor to perform operations on our database
cursor = db_conn.cursor()

request = ("SELECT "
	"(SELECT COUNT(software.release_date) FROM software "
		"WHERE software.release_date LIKE '%Jan%' OR '%Feb%' OR '%Mar%') AS Winter, "
	"(SELECT COUNT(software.release_date) FROM software "
		"WHERE software.release_date LIKE '%Apr%' OR '%May%' OR '%Jun%') AS Spring, "
	"(SELECT COUNT(software.release_date) FROM software "
		"WHERE software.release_date LIKE '%Jul%' OR '%Aug%' OR '%Sep%') AS Summer, "
	"(SELECT COUNT(software.release_date) FROM software "
		"WHERE software.release_date LIKE '%Oct%' OR '%Nov%' OR '%Dec%') AS Fall")

cursor.execute(request)

for winter, spring, summer, fall in cursor:
    drawGraph(winter, spring, summer, fall)

cursor.close()
db_conn.close()

print ("connection ended")