from flask import render_template, request, Flask
from flask.helpers import send_file, url_for
from werkzeug.utils import secure_filename

import os

import KittyKrypt.kitties as kt
import KittyKrypt.Conversion as Conversion

ALLOWED_EXTENSIONS = {'ppm', 'jpg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "uploads"

class State:
    def __init__(self):
        self.input_file = "da_cat.png"
        self.nonce = None


props = State()

        

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        if 'file' in request.files:
            if (file := request.files['file']) != '' and allowed_file(file.filename):
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
                props.input_file = secure_filename(file.filename)
                Conversion.convertToPPM(props.input_file)
        if request.form.get('do_the_thing') is not None:
            if request.form.get("encryption") is not None:
                with open 
                kt.encryptFile(props.input_file)
                return send_file(props.input_file[:-4]+".ppm", as_attachment=True, attachment_filename=props.input_file+".kky")
            else:
                if (key := request.form.get("cat_key")) is not None:
                    kt.decryptFile(props.input_file, key, props.nonce)
    return render_template("app.html", props=props)


@app.route('/about')
def about():
    return render_template("about.html")