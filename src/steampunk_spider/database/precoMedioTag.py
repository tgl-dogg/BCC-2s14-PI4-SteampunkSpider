import mysql.connector
from mysql.connector import errorcode

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

for nomeTag, precoMedio in cursor:

    print nomeTag
    print precoMedio, "\n"

cursor.close()
db_conn.close()

print ("connection ended")