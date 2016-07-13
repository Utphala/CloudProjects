"""
main is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask,render_template,request,session
from pymongo import MongoClient
import uuid
import base64
import time
import config
#import pydocumentdb.document_client as document_client


app = Flask(__name__)
app.secret_key="secret"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=["POST"])
def signup():

    startTime = time.time()

    username=request.form['user_name']
    passwd=request.form['password']

    client = MongoClient('mongodb://utphala:utphala@ds040489.mlab.com:40489/notesappstorage')
    db = client.notesappstorage

    users = db.usercollection
    

    # Create document
    post = { 'id': str(uuid.uuid1()),
          'username': username,
          'password': passwd,
          'num_of_files' : 10,
          'quota': 10*1024*1024
        }
    post_id = users.insert_one(post).inserted_id

    endTime = time.time()
    totalTime = endTime - startTime

    
    return render_template("index.html", timeTaken = totalTime)
		
@app.route('/login',methods=['GET','POST'])
def login():

    startTime = time.time()
    
    username = request.form['user_name'];
    passwd = request.form['password'];

    client = MongoClient('mongodb://utphala:utphala@ds040489.mlab.com:40489/notesappstorage')
    db = client.notesappstorage

    users = db.usercollection

    # Read documents and take first since id should not be duplicated.
    
    validUser = users.find({'username': username, 'password':passwd})
    if validUser:
            session['user'] = username
            endTime = time.time()
            totalTime = endTime - startTime
            
            return render_template("upload.html", timeTaken = totalTime)

    return "Failure!! Please register before you continue."
 
@app.route('/upload',methods =['GET','POST'])
def upload():

        startTime = time.time()

        client = MongoClient('mongodb://utphala:utphala@ds040489.mlab.com:40489/notesappstorage')
        db = client.notesappstorage

	# Read form data
        subject = request.form['notes_sub']
 	file = request.files['notes_to_upload']
	priority = request.form['notes_prior']
	time_of_upload = time.time()

        # Extract file extension
        filename = file.filename
        extension = filename.split('.')
        
        if (extension[1] == "txt"):
            fileFormat = "text"
            with open(file.filename, "rb") as note_file:
                encoded_string = note_file.read()
        else:
            fileFormat = "image"
            with open(file.filename, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())

        if(session['user']):
            currentUser =  session.get('user')
        else:
            currentUser = "anonymous"

        user_obj = db.usercollection.find_one({"username": currentUser})
        fileQuota = user_obj['num_of_files']
        
        if (fileQuota > 0):

            dbstartTime = time.time()
        
            # Create document
            document = { 'id': str(uuid.uuid1()),
              'subject' : subject,
              'notes' : encoded_string,
              'format' : fileFormat,
              'user': currentUser,
              'fileSize': len(encoded_string),
              'priority' : int(priority),
              'uploadTime' : time_of_upload    
            }
            
            dbtime = ((time.time()) - dbstartTime)

            document_id = db.notescollections.insert_one(document).inserted_id
            
            endTime = time.time()
            totalTime = endTime - startTime

            if document_id:
                response = "Notes uploaded successfully, click on View Notes button"
            else:
                response = "Failed to upload image."
        else:
            response = "User quota exceeded!!"
            
        return render_template("upload.html", response_value = response, timeTaken = totalTime, dbTime = dbtime)
  

@app.route('/view',methods =['GET','POST'])
def view():

    startTime = (time.time())

    client = MongoClient('mongodb://utphala:utphala@ds040489.mlab.com:40489/notesappstorage')
    db = client.notesappstorage

    sort_type = request.form['sort_type']
    print sort_type
 

    dbstartTime = time.time()

    document_coll = list(db.notescollections.find({'user': session.get('user')}).sort([(sort_type,-1)]))
    #print document_coll

    
    dbtime = ((time.time()) - dbstartTime)
    
    notes_list = dict()
    
    for document in document_coll:
        notes_list[document['id']] = [document['subject'],document['notes'],document['format'],document['priority'],document['uploadTime'],document['fileSize']]


    endTime = (time.time())
    totalTime = endTime - startTime

 
        
    return render_template("notes_list.html",notes_list= notes_list,timeTaken = totalTime, dbTime = dbtime)


@app.route("/delete", methods=["POST"])
def delete_images():

    startTime = (time.time())
    client = MongoClient('mongodb://utphala:utphala@ds040489.mlab.com:40489/notesappstorage')
    db = client.notesappstorage

    notes_to_delete = request.form["file_to_delete"]

    dbstartTime = time.time()
    
    db.notescollections.remove({"id":notes_to_delete})
    
    dbtime = ((time.time()) - dbstartTime)
    response ="Image deleted, click on View Images"
 
    endTime = (time.time())
    totalTime = endTime - startTime
    
    return render_template("upload.html",response_value=response,timeTaken = totalTime, dbTime = dbtime)

'''

@app.route("/add",methods=['POST'])
def add_key():
    keyword = request.form["keyword"]

    client = MongoClient('mongodb://104.154.93.59:27017/')
    db = client.imagestorage
    
    post = {"keyword": keyword}

    keys = db.keywords
    post_id = keys.insert_one(post).inserted_id

    return render_template("upload.html")


@app.route("/search_disp", methods=["POST"])
def search_disp():
    
    searchWord = request.form["search_word"]
    
    client = MongoClient('mongodb://104.154.93.59:27017/')
    db = client.imagestorage
    image_coll=db.images.find()
    image_list = dict()
    obj = db.images.find_one({'comment': searchWord})
    for image in image_coll:
        if ( obj ):
            image_list[obj['id']] = [obj['username'],obj['image'],obj['comment']]
    
    return render_template("notes.list.html",image_list= image_list)

    


@app.route("/delete_spec", methods=["POST"])
def search():
    userName_toDel = request.form["userName_todel"]
    searchWord = request.form["search_word"]
    
    client = MongoClient('mongodb://104.154.93.59:27017/')
    db = client.imagestorage
    
    delete_obj = db.images.find_one({'username': userName_toDel,'comment': searchWord})
    
    db.images.remove({'username': userName_toDel,'comment': searchWord})

    response = "Image deleted, click on View Images"
    
    return render_template("upload.html",response_value=response)

'''
@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')
    


if __name__ == "__main__":
    
    app.run()


