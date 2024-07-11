# Puts each prompt - response per row & change </s> into Person1:
from os import dup
from numpy import promote_types
import pandas as pd
from datetime import date
RESPONSE_PATH = "./data_scripts/model_responses/"
PROMPT_PATH = "./data_scripts/prompts/"
FINAL_PATH = "./data_scripts/final_responses/"

FILE_NAMES = [
    # "dailydialog_dialogpt_20211029-005818.txt",
    # "dailydialog_gpt3_responses.txt",
    # "dailydialog_plato2(24L)_211123.txt",
    # "dailydialog_plato2(32L)_211125.txt",
    # "dailydialogs_blender3b_20211125-143343.txt",
    # "dailydialogs_blender9b_20211128-162250.txt",
    # "dailydialogs_convAIPolyencoder(blenderTask)_20211128-151022.txt",
    # "dailydialogs_empathetic_20211128-193325.txt",
    # "dailydialogs_twitter(blenderTask)_20211128-153647.txt",
    "esl_dialogpt_20211112-165939.txt",
    "esl_gpt3_responses.txt",
    "esl_plato2(24L)_211123.txt",
    "esl_plato2(32L)_211223.txt",
    "esl_blender3b_20211127-175621.txt",
    "esl_blender9b_20211130-211702.txt",
    "esl_convAIPolyencoder(blenderTask)_20211128-150233.txt",
    "esl_empathetic_20211128-194459.txt",
    "esl_twitter(blenderTask)_20211128-160335.txt",
    "esl_groundtruth.txt"
]

# Create base Pandas DataFrame with prompts

# Read files


dialogpt_list = []
parlaiblenderpersona_list = []
gpt3_list = []

# To become a list of response_lists
response_list = []

dataset_name = FILE_NAMES[0].split("_")[0]
PROMPT_FILE = f"{dataset_name}_prompts.txt"

with open(PROMPT_PATH + PROMPT_FILE) as file:
    prompts_list = file.readlines()
    prompts_list = [line.rstrip() for line in prompts_list]
    print(prompts_list)


# Place all model responses in a giant list
responses_list = []
model_names = []
for file_name in FILE_NAMES:
    model_name = file_name.split('_')
    model_names.append(model_name)
    with open(RESPONSE_PATH + file_name) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]

        # Add model responses to the master list
        responses_list.append(lines)

# Create duplicated prompts list - duplicate prompt for each model
duplicated_prompts_list = []
duplicated_model_list = []
for prompt in prompts_list:
    for _ in range(len(FILE_NAMES)):
        # Prettify prompt
        utterances = prompt.split('</s>')
        pretty_prompt = ""
        person1 = True
        for utterance in utterances:
            if person1:
                pretty_prompt += "Person1: "
            else:
                pretty_prompt += "Person2: "
            
            pretty_prompt += utterance + "\n"

            # Switch person
            person1 = not person1

        duplicated_prompts_list.append(pretty_prompt)


# Initialize master response list, grouped by prompts
master_responses_list = []

# Create a single series of all model responses, grouped together for each prompt
for prompt_idx in range(len(prompts_list)):
    for responses in responses_list:
        # Extract & save model response for specific prompt
        response = responses[prompt_idx]
        master_responses_list.append(response)

# Create the final dataframe

# 1. Create dictionary with the two lists
d = {
    'prompts': duplicated_prompts_list,
    'responses': master_responses_list,
    'models': models_list
}

df = pd.DataFrame(d)

df.to_excel(FINAL_PATH + dataset_name + '_rows_' + str(date.today()) + ".xlsx")

