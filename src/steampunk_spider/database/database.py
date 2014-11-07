import mysql.connector

print "try connection"
cnx = mysql.connector.connect(user='root', password='@TGL_Dogg', host='localhost')
cnx.close()
print "connection ended"
