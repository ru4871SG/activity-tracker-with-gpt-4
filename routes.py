from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import json
from .ActivityDetector.activity_analysis import activity_analyzer
from .etl import etl_process

pages = Blueprint("activities", __name__, template_folder="templates", static_folder="static")

# Define allowed extensions for the user's uploaded file
ALLOWED_EXTENSIONS = {'csv'}

# Define a function to check if the uploaded file has the correct extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@pages.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            try:
                # Call etl_process function from etl.py
                etl_process(file_path)
            except Exception as e:
                return render_template('error.html', error=str(e))
            finally:
                # Delete the file after the ETL process
                if os.path.exists(file_path):
                    os.remove(file_path)

            return redirect(url_for('activities.index'))

    return render_template('upload.html')


@pages.route("/", methods=["GET", "POST"])
def index():
    # Fetch all activities
    activities_all = list(current_app.db.test_etl.find())

    # Convert activities data to JSON format for Highcharts interactive chart
    activities_json = json.dumps(activities_all)

    return render_template(
        "index.html",
        activities=activities_all,
        activities_chart=activities_json,
        title="Activity Tracker - Home"
    )
