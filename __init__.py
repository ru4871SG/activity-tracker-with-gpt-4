from dotenv import load_dotenv
from flask import Flask, render_template
import os
from pymongo import MongoClient
from .routes import pages

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["MONGODB_URI"] = os.environ.get("MONGODB_URI")

    app.db = MongoClient(app.config["MONGODB_URI"]).get_default_database()

    app.register_blueprint(pages, url_prefix="/")
    return app

app = create_app()
app.config['UPLOAD_FOLDER'] = './uploads' #Where user's uploaded CSV file will be temporarily stored

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html'), 500