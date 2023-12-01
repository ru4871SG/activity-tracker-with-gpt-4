## Code for ETL operations

import pandas as pd
import re
import json
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
import uuid
import concurrent.futures
from .ActivityDetector.activity_analysis import activity_analyzer

## Load environment variables
load_dotenv()

## Set all the default variables
table_attribs = ["Hour", "Activity"]
mongodb_uri = os.getenv('MONGODB_URI')


## Logging process
def log_progress(message):
    ''' This function logs the mentioned message of a given stage of the
    code execution to a log file. Function returns nothing'''
    time_stamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second
    now = datetime.now() # get current timestamp
    time_stamp = now.strftime(time_stamp_format)
    with open("./code_log.txt","a") as f:
        f.write(time_stamp + ':' + message + '\n')

log_progress('Preliminaries complete. Initiating ETL process')


## Step 1 - Extract
def extract(source):
    # Check if the file exists
    if not os.path.exists(source):
        raise FileNotFoundError('File not found (HTTP 404)')

    try:
        # Read the first row to check if headers are present
        with open(source, 'r') as sourcefile:
            first_char = sourcefile.read(1)

        # Check if the first character of the first cell (A1) is a number to verify if it's a header or not 
        # (because "Hour" values always start with a number)
        if first_char.isdigit():
            # No headers, so set them using table_attribs
            df = pd.read_csv(source, header=None)
        else:
            # Headers are present, so read them
            df = pd.read_csv(source)

        # Only keep the first two columns - delete the rest
        df = df.iloc[:, :2]
        df.columns = table_attribs[:2]

        return df

    except pd.errors.ParserError:
        log_progress('Bad request (HTTP 400). The CSV file could not be parsed.')
        raise ValueError('Bad request (HTTP 400)')
    except Exception as e:
        print(e)
        log_progress(f'Internal Server Error (HTTP 500): {e}')
        raise Exception('Internal Server Error (HTTP 500)')


## Step 2 - Transform
def transform(df):
    # Validate the format of the first column and prepend '0' to single-digit hours
    # Regex pattern for hour format, the correct formats are 02:00 and 2:00, we don't accept the rest
    time_pattern = re.compile(r'^\d{1,2}:\d{2}$')
    for i, entry in enumerate(df[table_attribs[0]]):
        entry_str = str(entry)
        if not time_pattern.match(entry_str):
            raise Exception("Hour format invalid. Fail to transform!")
        # Check if the hour part is a single digit, and if so, prepend a '0'
        hour, _ = entry_str.split(':') #_ is a throwaway variable
        if len(hour) == 1:
            df.loc[i, table_attribs[0]] = '0' + entry_str

    # Add a row index to the DataFrame
    df['row_index'] = range(1, len(df) + 1)

    # transform to JSON
    json_df = df.to_json(orient='records')
    ready_json = json.loads(json_df)
    return ready_json


## Step 3 - Load
def load(data, uri):
    client = MongoClient(uri)
    db = client['tracker']
    collection = db['test_etl']

    for record in data:
        # Find existing document from MongoDB
        existing_doc = collection.find_one({'Hour': record['Hour']})
        
        if existing_doc:
            # If the document exists, update it without altering the '_id'
            update_fields = {k: v for k, v in record.items() if k != '_id'}
            collection.update_one({'_id': existing_doc['_id']}, {'$set': update_fields})
        else:
            # Generate a new '_id' only for new document and include the new gpt_message
            record['_id'] = uuid.uuid4().hex
            collection.insert_one(record)



## Async ETL process function
def etl_process(file_path):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(etl_pipeline, file_path)
        return future.result()

def etl_pipeline(file_path):
    try:
        df = extract(file_path)
        log_progress('Data extraction complete. Initiating Transformation process')

        transformed_data = transform(df)
        log_progress('Data transformation complete. Initiating Analysis process')

        for record in transformed_data:
            print("Record being sent to analyzer:", record['Activity'])
            activity_description = record['Activity']
            # Ensure we are passing a list with a single item
            analysis_results = activity_analyzer([activity_description])
            # Since we now get a list of results, take the first result
            if analysis_results:
                first_result = analysis_results[0]
                record['gpt_message'] = first_result['message']

        log_progress('Analysis complete. Initiating Load process')

        load(transformed_data, mongodb_uri)
        log_progress('ETL process complete')
        return "ETL process completed successfully."

    except FileNotFoundError as e:
        log_progress('ETL process failed: File not found (HTTP 404)')
        raise e

    except ValueError as e:
        log_progress('ETL process failed: Bad request (HTTP 400)')
        raise e

    except Exception as e:
        log_progress('ETL process failed: Internal Server Error (HTTP 500)')
        raise e