# Create a xlsx file of prompts </s> changed to Person1: / Person2:
import pandas as pd

# File Paths
DATASET_NAME = "esl"
PROMPT_PATH = "./data_scripts/prompts/"
FINAL_PATH = "./data_scripts/final_responses/"
PROMPT_FILE = f"{DATASET_NAME}_truecased_detok.txt"

# Read original prompts </s> format
with open(PROMPT_PATH + PROMPT_FILE) as file:
    prompts_list = file.readlines()
    prompts_list = [line.rstrip() for line in prompts_list]
    print(prompts_list)

# Convert </s> into Person1: / Person2: format
prettified_prompts = []
for prompt in prompts_list:
    # Prettify prompt
    utterances = prompt.split('</s>')
    pretty_prompt = ""
    person1 = True
    for utterance in utterances:
        if person1:
            pretty_prompt += "Person A: "
        else:
            pretty_prompt += "Person B: "
        
        pretty_prompt += utterance + "\n"

        # Switch person
        person1 = not person1

    prettified_prompts.append(pretty_prompt)

prettified_prompts_s = pd.Series(prettified_prompts)

prettified_prompts_s.to_excel(FINAL_PATH + DATASET_NAME + "_truecased_prettified.xlsx")