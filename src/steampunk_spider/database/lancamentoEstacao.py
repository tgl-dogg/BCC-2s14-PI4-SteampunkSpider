import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'steampunk'

# Get database connection
db_conn = mysql.connector.connect(user='root', password='vaporAranha', host='localhost', database='steampunk')
# Get cursor to perform operations on our database
cursor = db_conn.cursor()

request = ("SELECT "
	"(SELECT COUNT(software.release_date) FROM software "
		"WHERE software.release_date LIKE '%Jan%') AS Jan, "
	"(SELECT COUNT(software.release_date) FROM software "
		"WHERE software.release_date LIKE '%Feb%') AS Feb, "
	"(SELECT COUNT(software.release_date) FROM software "
		"WHERE software.release_date LIKE '%Mar%') AS Mar, "
	"(SELECT COUNT(software.release_date) FROM software "
		"WHERE software.release_date LIKE '%Apr%') AS Apr, "
	"(SELECT COUNT(software.release_date) FROM software "
		"WHERE software.release_date LIKE '%May%') AS May, "
	"(SELECT COUNT(software.release_date) FROM software "
		"WHERE software.release_date LIKE '%Jun%') AS Jun, "
	"(SELECT COUNT(software.release_date) FROM software "
		"WHERE software.release_date LIKE '%Jul%') AS Jul, "
	"(SELECT COUNT(software.release_date) FROM software "
		"WHERE software.release_date LIKE '%Aug%') AS Aug, "
	"(SELECT COUNT(software.release_date) FROM software "
		"WHERE software.release_date LIKE '%Sep%') AS Sep, "
	"(SELECT COUNT(software.release_date) FROM software "
		"WHERE software.release_date LIKE '%Oct%') AS Oct, "
	"(SELECT COUNT(software.release_date) FROM software "
		"WHERE software.release_date LIKE '%Nov%') AS Nov, "
	"(SELECT COUNT(software.release_date) FROM software "
		"WHERE software.release_date LIKE '%Dec%') AS 'Dec'")

cursor.execute(request)

for Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec in cursor:
	print Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec

cursor.close()
db_conn.close()

print ("connection ended")