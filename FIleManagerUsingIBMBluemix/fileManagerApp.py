import hashlib, os, mimetypes, gnupg
import mimetypes, os
import keystoneclient.v3 as keystoneclient
import swiftclient.client as swiftclient
from flask import Flask, request, make_response, url_for,redirect

from datetime import datetime
from dateutil import tz

from cryptography.fernet import Fernet
key = Fernet.generate_key()
cipher_suite = Fernet(key)

container_size = 0

auth_url = "https://identity.open.softlayer.com/v3"
password = "BQ?X-[3{/c/aX.B0"
project_id = "3a146ab7ac4d40888beabd203b12bf9f"
region_name = "dallas"
user_id = "2c40af9a5442475e97c137d26ba5f236"

conn = swiftclient.Connection(key=password, authurl=auth_url, auth_version='3', os_options={"project_id":project_id, "user_id":user_id, "region_name":region_name})
print('Connection successful.')

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

ukey = ''

@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	return app.send_static_file('upload.html')
		

@app.route('/upload', methods=['POST', 'GET'])
def upload():
	if request.method == 'POST':
		container_name = 'Plain'

		
		conn.put_container(container_name)

		print'A new container ',container_name,' was created successfully.'
		
		file = request.files['file']
		file_contents = file.read()
		size=len(file_contents);
		global container_size 
		container_size += size

		print 'Total size', container_size

		if(size > (1024*1024)):
			return 'File exceed 1MB redirecting!!'
		    
		mime_type = mimetypes.guess_type(file.filename)
		
		conn.put_object(container_name, file.filename, contents=file_contents, content_type=mime_type)
		print'File ',file.filename,' was uploaded successfully.', 'size of file', size

		return 'File was uploaded successfully.'
	
		
@app.route('/eupload', methods=['POST', 'GET'])
def eupload():
	if request.method == 'POST':
		container_name = 'Encrypted'
		
		conn.put_container(container_name)
		print'A new container ',container_name,' was created successfully.'
		
		file = request.files['efile']
		# ukey = request.form['key']
		file_contents = file.read()
		size=len(file_contents);

		if(size > (1024*1024)):
			print 'File ', file.name, 'exceed 1MB redirecting!!'
			return redirect(url_for('list'))

			
		encrypted_file_name = 'e_'+file.filename
		print('Encrypting file...')
		
		cipher_text = cipher_suite.encrypt(file_contents)
		print('File encrypted successfully.')
			
		
		conn.put_object(container_name, encrypted_file_name,cipher_text, content_type='text/plain')
		print'File ',file.filename,' uploaded successfully.'
		
		
		return 'Encrypted file was uploaded successfully.'
		


@app.route('/download', methods=['GET'])
def download():
	if request.method == 'GET':
		id = request.args.get('id')
		container_name = request.args.get('cn')
		document = conn.get_object(container_name, id)
		if id[:2]=='e_':
			 response = make_response(cipher_suite.decrypt(document[1]))
		else:
			response = make_response(document[1])
		response.headers["Content-Disposition"] = "attachment; filename="+id
		return response

@app.route('/delete', methods=['GET'])
def delete():
	if request.method == 'GET':
		id = request.args.get('id')
		container_name = request.args.get('cn')
		conn.delete_object(container_name, id)
		return 'File was deleted successfully.'

port = int(os.getenv('VCAP_APP_PORT', 8080))

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=port)
