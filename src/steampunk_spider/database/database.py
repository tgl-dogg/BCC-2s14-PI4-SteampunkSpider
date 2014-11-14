# -*- coding: utf-8 -*-
from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'steampunk'

# Creates database if it doesn't exists yet
def create_database(cursor):
    try:
    	# utf-8 4life <3
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8' DEFAULT COLLATE utf8_general_ci".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


# Let the nightmare begin
TABLES = {}
##

TABLES['nationality'] = (
    "CREATE TABLE IF NOT EXISTS `nationality` ("
    "  `id_nationality` int(5) NOT NULL AUTO_INCREMENT,"
    "  `name` char(2),"
    "  PRIMARY KEY (`id_nationality`),"
    "  UNIQUE INDEX (`name`)"
    ") ENGINE=InnoDB")

TABLES['developer'] = (
    "CREATE TABLE IF NOT EXISTS `developer` ("
    "  `id_developer` int(5) NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(50) NOT NULL,"
    "  PRIMARY KEY (`id_developer`),"
    "  UNIQUE INDEX (`name`)"
    ") ENGINE=InnoDB")

TABLES['genre'] = (
    "CREATE TABLE IF NOT EXISTS `genre` ("
    "  `id_genre` int(5) NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(50) NOT NULL,"
    "  PRIMARY KEY (`id_genre`),"
    "  UNIQUE INDEX (`name`)"
    ") ENGINE=InnoDB")

TABLES['tag'] = (
    "CREATE TABLE IF NOT EXISTS `tag` ("
    "  `id_tag` int(5) NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(50) NOT NULL,"
    "  PRIMARY KEY (`id_tag`),"
    "  UNIQUE INDEX (`name`)"
    ") ENGINE=InnoDB")

TABLES['player'] = (
    "CREATE TABLE IF NOT EXISTS `player` ("
    "  `id_player` bigint(64) NOT NULL AUTO_INCREMENT," # vamos usar o steamid    
    "  `id_steam` varchar(30) NOT NULL," # vamos usar o steamid
    "  `url` varchar(100) NOT NULL,"
    "  `real_name` varchar(200),"
    "  `username` varchar(200),"
    "  `description` varchar(20000),"
    "  `level` int(5),"
    "  `last_login` varchar(100),"
    "  `vac_ban` tinyint(1),"
    "  `public` tinyint(1),"
    "  `bcc` tinyint(1),"    
    "  `fk_nationality` int(5),"
    "  PRIMARY KEY (`id_player`),"
    "  FOREIGN KEY (`fk_nationality`) REFERENCES `nationality`(`id_nationality`),"
    "  UNIQUE INDEX (`id_steam`),"
    "  UNIQUE INDEX (`url`),"
    "  INDEX (`username`),"
    "  INDEX (`real_name`),"
    "  INDEX (`vac_ban`),"
    "  INDEX (`public`),"    
    "  INDEX (`bcc`),"    
    "  INDEX (`fk_nationality`)"
    ") ENGINE=InnoDB")

TABLES['software'] = (
    "CREATE TABLE IF NOT EXISTS `software` ("
    "  `id_software` int(16) NOT NULL," # vamos usar o da steam também
    "  `url` varchar(100) NOT NULL,"
    "  `name` varchar(100) NOT NULL,"
    "  `price` numeric(7,2),"
    "  `description` varchar(20000),"
    "  `linux` tinyint(1),"
    "  `mac` tinyint(1),"
    "  `windows` tinyint(1),"
    "  `release_date` varchar(30),"
    "  `hdd_space` numeric(10,2),"
    "  PRIMARY KEY (`id_software`),"
    "  UNIQUE INDEX (`url`),"
    "  INDEX (`name`),"
    "  INDEX (`price`),"
    "  INDEX (`release_date`),"
    "  INDEX (`hdd_space`)"
    ") ENGINE=InnoDB")

