from flask import render_template, request, Flask
from flask.helpers import send_file, url_for
from werkzeug.utils import secure_filename

import os

import KittyKrypt.kitties as kt
import KittyKrypt.Conversion as Conversion

ALLOWED_EXTENSIONS = {'ppm', 'jpg', 'png', 'gif'}

def allowed_file(filename):
    #return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    return 

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "uploads"

class State:
    def __init__(self):
        self.input_file = "super_secret.txt"
        self.cat_file = "hackercat.jpg"


props = State()

        

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        if 'file' in request.files:
            files = request.files.getlist("file")
            for file in files:
                if "cat" in file.filename:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
                    props.cat_file = secure_filename(file.filename)
                    Conversion.convertToPPM(props.input_file)
                else:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
                    props.input_file = secure_filename(file.filename)
        if request.form.get("encryption") is not None:
            encrypted = kt.encryptFile(props.input_file, kt.keyFromCat(props.cat_file[:-4]+".ppm"))
            with open(props.input_file+".kky", 'w') as f:
                f.write(encrypted)
                return send_file(f, as_attachment=True)
        elif request.form.get("decryption") is not None:
            assert(props.cat_file[-10:] == ".encrypted")
            key = kt.keyFromCat(props.cat_file)
            with open(props.input_file, 'rb') as f:
                tmp = f.read().split(b'\xff\xff\xff\xff\xff')
                with open("AHHHHHH.txt", 'wb') as fml:
                    fml.write(tmp[0])
                kt.decryptFile(fml, key, tmp[1])

    return render_template("app.html", props=props)