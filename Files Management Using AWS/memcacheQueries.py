import mysql.connector
from mysql.connector import errorcode
import time
from random import uniform
import memcache

#set memcache client
memc = memcache.Client([':11211'],debug=1);

#establish a connection
conn=mysql.connector.connect(user='utphala_p',password='********',
host='rds-cse6331-utphala.cggcxeh6aa0m.us-east-1.rds.amazonaws.com', database='earthquake_details')

cur = conn.cursor()

#creating a view with limited set of tuples

query1="create view limited as select * from monthly_data LIMIT 2000"
cur.execute(query1)

#Creating 2000 Random numbers
randomNum = range(1,2000)
t0 = time.time() 
for count in randomNum:
 	#Generating decimal random numbers
	r=round(uniform(1,6),2)	
	#converting them to string
	arr=[str(r)]
	#Get data from memcache
	mag = memc.get('data')
	#check if the data is in memcache, if it is not in memcache, then fetch from the rds databse and put it to memcache
	if not mag:
		query = "select * from limited where magnitude= %s"
		cur.execute(query,arr) 
		rows = cur.fetchall()
		memc.set('data',rows,200)
		#print 'setting memcache'
	#if the data is in the memcache, then display the data
	else:
		for row in mag:
        		print "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (row[0], row[1], row[2], row[3], row[4], row[5],row[6], row[7], row[8], row[9], row[10],
        		row[11], row[12], row[13], row[14])
conn.commit() 
t1 = time.time()
print ("----------------------TIME TAKEN---------------------")
print t1-t0, "Seconds"
cur.close() 
conn.close()
