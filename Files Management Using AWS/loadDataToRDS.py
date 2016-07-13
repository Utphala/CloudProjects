import boto3
import mysql.connector
import csv
import time
import urllib
import itertools

# Connect RDS
conn=mysql.connector.connect(user='utphala_p',password='*********',
host='rds-cse6331-utphala.cggcxeh6aa0m.us-east-1.rds.amazonaws.com', database='earthquake_details')

print 'Connected to mySQL'

pointer= conn.cursor()

opens=urllib.URLopener()

#link="https://s3.amazonaws.com/aws-cse6331-utphala/data/all_month.csv"
link = "/Users/Chethan/Downloads/all_month.csv"
f=opens.open(link)
'''
f = urllib.urlopen(link)
'''
csvfile= csv.reader(f)

startTime = int(time.time())

for row in itertools.islice(csvfile, 1, None):

	sql_query="""Insert into monthly_data values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""

	pointer.execute(sql_query,row)

conn.commit()

pointer.close()

endTime = int(time.time())

totalTime = endTime-startTime

print 'Time to load data using mysql '+str(totalTime)+' seconds'
