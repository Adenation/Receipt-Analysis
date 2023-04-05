# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 15:08:38 2023

@author: Adenation
"""

## Generate environment variable

## Make sure you have dotenv installed on your machine, check pip commands
## Online as required

import os

file_name = ".env"

# Define the file path
file_path = os.path.join(os.getcwd(), file_name)

# Create the file
open(file_path, "w").close()

from dotenv import set_key

# Set the value of an environment variable in the .env file
set_key('.env', 'SUBSCRIPTION_KEY', '[Your key]')
set_key('.env', 'ENDPOINT', '[Your endpoint]')
set_key('.env', 'JSON_STORAGE', '[Your filename]')
set_key('.env', 'SUBSCRIPTION_KEY_FORM_RECOGNIZER', '[Your key]')
set_key('.env', 'ENDPOINT_FORM_RECOGNIZER', '[Your endpoint]')
set_key('.env', 'JSON_STORAGE_FORM_RECOGNIZER', '[Your filename]')