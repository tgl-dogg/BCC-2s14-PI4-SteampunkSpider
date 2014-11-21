import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'steampunk'

# Get database connection
db_conn = mysql.connector.connect(user='root', password='vaporAranha', host='localhost', database='steampunk')
# Get cursor to perform operations on our database
cursor = db_conn.cursor()

request = ("SELECT t1.name AS country, COUNT(rel_software_genre.fk_genre) AS ng, t2.name AS genero "
	"FROM (rel_player_software INNER JOIN software ON rel_player_software.fk_software = software.id_software) "
		"INNER JOIN rel_software_genre ON software.id_software = rel_software_genre.fk_software, "
	"(SELECT nationality.id_nationality, nationality.name "
		"FROM nationality INNER JOIN player ON nationality.id_nationality = player.fk_nationality "
		"GROUP BY nationality.id_nationality "
		"ORDER BY COUNT(player.id_player) DESC "
		"LIMIT 25) AS t1, "
	"(SELECT genre.id_genre, genre.name "
		"FROM (genre INNER JOIN rel_software_genre ON rel_software_genre.fk_genre = genre.id_genre) "
			"INNER JOIN rel_player_software ON rel_player_software.fk_software = rel_software_genre.fk_software "
		"GROUP BY genre.id_genre) AS t2, player "
	"WHERE rel_software_genre.fk_genre = t2.id_genre AND player.id_player = rel_player_software.fk_player "
		"AND t1.id_nationality = player.fk_nationality "
	"GROUP BY t1.name, t2.name "
	"ORDER BY country, ng DESC")

cursor.execute(request)

for country, ng, genero in cursor:

    print country
    print ng
    print genero, "\n"

cursor.close()
db_conn.close()

print ("connection ended")