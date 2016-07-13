from flask import Flask
from flask.templating import render_template
from flask import request,make_response, url_for,redirect
import boto3
import botocore
import os
import MySQLdb
import time
import random
from random import uniform
import memcache

#import aws_controller
from flask.templating import render_template
from flask.helpers import make_response

app = Flask(__name__, template_folder='templates')

global bucket

@app.route("/")
def main_page():
	return render_template('image_list.html')

@app.route("/upload",methods=["POST"])
def upload():

        # Upload
	file_to_upload = request.files['file_to_upload']
	s3 = boto3.resource('s3')
	bucket = s3.Bucket('aws-cse6331-utphala')
	exists = True
	try:
		s3.meta.client.head_bucket(Bucket='aws-cse6331-utphala')
	except botocore.exceptions.ClientError as e:
		error_code = int(e.response['Error']['Code'])
		if error_code == 404:
			exists = False
	UPLOAD_FOLDER = "/Users/Chethan/Downloads"
	file_name = file_to_upload.filename
	file_contents = file_to_upload.read()
	file_path = os.path.join(UPLOAD_FOLDER, file_name)
	s3.Object('aws-cse6331-utphala', file_name).put(Body=open(file_path, 'rb'))
	response_val = "File " + file_name + " inserted successfully!!"

	# File list
	file_list = dict()
	for bucket in s3.buckets.all():
            for s3object in bucket.objects.all():
                file_list[s3object.key] = [s3object.key]

	return render_template('image_list.html', response_value = response_val, files_list = file_list)

@app.route("/delete", methods=["POST"])
def delete_file():
        file_to_delete = request.form["file_to_delete"]
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('aws-cse6331-utphala')
        exists = True
	try:
		s3.meta.client.head_bucket(Bucket='aws-cse6331-utphala')
	except botocore.exceptions.ClientError as e:
		error_code = int(e.response['Error']['Code'])
		if error_code == 404:
			exists = False                          
        DeleteObj = {'Objects': [{'Key': file_to_delete }]}
        bucket.delete_objects(Delete=DeleteObj);
        response = "File deleted Successfully"
        files_list = dict()
	for bucket in s3.buckets.all():
            for s3object in bucket.objects.all():
                files_list[s3object.key] = [s3object.key]
        return render_template('image_list.html', response_value = response, files_list = files_list)

@app.route("/download", methods=["POST"])
def download_file():
        file_to_download = request.form["file_to_download"]
        s3 = boto3.resource('s3')
        DOWNLOAD_FOLDER = "/Users/Chethan/Documents/uploads"
	#file_name = file_to_download.filename
	file_path = os.path.join(DOWNLOAD_FOLDER, file_to_download)
        s3.Bucket('aws-cse6331-utphala').download_file(file_to_download, file_path)
        response = "File Downloaded Successfully!"
        # File List
        files_list = dict()
	for bucket in s3.buckets.all():
            for s3object in bucket.objects.all():
                files_list[s3object.key] = [s3object.key]
        return render_template('image_list.html', response_value = response, files_list = files_list)
        
@app.route("/execute_rds", methods=["POST"])
def execute_rds_queries():
        query_to_execute = request.form["rds_query_to_execute"]
        
        conn=MySQLdb.connect('rds-cse6331-utphala.cggcxeh6aa0m.us-east-1.rds.amazonaws.com','utphala_p','************','earthquake_details')
        pointer= conn.cursor()
        startTime = time.time()
        pointer.execute(query_to_execute)
        endTime = time.time()
        
        time_taken = endTime-startTime
        
        return render_template('image_list.html', response_value = None, rds_time_taken=time_taken)

@app.route("/execute_mem", methods=["POST"])
def execute_mem_queries():
        query_to_execute = request.form["mem_query_to_execute"]
        #set memcache client
        memc = memcache.Client(['memcache-utphala.kglgsa.0001.use1.cache.amazonaws.com:11211'],debug=1);

        #establish a connection
        conn=MySQLdb.connect('rds-cse6331-utphala.cggcxeh6aa0m.us-east-1.rds.amazonaws.com','utphala_p','************','earthquake_details')
        cur = conn.cursor()

        cache_data = memc.get('data')
        if not cache_data:
                startTime = time.time()
                cur.execute(query_to_execute)
                rows = cur.fetchall()
                memc.set('data',rows,200)
                endTime = time.time()
        else:
                startTime = time.time()
                rowCount = 0
                for row in cache_data:
                        rowCount += 1
                endTime = time
        time_taken = endTime-startTime
        conn.commit()
        cur.close()
        conn.close()
        return render_template('image_list.html', response_value = None, mem_time_taken=time_taken)
        
	

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
