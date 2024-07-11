# Read Prompts. model responses -> Pandas Table -> CSV
# Dataset Name, Dataset Id, Prompt id, prompt name, model name, model_id, model response

# 1. Read model response files from .csv

# 2. Read prompt info (prompts, prompt_id)
# 2. Combine with Prompt info

# 3. Output into a CSV file

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

df = pd.DataFrame(prompts_list)


df['dataset_name'] = dataset_name

for file_name in FILE_NAMES:
    with open(RESPONSE_PATH + file_name) as file:
        model_name = file_name.split("_")[1]

        lines = file.readlines()
        lines = [line.rstrip() for line in lines]

        response_series = pd.Series(lines)
        df[model_name] = response_series

df.to_excel(FINAL_PATH + dataset_name + '_' + str(date.today()) + ".xlsx")
