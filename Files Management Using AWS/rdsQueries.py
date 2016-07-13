import mysql.connector
from mysql.connector import Error
from mysql.connector import MySQLConnection
import time
import random

#Connect to RDS with my user credentials and declare a for the DB instance
conn=mysql.connector.connect(user='utphala_p',password='*******',
host='rds-cse6331-utphala.cggcxeh6aa0m.us-east-1.rds.amazonaws.com', database='earthquake_details')

pointer= conn.cursor()

if conn.is_connected():
	print('Connected to MySQL database')

loop_times = range(1,20)
startTime = time.time()

for count in loop_times:
	number = round(random.uniform(0,6),2)
	num_arr = [str(number)]
	query = "SELECT * FROM monthly_data WHERE magnitude = %s"
	fetch_query = pointer.execute(query,num_arr)
	rows = pointer.fetchall()
	
	for row in rows:
		print row

conn.commit()

endTime = time.time()
totalTime = endTime-startTime

print 'Total time to excute query ' +str(totalTime)+' seconds'

# Close connections
pointer.close()
conn.close()
