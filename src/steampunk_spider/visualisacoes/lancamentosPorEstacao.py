import math
from math import pi, radians, sin, cos, degrees
import mysql.connector
from mysql.connector import errorcode

size(2048, 2048)
stroke(0)
strokewidth(1)
nofill()

translate(1024, 1024)

beginpath(0, 0)
c = oval(-1024, -1024, 2048, 2048)
endpath(draw = False)

drawpath(c)

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
def createPath(ia, ea, index, tam):
    stroke(0)
    pi = (1152 * cos(ia), 1152 * sin(ia))
    pf = (1152 * cos(ea), 1152 * sin(ea))
    
    ma = ia + ((ea - ia) / 2)
    pm = (1152 * cos(ma), 1152 * sin(ma))
    
    pathCone = findpath([pi, pf, (0, 0)], 0)
    
    path = c.intersect(pathCone)
    drawpath(path)
    
    push()
    fill(0)
    font("Helvetica", tam / 3)
    align(CENTER)

    text(months[index], 2 * pm[0] / 3 - textwidth(months[index]) / 2, 2 * pm[1] / 3 + textheight(months[index]) / 4)
    pop()
    
    return pi, pf
    
def drawText(name, x, y, pct):
    name = "%s: %.2f %%" % (name, pct * 100)
    
    fill(0)
    font("Helvetica", pct * 200)
    align(CENTER)
    text(name, x - textwidth(name) / 2, y)

def drawGraph(winter, spring, summer, fall):
    total = float(sum(winter) + sum(spring) + sum(summer) + sum(fall))

    stack = 0
    
    i = (0, 0)
    f = (0, 0)
    
    n = 0
    for month in winter:
        fill(0.94, .97, 1, 1)
        angle = radians(month / total * 360)
        pi, pf = createPath(stack, angle + stack, n, month)
        stack += angle
        n += 1
            
    drawText("Winter", 800, 900, float(sum(winter)) / total)
    
    
    n = 0
    for month in spring:
        fill(1, .88, 1, 1)
        angle = radians(month / total * 360)
        pi, pf = createPath(stack, angle + stack, n + 3, month)
        stack += angle
        n += 1
            
    p = ((i[0] + f[0]) / 4, (i[1] + f[1]) / 4)
    drawText("Spring", -800, 900, float(sum(spring)) / total)
        
        
    n = 0
    for month in summer:
        fill(1, 1, .05, 1)
        angle = radians(month / total * 360)
        pi, pf = createPath(stack, angle + stack, n + 6, month)
        stack += angle
        n += 1
            
    p = ((i[0] + f[0]) / 4, (i[1] + f[1]) / 4)
    drawText("Summer", -800, -900, float(sum(summer)) / total)
        

    n = 0
    for month in fall:
        fill(.87, .46, .28, 1)
        angle = radians(month / total * 360)
        pi, pf = createPath(stack, angle + stack, n + 9, month)
        stack += angle
        n += 1
            
    p = ((i[0] + f[0]) / 4, (i[1] + f[1]) / 4)
    drawText("Fall", 800, -900, float(sum(fall)) / total)
        
DB_NAME = 'steampunk'

# Get database connection
db_conn = mysql.connector.connect(user='root', password='vaporAranha', host='localhost', database='steampunk')
# Get cursor to perform operations on our database
cursor = db_conn.cursor()

request = ("SELECT "
    "(SELECT COUNT(software.release_date) FROM software "
        "WHERE software.release_date LIKE '%Jan%') AS Jan, "
    "(SELECT COUNT(software.release_date) FROM software "
        "WHERE software.release_date LIKE '%Feb%') AS Feb, "
    "(SELECT COUNT(software.release_date) FROM software "
        "WHERE software.release_date LIKE '%Mar%') AS Mar, "
    "(SELECT COUNT(software.release_date) FROM software "
        "WHERE software.release_date LIKE '%Apr%') AS Apr, "
    "(SELECT COUNT(software.release_date) FROM software "
        "WHERE software.release_date LIKE '%May%') AS May, "
    "(SELECT COUNT(software.release_date) FROM software "
        "WHERE software.release_date LIKE '%Jun%') AS Jun, "
    "(SELECT COUNT(software.release_date) FROM software "
        "WHERE software.release_date LIKE '%Jul%') AS Jul, "
    "(SELECT COUNT(software.release_date) FROM software "
        "WHERE software.release_date LIKE '%Aug%') AS Aug, "
    "(SELECT COUNT(software.release_date) FROM software "
        "WHERE software.release_date LIKE '%Sep%') AS Sep, "
    "(SELECT COUNT(software.release_date) FROM software "
        "WHERE software.release_date LIKE '%Oct%') AS Oct, "
    "(SELECT COUNT(software.release_date) FROM software "
        "WHERE software.release_date LIKE '%Nov%') AS Nov, "
    "(SELECT COUNT(software.release_date) FROM software "
        "WHERE software.release_date LIKE '%Dec%') AS 'Dec'")

cursor.execute(request)

for Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec in cursor:
    winter = [Jan, Feb, Mar]
    spring = [Apr, May, Jun]
    summer = [Jul, Aug, Sep]
    fall = [Oct, Nov, Dec]
    drawGraph(winter, spring, summer, fall)

cursor.close()
db_conn.close()

print ("connection ended")