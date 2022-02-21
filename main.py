import io
from flask import render_template, request, Flask
from flask.helpers import send_file, url_for
from werkzeug.utils import secure_filename

import os
import requests

import KittyKrypt.kitties as kt

ALLOWED_EXTENSIONS = {'jpg', 'png'}

def allowed_file(filename):
    #return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    return True

app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = "static/uploads"

class State:
    def __init__(self):
        self.cat_extension = ".jpg"
        self.input_extension = ".txt"


props = State()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        if request.form.get("load_cat") is  not None:
            file = request.files['cat_file']
            props.cat_extension = file.filename[-4:]
            file.save("static/uploads/cat"+props.cat_extension)
            kt.convertToPPM("static/uploads/cat"+props.cat_extension)

        if request.form.get("load_input") is  not None:
            file = request.files['input_file']
            file.save("static/uploads/secret")
            if file.filename[-4:] != ".kky":
                props.input_extension = file.filename[-4:]

        #if (key := request.form.get("cat_key")) is not None:
        #    kt.applyKeyToCat(key, "static/cat.jpg")
        if request.form.get("radiobutton") == "encryption":
            kt.convertToPPM("static/uploads/cat"+props.cat_extension)
            encrypted = kt.encryptFile("static/uploads/secret", kt.keyFromCat("static/uploads/cat.ppm"))
            with open("static/uploads/secret.kky", 'wb') as f:
                f.write(encrypted)
            return send_file("static/uploads/secret.kky", as_attachment=True, mimetype="application/octet-stream")
        elif request.form.get("radiobutton") == "decryption":
            key = kt.keyFromCat("static/uploads/cat"+props.cat_extension)
            with open("static/uploads/secret.kky", 'rb') as f:
                tmp = f.read().split(b'\xff\xff\xff\xff\xff')
                with open("static/uploads/decrypter", 'wb') as fml:
                    fml.write(tmp[0])
                mem = io.BytesIO(kt.decryptFile("static/uploads/decrypter", key, tmp[1]))
                mem.seek(0)
                os.remove("static/uploads/decrypter")
                return send_file(mem, as_attachment=True, attachment_filename="secret"+props.input_extension, mimetype="application/octet-stream")
        elif request.form.get("random_cat") is not None:
            props.cat_extension, contents = kt.getRandomCat()
            with open("static/uploads/cat"+props.cat_extension, 'wb') as f:
                f.write(contents)
            kt.convertToPPM("static/uploads/cat"+props.cat_extension)


    return render_template("app.html", props=props)