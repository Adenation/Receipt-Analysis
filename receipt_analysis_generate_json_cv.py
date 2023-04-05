# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 14:53:43 2023

@author: Adenation
"""
#%% Imports

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import requests
import json
import time
from dotenv import load_dotenv
import os

 #%% Generate JSON


# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
subscription_key = os.getenv('SUBSCRIPTION_KEY')
endpoint = os.getenv('ENDPOINT')

# Set up the Azure Computer Vision API endpoint and key
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# set up the image path
folder_path = os.getcwd()

# Get a list of all PNG files in the folder
png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]

# Read each PNG file into a byte array and add it to a list
png_bytes_list = []
for png_file in png_files:
    with open(os.path.join(folder_path, png_file), 'rb') as f:
        png_bytes_list.append(f.read())

# Or if stored already in an earlier variable use that instead
# png_bytes_list = []
# buffer = BytesIO() 
# for img in receipt_list:
#     img.save(buffer, format='png')
#     png_bytes_list.append(buffer.getvalue())

    
# set up the API headers and parameters
headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key
}
params = {
    'language': 'en',
    'detectOrientation': 'true'
}



# call the API to analyze the images and load into a list of json payloads

headers_list = []
responses_list = []
json_data_list = []

for image_data in png_bytes_list:
    post = requests.post(endpoint, headers=headers, params=params, data=image_data)
    headers_list.append(post.headers)
    time.sleep(3) # Delay for 3 seconds to avoid going over 20 free calls per minute
    operation_url = post.headers['Operation-Location']
    attempts = 0; waiting = True
    while(waiting and attempts < 10):
        response = requests.get(operation_url, headers=headers)
        responses_list.append(response)
        if response.status_code == 200:
            json_data = json.loads(response.text)
            while(json_data["status"] == "running"):
                # While operation is successful and runnin, wait for it to finish
                time.sleep(3)
            # Once it has finished running status should change to succeeded
            # extract the JSON payload from the response
            json_data_list.append(json_data)
            # print the JSON payload
            print(json.dumps(json_data, indent=2))
            # break out of loop
            waiting = False
        if response.status_code == 202:
            print("Waiting for server to process response.  Attempting again in 3 seconds")
            attempts += 1
            time.sleep(3)
        else:
            print("Error retrieving results:", response.text, response.status_code)
    
    time.sleep(3)

#%% Persist JSON Payloads

# You can either call the filename from the .env file
filename = os.getenv('JSON_STORAGE')

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