# TABLES['post'] = (
#     "CREATE TABLE IF NOT EXISTS `post` ("
#     "  `id_post` int(10) NOT NULL AUTO_INCREMENT,"
#     "  `title` varchar(100) NOT NULL,"
#     "  `body` varchar(4000) NOT NULL,"
#     "  `fk_player` bigint(64) NOT NULL,"
#     "  `fk_software` int(16) NOT NULL,"
#     "  PRIMARY KEY (`id_post`),"
#     "  FOREIGN KEY (`fk_player`) REFERENCES `player`(`id_player`),"
#     "  FOREIGN KEY (`fk_software`) REFERENCES `software`(`id_software`)"
#     ") ENGINE=InnoDB")

# amigos
TABLES['rel_player_player'] = (
    "CREATE TABLE IF NOT EXISTS `rel_player_player` ("
    "  `fk_player1` bigint(64) NOT NULL,"
    "  `fk_player2` bigint(64) NOT NULL,"
    "  PRIMARY KEY (`fk_player1`, `fk_player2`),"
    "  FOREIGN KEY (`fk_player1`) REFERENCES `player`(`id_player`),"
    "  FOREIGN KEY (`fk_player2`) REFERENCES `player`(`id_player`)"
    ") ENGINE=InnoDB")

TABLES['rel_player_software'] = (
    "CREATE TABLE IF NOT EXISTS `rel_player_software` ("
    "  `fk_player` bigint(64) NOT NULL,"
    "  `fk_software` int(16) NOT NULL,"
    "  `hours` numeric(10,4),"
    "  PRIMARY KEY (`fk_player`, `fk_software`),"
    "  FOREIGN KEY (`fk_player`) REFERENCES `player`(`id_player`),"
    "  FOREIGN KEY (`fk_software`) REFERENCES `software`(`id_software`),"
    "  INDEX (`hours`)"
    ") ENGINE=InnoDB")

TABLES['rel_software_tag'] = (
    "CREATE TABLE IF NOT EXISTS `rel_software_tag` ("
    "  `fk_tag` int(5) NOT NULL,"
    "  `fk_software` int(16) NOT NULL,"
    "  PRIMARY KEY (`fk_tag`, `fk_software`),"
    "  FOREIGN KEY (`fk_tag`) REFERENCES `tag`(`id_tag`),"
    "  FOREIGN KEY (`fk_software`) REFERENCES `software`(`id_software`)"
    ") ENGINE=InnoDB")

TABLES['rel_software_genre'] = (
    "CREATE TABLE IF NOT EXISTS `rel_software_genre` ("
    "  `fk_genre` int(5) NOT NULL,"
    "  `fk_software` int(16) NOT NULL,"
    "  PRIMARY KEY (`fk_genre`, `fk_software`),"
    "  FOREIGN KEY (`fk_genre`) REFERENCES `genre`(`id_genre`),"
    "  FOREIGN KEY (`fk_software`) REFERENCES `software`(`id_software`)"
    ") ENGINE=InnoDB")

TABLES['rel_software_developer'] = (
    "CREATE TABLE IF NOT EXISTS `rel_software_developer` ("
    "  `fk_developer` int(5) NOT NULL,"
    "  `fk_software` int(16) NOT NULL,"
    "  PRIMARY KEY (`fk_developer`, `fk_software`),"
    "  FOREIGN KEY (`fk_developer`) REFERENCES `developer`(`id_developer`),"
    "  FOREIGN KEY (`fk_software`) REFERENCES `software`(`id_software`)"
    ") ENGINE=InnoDB")

print ("try connection")

# Get database connection
db_conn = mysql.connector.connect(user='root', password='@TGL_Dogg', host='localhost')
# Get cursor to perform operations on our database
cursor = db_conn.cursor()

try:
    db_conn.database = DB_NAME    
except mysql.connector.Error as err:
	# Database doesn't exists yet, let's create it
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        db_conn.database = DB_NAME
    else:
        print(err)
        exit(1)

for name, ddl in TABLES.iteritems():
    try:
        print("Creating table {}: ".format(name), end='')
        cursor.execute(ddl)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            
            print(err.msg)
    else:
        print("OK")

cursor.close()
db_conn.close()

print ("connection ended")