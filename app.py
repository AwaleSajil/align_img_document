from flask import Flask
from flask import render_template, request, redirect
import os

from utils import align_image, save_base64_img
from config import upload_dir, result_dir


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload-image", methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # if request.files:
        #     image = request.files["image"]
        #     image.save(os.path.join(upload_dir,image.filename))
        #     result = align_image(os.path.join(upload_dir,image.filename))
        #     save_base64_img(result, image.filename)
        #     return result

        if request.files:
            uploaded_files = request.files.getlist("image")
            for upload_file in uploaded_files:
                upload_file.save(os.path.join(upload_dir,upload_file.filename))
                result = align_image(os.path.join(upload_dir,upload_file.filename))
                save_base64_img(result, os.path.join(result_dir,upload_file.filename))
            #this gives base64 ouput for the last image
            return result

        # return redirect(request.url)
    # return render_template("upload_image.html")

if __name__ == "__main__":
    app.run()

