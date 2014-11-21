import mysql.connector
from mysql.connector import errorcode

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

cursor.execute(request)

for nome, mac, linux, windows, total in cursor:

    print nome
    print mac, linux, windows
    print total, "\n"

cursor.close()
db_conn.close()

print ("connection ended")