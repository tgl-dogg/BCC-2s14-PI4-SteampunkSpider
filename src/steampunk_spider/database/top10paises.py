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

request2 = ("SELECT COUNT(bcc.id_player) AS players, SUM(bcc.level) AS totalLv, SUM(software.price) AS totalPrice "
	"FROM (SELECT player.id_player, player.level, rel_player_software.fk_software FROM player "
				"INNER JOIN rel_player_software ON player.id_player = rel_player_software.fk_player "
			"WHERE player.bcc = 1 "
			"GROUP BY player.id_player) AS bcc "
		"INNER JOIN software ON software.id_software = bcc.fk_software")

cursor.execute(request2)

for players, totalLv, totalPrice in cursor:
	print "BCC", players, totalLv, totalPrice

cursor.close()
db_conn.close()

print ("connection ended")