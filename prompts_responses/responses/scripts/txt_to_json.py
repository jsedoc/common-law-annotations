# Transform .txt prompts to .json format as outlined here:
# https://parl.ai/docs/tutorial_task.html#json-file-format-instead-of-text-file-format


# Read .txt input

# Loop through each dialogue

    # Transform into json

    # Save json

# Puts each prompt - response per row
from os import dup
from numpy import promote_types
import pandas as pd
from datetime import date
import json
RESPONSE_PATH = "./data_scripts/model_responses/"
PROMPT_PATH = "./data_scripts/scripts/prompts/raw_prompts/"
FINAL_PATH = "./data_scripts/final_responses/"
dataset_name = "dailydialog"
PROMPT_FILE = f"{dataset_name}_prompts_huda.txt"

with open(PROMPT_PATH + PROMPT_FILE) as file:
    prompts_list = file.readlines()
    prompts_list = [line.rstrip() for line in prompts_list]
    print(prompts_list)

# Create json prompts list - list of json prompts for each dialogue
json_prompts_list = []
for prompt in prompts_list:

    # Build base json
    base_dialogue_json = { "dialog": [ [  
    ] ]}

    # Prettify prompt
    utterances = prompt.split('</s>')
    pretty_prompt = ""
    person1 = True
    for utterance in utterances:

        # Build base utterance json
        base_utterance_json = {
            "id": "person1" if person1 else "person2", 
            "text": utterance
        }

        # Switch person
        person1 = not person1

        # Append utterance to 
        base_dialogue_json["dialog"][0].append(base_utterance_json)
    
    # Add dummy (empty) utterance
    dummy_utterance_json = {
        "id": "person1" if person1 else "person2",
        "text": ""
    }
    base_dialogue_json["dialog"][0].append(dummy_utterance_json)

    
    # Append dialgoue into prompts list
    json_prompts_list.append(base_dialogue_json)

# Save each json into a line
with open(PROMPT_PATH + dataset_name+'_prompts_huda.json', 'w') as file:
    for prompt in json_prompts_list:
        json_obj = json.dumps(prompt)
        file.write(json_obj)
        file.write('\n')
