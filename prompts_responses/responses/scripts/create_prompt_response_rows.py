# Puts each prompt - response per row
from os import dup
from numpy import promote_types
import pandas as pd
from datetime import date
RESPONSE_PATH = "./data_scripts/model_responses/"
PROMPT_PATH = "./data_scripts/prompts/"
FINAL_PATH = "./data_scripts/final_responses/"

PROMPTID_NAME = "esl_promptid.txt"

FILE_NAMES = [
    # "dailydialog_blender3b_detok.txt",
    # "dailydialog_blender9b_detok.txt",
    # "dailydialog_blender23b_detok.txt",
    # "dailydialog_blender2400_detok.txt",
    # "dailydialog_dialogpt_detok.txt",
    # "dailydialog_gpt3_detok.txt",
    # "dailydialog_plato224L_detok.txt",
    # "dailydialog_plato232L_detok.txt",
    # "dailydialog_groundtruth_detok.txt"
    "esl_blender3b_2022.txt",
    "esl_blender9b_2022.txt",
    "esl_blender23b_2022.txt",
    "esl_blender2400_20220125.txt",
    "esl_dialogpt_responses_20220124.txt",
    "esl_gpt3_2022.txt",
    "esl_plato2_24L_2022.txt",
    "esl_plato2_32L_2022.txt",
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


with open(PROMPT_PATH + PROMPTID_NAME) as file:
    promptids_list = file.readlines()
    promptids_list = [line.rstrip() for line in promptids_list]
    print(promptids_list)

# Create duplicated prompts list - duplicate prompt for each model
duplicated_prompts_list = []
duplicated_promptids_list = []
for idx, prompt in enumerate(prompts_list):
    for _ in range(len(FILE_NAMES)):
        duplicated_prompts_list.append(prompt)
        duplicated_promptids_list.append(promptids_list[idx])


# Place all model responses in a giant list
responses_list = []
model_list = []
for file_name in FILE_NAMES:
    with open(FINAL_PATH + file_name) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        
        # Add model responses to the master list
        responses_list.append(lines)

        # Add model name to model list
        model_name = file_name.split('_')[1]
        model_list.append(model_name)

# Initialize master response list, grouped by prompts
master_responses_list = []
master_model_list = []
# Create a single series of all model responses, grouped together for each prompt
for prompt_idx in range(len(prompts_list)):
    for responses in responses_list:
        # Extract & save model response for specific prompt
        response = responses[prompt_idx]
        master_responses_list.append(response)
    master_model_list.extend(model_list)

# Create the final dataframe

# 1. Create dictionary with the two lists
d = {
    'prompt_id': duplicated_promptids_list,
    'prompt': duplicated_prompts_list,
    'response': master_responses_list,
    'model': master_model_list
}

df = pd.DataFrame(d)

df.to_excel(FINAL_PATH + dataset_name + '_rows_' + str(date.today()) + ".xlsx")

