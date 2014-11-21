import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'steampunk'

# Get database connection
db_conn = mysql.connector.connect(user='root', password='vaporAranha', host='localhost', database='steampunk')
# Get cursor to perform operations on our database
cursor = db_conn.cursor()

request = ("SELECT nationality.name AS country, AVG(software.price) AS valorMedio, "
        "SUM(software.price) AS valorTotal, COUNT(rel_player_software.fk_player) AS nJogadores "
    "FROM((player INNER JOIN rel_player_software ON player.id_player = rel_player_software.fk_player) "
        "INNER JOIN software ON software.id_software = rel_player_software.fk_software) "
        "INNER JOIN nationality ON nationality.id_nationality = player.fk_nationality "
    "GROUP BY nationality.name "
    "ORDER BY valorMedio DESC")

cursor.execute(request)

for country, valorMedio, valorTotal, nJogadores in cursor:

    print country
    print valorMedio
    print valorTotal
    print nJogadores, "\n"

cursor.close()
db_conn.close()

print ("connection ended")