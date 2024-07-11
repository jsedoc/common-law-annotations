# Script to clean response into one-response-per-line format

# Puts each prompt - response per row
from os import dup
from numpy import promote_types
import pandas as pd
from datetime import date
import json
RESPONSE_PATH = "./data_scripts/model_responses/"
PROMPT_PATH = "./data_scripts/prompts/"
FINAL_PATH = "./data_scripts/final_responses/"
dataset_name = "esl"
FILE_NAME = f"{dataset_name}_dialoGPT_medium_20220124-134353.txt"

with open(RESPONSE_PATH + FILE_NAME) as file:
    responses_list = file.readlines()


extracted_responses = []

# Extract responses
for response in responses_list:

    # If response is a linebreak, skip
    if response == '\n':
        continue

    # Split based on \t
    extracted_response = response.split('\t')[1]

    extracted_responses.append(extracted_response.replace(" .", "."))

# Save each json into a line
with open(FINAL_PATH + dataset_name+'_dialogpt_responses.txt', 'w') as file:
    for response in extracted_responses:
        file.write(response)