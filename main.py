import os
from flask import Flask, flash, request, redirect, url_for, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import hashlib
import uuid
import database
from datetime import datetime
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
    
    
    #you guys can try to convert to the below code to a template
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route("/")
def hello():
    return render_template('index.html')




if __name__ == "__main__":
    app.run(port=4000, debug=True)  
