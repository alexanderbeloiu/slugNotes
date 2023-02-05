import os
#pip3 install flask
from flask import Flask, flash, request, redirect, url_for, render_template, request, redirect, url_for, flash, jsonify,send_from_directory
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
#dewg
#this is the object that interacts with the database
file_info=database.Files()
course_info=database.course()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#this function saves the file to the disk, then adds it to the database
def save_file(file):
    #secure filename does something to prevent hacking
    filename = secure_filename(file.filename)
    
    #adds the file to the database
    file_info.add_file(filename,'CSE_30','week1',filename,UPLOAD_FOLDER+'/'+filename)
    
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
    return render_template('upload.html')

@app.route("/")
def hello():
    return render_template('mainpage.html')


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





#(Aidan) Goal: make a list of classes that also has options to 
#POST: situation when a button is clicked. GET: natural state of webpage
@app.route("/classes", methods=['GET','POST'])
def add_class():
    name = None
    form = ClassForm()
    if form.validate_on_submit():
        #grab all the users that typed in the entered classname. Should return None unless the class is already in the database
        #Class.query.filter_by(name = form.name.data).first()
        #!!! Need to add and else statement in case the classdata does exist. Maybe say that this class is already in our database or smthn
        class_name=form.name.data
        new_class = course_info.add_class(form.name.data)
        if new_class is not False:
            flash("Class Added Successfully!")
            form.name.data = ''
            name = form.name.data
            form.name.data = ''
            for i in range(10):
                print(new_class)
                course_info.add_folder(str(f"Week {i+1}"), str(course_info.get_course_by_id(course_info.get_id_by_class_name(str(new_class)))))
        else:
            flash("That class is already in the DataBase!!!")
    
    our_classes = course_info.get_class_and_ids()
    
    return render_template('add_class.html',
    name = name,
    form = form,
    our_classes=our_classes)

@app.route("/classes/<int:id>/", methods=['GET','POST'])
def classes(id):
    name = None
    form = ClassForm()
    class_name = str(course_info.get_course_by_id(id))
    if form.validate_on_submit():
        #grab all the users that typed in the entered classname. Should return None unless the class is already in the database
        #Class.query.filter_by(name = form.name.data).first()
        #!!! Need to add and else statement in case the classdata does exist. Maybe say that this class is already in our database or smthn
        classdata = course_info.add_folder(form.name.data,class_name)
        
        if classdata is not False:
            flash("Class Added Successfully!")
            form.name.data = ''
            name = form.name.data
            form.name.data = ''
        else:
            flash("That class is already in the DataBase!!!")
    
    our_weeks = course_info.get_folders_list(class_name)
    print(our_weeks)
    print("------------------------------------------------------------")
    return render_template('add_week.html',
    name = name,
    form = form,
    our_weeks=our_weeks,
    id=id)



@app.route('/classes/<int:id>/<string:week>',methods=['POST','GET'])
def cmenu(id,week):
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
            file_info.add_file(filename,str(course_info.get_course_by_id(id)),week,str(filename),UPLOAD_FOLDER+'/'+filename)
    
    
    
    
    print(id,week)
    
    print("------------------------------------------------------------")
    name_to_update = str(course_info.get_course_by_id(id))
    files_list=file_info.get_files_list(name_to_update,week)
    print(files_list)
    
    return render_template("files.html",
            our_files=files_list,
            name = week)







@app.route("/getfile/<string:filename>")
def getfile(filename):
    filetype=filename.split(".")[1]
    if filetype=="pdf":
        return send_from_directory(app.config['UPLOAD_FOLDER'],filename, as_attachment=True,mimetype='application/pdf')
    
    if filetype=="jpg" or filetype=="png" or filetype=="jpeg":
        return '<img src="/rawfile/'+filename+'">'
       
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename, as_attachment=True)

@app.route("/rawfile/<string:filename>")
def rawfile(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename, as_attachment=True)





if __name__ == "__main__":
    app.run(port=4000, debug=True)  
