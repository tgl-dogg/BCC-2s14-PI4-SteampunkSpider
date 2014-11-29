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
        
def createPath(ia, ea):
    stroke(0)
    pi = (768 * cos(ia), 768 * sin(ia))
    pf = (768 * cos(ea), 768 * sin(ea))
    
    pathCone = findpath([pi, pf, (0, 0)], 0)
    
    path = c.intersect(pathCone)
    drawpath(path)
    
    return pi, pf
    
def drawText(name, tam, p):
    fill(0)
    font("Helvetica", tam / 25)
    align(CENTER)
    text(name, p[0] - textwidth(name) / 2, p[1] + textheight(name) / 8)

def drawGraph(winter, spring, summer, fall):
    total = float(sum(winter) + sum(spring) + sum(summer) + sum(fall))

    stack = 0
    
    i = (0, 0)
    f = (0, 0)
    
    fill(0.94, .97, 1, 1)
    for month in winter:
        angle = radians(month / total * 360)
        pi, pf = createPath(stack, angle + stack)
        stack += angle
        
        if winter.index(month) == 0:
            i = pi
        if winter.index(month) == 2:
            f = pf
            
    p = ((i[0] + f[0]) / 4, (i[1] + f[1]) / 4)
    drawText("Winter", float(sum(winter)), p)
    
    
    fill(1, .88, 1, 1)
    for month in spring:
        angle = radians(month / total * 360)
        pi, pf = createPath(stack, angle + stack)
        stack += angle
        
        if spring.index(month) == 0:
            i = pi
        if spring.index(month) == 2:
            f = pf
            
    p = ((i[0] + f[0]) / 4, (i[1] + f[1]) / 4)
    drawText("Spring", float(sum(spring)), p)
        
        
    fill(1, 1, .05, 1)
    for month in summer:
        angle = radians(month / total * 360)
        pi, pf = createPath(stack, angle + stack)
        stack += angle
        
        if summer.index(month) == 0:
            i = pi
        if summer.index(month) == 2:
            f = pf
            
    p = ((i[0] + f[0]) / 4, (i[1] + f[1]) / 4)
    drawText("Summer", float(sum(summer)), p)
        
        
    fill(.87, .46, .28, 1)
    for month in fall:
        angle = radians(month / total * 360)
        pi, pf = createPath(stack, angle + stack)
        stack += angle
        
        if fall.index(month) == 0:
            i = pi
        if fall.index(month) == 2:
            f = pf
            
    p = ((i[0] + f[0]) / 4, (i[1] + f[1]) / 4)
    drawText("Fall", float(sum(fall)), p)
        
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