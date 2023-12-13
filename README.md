# Activity Tracker with GPT-4

Welcome to the GitHub repo for the Activity Tracker Flask app with GPT-4.

This app allows you to upload CSV files containing your daily activity schedules. Once the file has been uploaded, GPT-4 will automatically rate the intensity of each activity. For example, if the first row of the Activity column has the value "Running for 2km", GPT-4 may rate it as 6 or 7 (out of 10).

Once you upload your CSV file, this app will automatically create an interactive line chart using Highcharts library, where the x-axis represents the hours, and the y-axis represents the activity ratings by GPT-4.

## Version

Current version: 0.2

## How to Use

Create your own `.env` file containing your MONGODB_URI and OpenAI API key. Don't forget to put your own MongoDB database name. You can find the format example of this `.env` file in `.env.example`, just follow the instructions over there.

The collection name that this app fetches from MongoDB is called `test_etl`. If you want to use another collection name in your database, make sure to change the mention of `test_etl` in `etl.py` and `routes.py`.

To run this app in your localhost, just type `flask run` in your Terminal. Make sure you have installed all the necessary libraries (I will provide requirements.txt later).

Once you are able to run the app locally, you can test it by using the uploaded csv sample files here, test.csv and test2.csv, to test how GPT-4 is able to detect and rate the activities from the "Activity" column.

## Future Updates

This app is still at its early stage. I have not refactored most of the codes. In the future versions, I will include other file formats and automatic syncing to third-party apps.