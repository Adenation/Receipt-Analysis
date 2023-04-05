# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 08:19:55 2023

@author: Adenation
"""
#%% Imports
import os
import time
import requests
import json

from dotenv import load_dotenv

#%% Generate JSON

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
subscription_key = os.getenv('SUBSCRIPTION_KEY_FORM_RECOGNIZER')
endpoint = os.getenv('ENDPOINT_FORM_RECOGNIZER')

# Set the API version and content type
api_version = 'v2.1'
content_type = 'image/png'

# Set the input file path
input_file_path = os.getcwd()

# Define the request headers
headers = {
    'Content-Type': content_type,
    'Ocp-Apim-Subscription-Key': subscription_key,
}

# Define the request parameters
params = {
    'includeTextDetails': 'true'
}

# Set up list of PNG files to process
png_files = [f for f in os.listdir(".") if f.endswith(".png")]

responses_list = []
json_data_list = []

# Process each PNG file
for png_file in png_files:
    with open(png_file, "rb") as file:
        response = requests.post(
            endpoint + "/formrecognizer/" + api_version + "/prebuilt/receipt/analyze",
            headers=headers,
            params=params,
            data=file.read(),
        )
        time.sleep(3)
        if response.status_code == 202:
            operation_url = response.headers["Operation-Location"]
            attempts = 0
            waiting = True
            while waiting and attempts < 10:
                response = requests.get(operation_url, headers=headers)
                responses_list.append(response)
                if response.status_code == 200:
                    json_data = json.loads(response.text)
                    while json_data["status"] == "running":
                        time.sleep(3)
                    if json_data["status"] == "succeeded":
                        json_data_list.append(json_data)
                        print(json.dumps(json_data, indent=2))
                        break
                    else:
                        print("Still Running:", png_file)
                        break
                elif response.status_code == 202:
                    print(
                        "Waiting for server to process response. Attempting again in 3 seconds"
                    )
                    attempts += 1
                    time.sleep(3)
                else:
                    print(
                        "Error retrieving results:",
                        response.text,
                        response.status_code,
                    )
                    break
        else:
            print("Error processing file:", png_file)

#%% Persist JSON Payloads

# You can either call the filename from the .env file
filename = os.getenv('JSON_STORAGE_FORM_RECOGNIZER')

# Or comment the above line of code out and replace filename with the
# string literal of the file name you desire

with open(filename, 'a') as f:
    # Iterate through payloads
    for i, payload in enumerate(json_data_list):
        # Write JSON payload to file
        f.write(json.dumps(payload))
        # Add separator between payloads
        f.write('\n')
f.close()