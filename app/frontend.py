from flask import Blueprint, render_template, app
from flask_appconfig import AppConfig
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
from flask_nav.elements import Navbar, View, Text
import os
from flask import request, redirect, url_for
from werkzeug.utils import secure_filename

from app.forms import TextInputForm
from app.nav import nav
from app.src.detector import Detector

UPLOAD_FOLDER = 'app/static/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

frontend = Blueprint('frontend', __name__)

nav.register_element('frontend_top', Navbar(
    View('Detector', '.index'),
    View('Debug-Info', 'debug.debug_root'),
    Text('Using Flask-Bootstrap {}'.format(FLASK_BOOTSTRAP_VERSION)), ))

detector = Detector()

@frontend.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@frontend.route("/", methods=["POST", "GET"])
def index():
    args = {"method": "GET"}

    return render_template("index.html", args=args)


@frontend.route('/img', methods=["POST", "GET"])
def img_form():
    if request.method == "POST":
        file = request.files["upload"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
    return render_template('img_form.html', img="images/" + filename)


@frontend.route("/detection", methods=["POST", "GET"])
def detection():
    labelImg = request.form.get('fructselect')
    pathImg = request.form.get('btnDtct')
    pathImg = detector.detect('app/static/' + pathImg, int(labelImg))
    return render_template("detection.html", pathImg=pathImg.replace('app/static/', ''))
