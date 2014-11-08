from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'steampunk'

# Creates database if it doesn't exists yet
def create_database(cursor):
    try:
    	# utf-8 4life <3
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


# Let the nightmare begin
TABLES = {}
##

# referenciar nacionalidade
TABLES['jogador'] = (
    "CREATE TABLE `jogador` ("
    "  `idSteam` int(11) NOT NULL AUTO_INCREMENT,"
    "  `url` int NOT NULL,"
    "  `username` varchar(11) NOT NULL,"
    "  `description` varchar(4000),"
    "  `realName` varchar(11),"
    "  `level` int(11),"
    "  `lastLogOut` datetime,"
    "  `vacBanCount` int(11),"
    "  `mainGroup` int(11),"
    "  PRIMARY KEY (`idSteam`)"
    ") ENGINE=InnoDB")

TABLES['nacionalidade'] = (
    "CREATE TABLE `nacionalidade ` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(11),"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

# referenciar jogador líder
# pegar nome do grupo
# fazer tabela jogador-grupo
TABLES['grupo'] = (
    "CREATE TABLE `grupo` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `adm` int(35) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['software'] = (
    "CREATE TABLE `software` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(35) NOT NULL,"
    "  `price` int(11) NOT NULL,"
    "  `description` varchar(4000) NOT NULL,"
    "  `linux` tinyint(1) NOT NULL,"
    "  `mac` tinyint(1) NOT NULL,"
    "  `windows` tinyint(1) NOT NULL,"
    "  `release_date` date NOT NULL,"
    "  `game_specs` varchar(200),"
    "  `size` int(11),"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

# checar tamanho de nome para developer
TABLES['developer'] = (
    "CREATE TABLE `developer` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `name` int(35) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

# checar máximo de textos por post
TABLES['post'] = (
    "CREATE TABLE `post` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `title` int(75) NOT NULL,"
    "  `text` int(500) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['genero'] = (
    "CREATE TABLE `genero` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `name` int(35) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES[‘rel_player_nacionalidade’] = (
    "CREATE TABLE `rel_player_nacionalidade ` ("

    ") ENGINE=InnoDB")


# amigos
TABLES['rel_player_player'] = (
    "CREATE TABLE `rel_player_player ` ("

    ") ENGINE=InnoDB")

# player pertence ao grupo
TABLES[‘rel_player_group’] = (
    "CREATE TABLE `rel_player_group ` ("

    ") ENGINE=InnoDB")

# player tem o jogo
TABLES[‘rel_player_software’] = (
    "CREATE TABLE `rel_player_software ` ("
    "  `horas` int(11)"


    ") ENGINE=InnoDB")

# jogo tem gênero
TABLES[‘rel_software_genero’] = (
    "CREATE TABLE `rel_software_genero ` ("

    ") ENGINE=InnoDB")

# jogo tem desenvolvedor
TABLES[‘rel_software_developer’] = (
    "CREATE TABLE `rel_software_developer ` ("

    ") ENGINE=InnoDB")

# item da comunidade tem post
TABLES[‘rel_software_post’] = (
    "CREATE TABLE `rel_software_post ` ("

    ") ENGINE=InnoDB")

##
# TABLES['employees'] = (
#     "CREATE TABLE `employees` ("
#     "  `emp_no` int(11) NOT NULL AUTO_INCREMENT,"
#     "  `birth_date` date NOT NULL,"
#     "  `first_name` varchar(14) NOT NULL,"
#     "  `last_name` varchar(16) NOT NULL,"
#     "  `gender` enum('M','F') NOT NULL,"
#     "  `hire_date` date NOT NULL,"
#     "  PRIMARY KEY (`emp_no`)"
#     ") ENGINE=InnoDB")

# TABLES['departments'] = (
#     "CREATE TABLE `departments` ("
#     "  `dept_no` char(4) NOT NULL,"
#     "  `dept_name` varchar(40) NOT NULL,"
#     "  PRIMARY KEY (`dept_no`), UNIQUE KEY `dept_name` (`dept_name`)"
#     ") ENGINE=InnoDB")

# TABLES['salaries'] = (
#     "CREATE TABLE `salaries` ("
#     "  `emp_no` int(11) NOT NULL,"
#     "  `salary` int(11) NOT NULL,"
#     "  `from_date` date NOT NULL,"
#     "  `to_date` date NOT NULL,"
#     "  PRIMARY KEY (`emp_no`,`from_date`), KEY `emp_no` (`emp_no`),"
#     "  CONSTRAINT `salaries_ibfk_1` FOREIGN KEY (`emp_no`) "
#     "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE"
#     ") ENGINE=InnoDB")

# TABLES['dept_emp'] = (
#     "CREATE TABLE `dept_emp` ("
#     "  `emp_no` int(11) NOT NULL,"
#     "  `dept_no` char(4) NOT NULL,"
#     "  `from_date` date NOT NULL,"
#     "  `to_date` date NOT NULL,"
#     "  PRIMARY KEY (`emp_no`,`dept_no`), KEY `emp_no` (`emp_no`),"
#     "  KEY `dept_no` (`dept_no`),"
#     "  CONSTRAINT `dept_emp_ibfk_1` FOREIGN KEY (`emp_no`) "
#     "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE,"
#     "  CONSTRAINT `dept_emp_ibfk_2` FOREIGN KEY (`dept_no`) "
#     "     REFERENCES `departments` (`dept_no`) ON DELETE CASCADE"
#     ") ENGINE=InnoDB")

# TABLES['dept_manager'] = (
#     "  CREATE TABLE `dept_manager` ("
#     "  `dept_no` char(4) NOT NULL,"
#     "  `emp_no` int(11) NOT NULL,"
#     "  `from_date` date NOT NULL,"
#     "  `to_date` date NOT NULL,"
#     "  PRIMARY KEY (`emp_no`,`dept_no`),"
#     "  KEY `emp_no` (`emp_no`),"
#     "  KEY `dept_no` (`dept_no`),"
#     "  CONSTRAINT `dept_manager_ibfk_1` FOREIGN KEY (`emp_no`) "
#     "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE,"
#     "  CONSTRAINT `dept_manager_ibfk_2` FOREIGN KEY (`dept_no`) "
#     "     REFERENCES `departments` (`dept_no`) ON DELETE CASCADE"
#     ") ENGINE=InnoDB")

# TABLES['titles'] = (
#     "CREATE TABLE `titles` ("
#     "  `emp_no` int(11) NOT NULL,"
#     "  `title` varchar(50) NOT NULL,"
#     "  `from_date` date NOT NULL,"
#     "  `to_date` date DEFAULT NULL,"
#     "  PRIMARY KEY (`emp_no`,`title`,`from_date`), KEY `emp_no` (`emp_no`),"
#     "  CONSTRAINT `titles_ibfk_1` FOREIGN KEY (`emp_no`)"
#     "     REFERENCES `employees` (`emp_no`) ON DELETE CASCADE"
#     ") ENGINE=InnoDB")

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