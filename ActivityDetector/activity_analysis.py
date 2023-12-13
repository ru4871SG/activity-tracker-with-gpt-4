''' This file contains the code for the activity 
    detection functionality of the chatbot.
'''

import os
import json
import requests

# ACTIVITY_KEYS = ['relaxed', 'calm', 'moderate', 'engaged', 'vigorous', 'intense', 'grueling', 'exhausting', 'extreme']
ACTIVITY_SCORES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def get_api_key():
    return os.getenv('OPENAI_API_KEY')

def activity_analyzer(activities):
    # GPT-4 API endpoint
    url = 'https://api.openai.com/v1/chat/completions'

    # Your OpenAI API key
    api_key = get_api_key()

    responses = []

    for text_to_analyze in activities:
        # Constructing the prompt for activity analysis
        prompt = f"Classify the intensity of the activity of the following text from 1 to 10. Make sure \
            your response only include the number. For example just answer 1 or just answer 2, and so \
            on: '{text_to_analyze}'."

        # Data to be sent to the API
        data = {
            'model': 'gpt-4',
            'messages': [
                {'role': 'system', 'content': 'You are a helpful assistant that classifies the \
                 intensity of the activity described by the text.'},
                {'role': 'user', 'content': prompt}
            ],
            'max_tokens': 50  # adjust max_tokens as per requirement
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }

        try:
            response = requests.post(url, data=json.dumps(data), headers=headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            continue

        # Validate the API response
        if response.status_code == 200:
            formatted_response = response.json()
            message = formatted_response['choices'][0]['message']['content'].strip()
            activity = process_gpt_message(message)
        else:
            activity = None
            message = f"Unexpected API response: {response.status_code}, {response.text}"

        # Append the response for each activity
        responses.append({'activity': activity, 'message': message})
    
    return responses


def process_gpt_message(message):
    print("Processing GPT Message:", message)

    for activity in ACTIVITY_SCORES:
        if str(activity) in message:
            return activity

    print("Unexpected GPT Message:", message)
    return None
