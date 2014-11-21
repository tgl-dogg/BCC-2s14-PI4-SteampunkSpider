import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'steampunk'

# Get database connection
db_conn = mysql.connector.connect(user='root', password='vaporAranha', host='localhost', database='steampunk')
# Get cursor to perform operations on our database
cursor = db_conn.cursor()

request = ("SELECT "
	"(SELECT COUNT(software.release_date) FROM software "
		"WHERE software.release_date LIKE '%Jan%' OR '%Feb%' OR '%Mar%') AS Winter, "
	"(SELECT COUNT(software.release_date) FROM software "
		"WHERE software.release_date LIKE '%Apr%' OR '%May%' OR '%Jun%') AS Spring, "
	"(SELECT COUNT(software.release_date) FROM software "
		"WHERE software.release_date LIKE '%Jul%' OR '%Aug%' OR '%Sep%') AS Summer, "
	"(SELECT COUNT(software.release_date) FROM software "
		"WHERE software.release_date LIKE '%Oct%' OR '%Nov%' OR '%Dec%') AS Fall")

cursor.execute(request)

for Winter, Spring, Summer, Fall in cursor:

    print Winter, Spring, Summer, Fall

cursor.close()
db_conn.close()

print ("connection ended")