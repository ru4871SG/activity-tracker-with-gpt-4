# Activity Tracker with GPT-4

Welcome to the GitHub repo for the Activity Tracker Flask app with GPT-4.

This app allows you to upload CSV files containing your daily activity schedules. Once the file has been uploaded, GPT-4 will automatically analyze each row of your activity. For example, if the first row of the column "Activity" has the value "Running for 2km", GPT-4 will label it as "Moderate" or "Intense" activity.

## Version

Current version: 0.1

## How to Use

Create your own `.env` file containing your MONGODB_URI and OpenAI API key. Don't forget to put your own MongoDB database name. You can find the format example of this `.env` file in `.env.example`, just follow the instructions over there.

The collection name that this app fetches from MongoDB is called `test_etl`. If you want to use another collection name in your database, make sure to change the mention of `test_etl` in `etl.py` and `routes.py`.

To run this app in your localhost, just type `flask run` in your Terminal. Make sure you have installed all the necessary libraries (I will provide requirements.txt later).

Once you are able to run the app locally, you can test it by using the uploaded csv sample files here, test.csv and test2.csv, to test how GPT-4 is able to detect and analyze the activities from the "Activity" column.

## Future Updates

This app is still at its earliest stage. I have not refactored most of the codes. In the future versions, I will also include an automatic data visualization feature (I am thinking to use the Bokeh library for this) that takes the arguments from GPT-4 analysis of the uploaded activities. I also have some plans to include other file formats and automatic syncing to third-party apps.