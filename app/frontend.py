from flask import Blueprint, render_template, flash, redirect, url_for, request, app
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator


from app.forms import TextInputForm
from app.nav import nav

from app.src.sentiment_analyzer import SentimentAnalyzer

frontend = Blueprint('frontend', __name__)

nav.register_element('frontend_top', Navbar(
    View('Detector', '.index'),
    View('Debug-Info', 'debug.debug_root'),
    Text('Using Flask-Bootstrap {}'.format(FLASK_BOOTSTRAP_VERSION)), ))


MAX_FILE_SIZE = 1024 * 1024 + 1
@frontend.route("/", methods=["POST", "GET"])
def index():
    args = {"method": "GET"}
    if request.method == "POST":
        file = request.files["file"]
        if bool(file.filename):
            file_bytes = file.read(MAX_FILE_SIZE)
            args["file_size_error"] = len(file_bytes) == MAX_FILE_SIZE
        args["method"] = "POST"
    return render_template("index.html", args=args)


@frontend.route('/sentiment', methods=['GET'])
def sentiment_form():
    form = TextInputForm()
    return render_template('sentiment_form.html', form=form)


@frontend.route("/predict", methods=['GET'])
def predict():
    sentiment_text = request.args.get('textarea', '')
    respalyzer = SentimentAnalyzer()
    prediction_message = respalyzer.get_prediction_message(sentiment_text)
    return render_template("prediction.html", form=TextInputForm(),
                           sentiment_text=sentiment_text,
                           prediction_message=prediction_message)


