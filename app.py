from flask import request,Flask,render_template,jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import subprocess,sys
from helper_functions import allowed_file
import os
from processor import generate_caption
import random
from pathlib import Path
import uuid

UPLOAD_FOLDER = './caption_images'
ALLOWED_EXTENTIONS = ['jpg','jpeg','png']

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/testpage', methods = ['POST','GET'])
def main():
    if request.method == 'POST':

        #if 'caption_image' not in request.files:
            #Do something if post has no file part
            #Better handled on client side using js

        print(request)
        uploaded_image = request.files.get("caption_image")

        #if uploaded_image.filename == '':
            #Do something if file has no name ( file not selected )
        #request.args.get('name')

        if uploaded_image and allowed_file(uploaded_image.filename, ALLOWED_EXTENTIONS):
            #save the image file to a folder for processing by the ML/DL script

            #checks whether the file is actually of the same extension as mentioned
            filename = secure_filename(uploaded_image.filename)
            
            if( len(filename) != 0):
                filename = str(uuid.uuid4()) +"."

            # Contruct path for image storage
            image_storage_path = os.path.join(app.config['UPLOAD_FOLDER'], filename )

            # Saves image in ./caption_images folders
            uploaded_image.save( image_storage_path )

            #call function from caption generation script
            caption = generate_caption( photoFileName = image_storage_path)

            # remove stored file after processing
            os.remove(path=image_storage_path)

            return jsonify(description = caption)

        return jsonify( error = "Non-Existent or Invalid File Upload")

    if request.method == 'GET':
        return jsonify(description = 'My First Heading')


if __name__ == '__main__':
    app.run(debug=False)