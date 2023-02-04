import os
from flask import Flask, flash, request, redirect, url_for, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import hashlib
import uuid
import database
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
#Import for creating forms. pip3 install flask-wtf
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

UPLOAD_FOLDER = 'data'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','c','py','docx','doc'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "ouhojaheoduh[a0uhfouahd;oubasdoiholjawbe;h[oiabfljhvipuh"

#this is the object that interacts with the database
file_info=database.Files()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#this function saves the file to the disk, then adds it to the database
def save_file(file):
    #secure filename does something to prevent hacking
    filename = secure_filename(file.filename)
    
    #adds the file to the database
    file_info.add_file(filename,'CSE_30','week1',filename,100,datetime.today().strftime('%Y-%m-%d %H:%M:%S'),filename[filename.rindex("."):len(filename)],1,UPLOAD_FOLDER+'/'+filename)
    
    #saves the file to the disk
    file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    return filename

#how to do file upload https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            
            filename=save_file(file)
            return redirect(url_for('upload_file', name=filename))
    return 'oops looks like ur broken!'

@app.route("/")
def hello():
    return render_template('index.html')


#Creating a Form Class for adding new classes to the class database. One input box. One submit box
#used what the forms. We can add alot of cool form types if we want if we have time!!! https://youtu.be/GbJPqu0ff9A?t=1173
app.config['SECRET_KEY'] = "I hope I'm doing this right?"
class ClassForm(FlaskForm):
    name = StringField("Add a New Class Here!", validators=[DataRequired()])
    submit = SubmitField("Submit")




#Creating a class database to hold all possible classes on the site!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///subject.db'
with app.app_context():
    cdb = SQLAlchemy(app)

#subject class for each individual class object
class Class(cdb.Model):
    #id so that we can delete or modify a specific element. Primary key generates this unique id
    id = cdb.Column(cdb.Integer, primary_key = True)
    name = cdb.Column(cdb.String(200), nullable=False, unique=True)
    date_added = cdb.Column(cdb.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.name




#(Aidan) Goal: make a list of classes that also has options to 
#POST: situation when a button is clicked. GET: natural state of webpage
@app.route("/classes", methods=['GET','POST'])
def add_class():
    name = None
    form = ClassForm()
    if form.validate_on_submit():
        #grab all the users that typed in the entered classname. Should return None unless the class is already in the database
        classdata = Class.query.filter_by(name = form.name.data).first()
        #!!! Need to add and else statement in case the classdata does exist. Maybe say that this class is already in our database or smthn
        if classdata is None:
            classdata = Class(name = form.name.data)
            #ig its adding and committing the new data to our database?
            cdb.session.add(classdata)
            cdb.session.commit()
            flash("Class Added Successfully!")
            form.name.data = ''
            name = form.name.data
            form.name.data = ''
        else:
            flash("That class is already in the DataBase!!!")
            
    our_classes = Class.query
    return render_template('add_class.html',
    name = name,
    form = form,
    our_classes=our_classes)







if __name__ == "__main__":
    app.run(port=4000, debug=True)  
