import mysql.connector
from mysql.connector import errorcode

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

    print country, players, totalLv, totalPrice, "\n"

cursor.close()
db_conn.close()

print ("connection ended")