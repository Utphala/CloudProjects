"""
main is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask,render_template,request,session
from pymongo import MongoClient
import uuid
import base64
import time


app = Flask(__name__)
app.secret_key="secret"

file_quote = 10*1024*1024
#app.config.from_pyfile('config.py')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024    # 50 Mb limit

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=["POST"])
def signup():
    
    client = MongoClient('mongodb://104.154.93.59:27017/')
    db = client.imagestorage
    
    username=request.form['user_name']
    passwd=request.form['password']
   
    post = {"username": username,
            "password": passwd,
            "quota": 10*1024*1024}

    users = db.users
    post_id = users.insert_one(post).inserted_id
    print post_id
    return render_template("index.html")
		
@app.route('/login',methods=['GET','POST'])
def login():
    username = request.form['user_name'];
    passwd = request.form['password'];

    client = MongoClient('mongodb://104.154.93.59:27017/')
    db = client.imagestorage
    
    result = db.users.find({"username": username, "password": passwd})
    if result:
        for row in result:
            print row
            session['user'] = username
            return render_template("upload.html")
    
    #session['user'] = NULL
    return "Failure!! Please register before you continue."
  

@app.route('/upload',methods =['GET','POST'])
def upload():
	
 	file = request.files['image_to_upload']
	cmnt = request.form['image_desc']

	client = MongoClient('mongodb://104.154.93.59:27017/')
        db = client.imagestorage
        
	file_contents = file.read()
	size=len(file_contents);

        # Return if individual file is > the limit
        if(size>file_quote):
            response = "File size exceeded the limit"
            return render_template("upload.html", response_value = response, timeTaken = 0)
        
	startTime = int(time.time())
        '''
	with open(file.filename, "wb") as new:
            new.write(file.read())
        '''
        with open(file.filename, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            

        if(session['user']):
            currentUser =  session.get('user')
        else:
            currentUser = "anonymous"

        user_obj = db.users.find_one({"username": currentUser})
        user_quota = user_obj['quota']
        
        #user_quota-=size
   
        if (user_quota > 0):
        
            post = {"image": encoded_string,
                    "comment" : cmnt,
                    "username": currentUser,
                    "filesize": size,
                    "id": str(uuid.uuid1())
                    }
        
            post_id = db.images.insert_one(post).inserted_id

            endTime = int(time.time())
            totalTime = endTime - startTime
            
            decode = encoded_string.decode()
            img_tag = '<img alt="sample" src="data:image/png;base64,{0}">'.format(decode)

            if post_id:
                response = "Image uploaded successfully, click on View Images button"
            else:
                response = "Failed to upload image."
        else:
            response = "User quota exceeded!!"
            totalTime = 0
            
        return render_template("upload.html", response_value = response, timeTaken = totalTime)
  


@app.route('/view',methods =['GET','POST'])
def view():

    client = MongoClient('mongodb://104.154.93.59:27017/')
    db = client.imagestorage
    
    startTime = int(time.time())
    
    image_coll=db.images.find()
    image_list = dict()
    
    for image in image_coll:
        image_list[image['id']] = [image['username'],image['image'],image['comment'],image['filesize']]

    endTime = int(time.time())
    totalTime = endTime - startTime
        
    return render_template("image_list.html",image_list= image_list,timeTaken = totalTime)

@app.route("/delete", methods=["POST"])
def delete_images():
    image_to_delete = request.form["file_to_delete"]
    
    client = MongoClient('mongodb://104.154.93.59:27017/')
    db = client.imagestorage
    
    delete_obj = db.images.find_one({"id":image_to_delete})
    
    
    if (delete_obj['username'] == session.get('user')):
        db.images.remove({"id":image_to_delete})
        response ="Image deleted, click on View Images"
    else:
        response = "You cannot delete other user pics!!"
    
    return render_template("upload.html",response_value=response)


@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')
    


if __name__ == "__main__":
    
    app.run()


