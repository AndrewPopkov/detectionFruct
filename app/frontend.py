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


detector =Detector()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@frontend.route("/", methods=["POST", "GET"])
def index():
    args = {"method": "GET"}

    return render_template("index.html", args=args)


@frontend.route('/sentiment', methods=["POST", "GET"])
def sentiment_form():
    if request.method == "POST":
        file = request.files["upload"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
    return render_template('sentiment_form.html', img=filename)

# @frontend.route("/predict", methods=['GET'])
# def predict():
#     sentiment_text = request.args.get('textarea', '')
#     respalyzer = SentimentAnalyzer()
#     prediction_message = respalyzer.get_prediction_message(sentiment_text)
#     return render_template("prediction.html", form=TextInputForm(),
#                            sentiment_text=sentiment_text,
#                            prediction_message=prediction_message)
