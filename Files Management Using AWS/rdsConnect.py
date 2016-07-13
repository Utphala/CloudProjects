import boto3
import mysql.connector

#Connect to RDS with my user credentials and declare a for the DB instance
conn=mysql.connector.connect(user='utphala_p',password='*******',
host='rds-cse6331-utphala.cggcxeh6aa0m.us-east-1.rds.amazonaws.com', database='earthquake_details')

pointer= conn.cursor()

#Create a table to upload the all_month.csv file to RDS

pointer.execute("""create table monthly_data(time_occured varchar(50), latitude varchar(50), longitude
varchar(50), depth varchar(50), magnitude varchar(50), magtype varchar(50), nst varchar(50), gap
varchar(50), dmin varchar(50), rms varchar(50), net varchar(50), id varchar(50) PRIMARY KEY,
updated varchar(50), place varchar(50), type_occured varchar(50), horizontalError varchar(50), 
depthError varchar(50),magError varchar(50), magNst varchar(50), status varchar(50), locationSource varchar(50), magSource varchar(50)); """)

pointer.execute("show tables")

print pointer.fetchall()

conn.close()
