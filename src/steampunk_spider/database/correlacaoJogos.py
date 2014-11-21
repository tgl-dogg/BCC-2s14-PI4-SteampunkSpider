import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'steampunk'

# Get database connection
db_conn = mysql.connector.connect(user='root', password='vaporAranha', host='localhost', database='steampunk')
# Get cursor to perform operations on our database
cursor = db_conn.cursor()

db_conn2 = mysql.connector.connect(user='root', password='vaporAranha', host='localhost', database='steampunk')
cursor2 = db_conn.cursor()

request = ("SELECT software.name AS nome, software.id_software AS id, COUNT(rel_player_software.fk_software) AS jogadores "
    "FROM software INNER JOIN rel_player_software ON software.id_software = rel_player_software.fk_software "
    "GROUP BY nome "
    "ORDER BY jogadores DESC "
    "LIMIT 10")

cursor.execute(request)

nomes = []
ids = []
players = []

for nome, id, jogadores in cursor:
    nomes.append(nome)
    ids.append(id)
    players.append(jogadores)

for x in range(10):
    for y in range(10):
        if x != y:
            xy = {
                'xid' : ids[x],
                'yid' : ids[y]
            }

            request2 = ("SELECT COUNT(j2.fk_player) AS ambos, qualquer.players AS qualquer, "
                "COUNT(j2.fk_player) / qualquer.players AS rel "
                "FROM (SELECT DISTINCT COUNT(rel_player_software.fk_player) AS players FROM rel_player_software "
                    "WHERE rel_player_software.fk_software = %(xid)s OR rel_player_software.fk_software = %(yid)s) AS qualquer, "
                    "(SELECT * FROM rel_player_software WHERE rel_player_software.fk_software = %(xid)s) AS j1 "
                    "INNER JOIN (SELECT * FROM rel_player_software WHERE rel_player_software.fk_software = %(yid)s) AS j2 "
                        "ON j1.fk_player = j2.fk_player")

            cursor2.execute(request2, xy)

            for ambos, qualquer, rel in cursor2:
                print nomes[x], nomes[y]
                print ambos, qualquer, rel

cursor.close()
db_conn.close()

print ("connection ended")