import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'steampunk'

# Get database connection
db_conn = mysql.connector.connect(user='root', password='vaporAranha', host='localhost', database='steampunk')
# Get cursor to perform operations on our database
cursor = db_conn.cursor()

db_conn2 = mysql.connector.connect(user='root', password='vaporAranha', host='localhost', database='steampunk')
cursor2 = db_conn2.cursor()

request = ("SELECT nationality.name AS country, nationality.id_nationality AS id_nat "
        "FROM nationality INNER JOIN player ON nationality.id_nationality = player.fk_nationality "
        "GROUP BY nationality.name "
        "ORDER BY COUNT(player.id_player) DESC "
        "LIMIT 10")

cursor.execute(request)

for country, id_nat in cursor:
    countryRequest = ("SELECT t1.name AS jogo, t1.players AS players "
        "FROM (SELECT software.name, COUNT(rel_player_software.fk_player) AS players, player.fk_nationality AS id_nat "
            "FROM (software INNER JOIN rel_player_software ON software.id_software = rel_player_software.fk_software) "
                "INNER JOIN player ON rel_player_software.fk_player = player.id_player "
            "GROUP BY software.name, player.fk_nationality "
            "ORDER BY COUNT(rel_player_software.fk_player) DESC) AS t1 "
        "WHERE t1.id_nat = %(id_nat)s "
        "LIMIT 10")

    data = {
        'id_nat' : id_nat,
        'country' : country
    }

    cursor2.execute(countryRequest, data)

    for jogo, players in cursor2:
        print country
        print jogo
        print players, "\n"

cursor.close()
cursor2.close()
db_conn.close()
db_conn2.close()

print ("connection ended")