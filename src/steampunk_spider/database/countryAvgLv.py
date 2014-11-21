import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'steampunk'

# Get database connection
db_conn = mysql.connector.connect(user='root', password='vaporAranha', host='localhost', database='steampunk')
# Get cursor to perform operations on our database
cursor = db_conn.cursor()

request = ("SELECT nationality.name AS país, SUM(player.level) AS totalLv "
	"FROM nationality INNER JOIN player ON nationality.id_nationality = player.fk_nationality "
	"GROUP BY nationality.name "
	"ORDER BY totalLv DESC")

cursor.execute(request)

for country, totalLv in cursor:

    print country
    print totalLv, "\n"

cursor.close()
db_conn.close()

print ("connection ended")