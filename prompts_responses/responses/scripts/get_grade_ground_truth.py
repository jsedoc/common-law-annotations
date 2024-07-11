# Each prompt should become a string -> w a separator
# i.e. "blablabla </s> lololol </s> hehehe"
# tokenization should be consistent -> what's it like on SQL?

# 1. Separate OG utterances by 
# __eou__
# 2. Detokenize prompts
# 3. Combine into a single string

# 4. Format new DD prompts
# 5. Detokenize prompts

from os import dup
from urllib import response
from numpy import promote_types
import pandas as pd
from datetime import date
RESPONSE_PATH = "./data_scripts/model_responses/"
PROMPT_PATH = "./data_scripts/prompts/"
FINAL_PATH = "./data_scripts/final_responses/"
FILE_NAME_OG = 'dialogues_text_og.txt'
FILE_NAME_NEW = 'dailydialog_prompts.txt'

with open(PROMPT_PATH + FILE_NAME_OG) as file:
    prompts_list_og = file.readlines()

with open(PROMPT_PATH + FILE_NAME_NEW) as file:
    prompts_list_new = file.readlines()

# Each prompt is split into utterance
# Each utterance becomes a key
# The utterances are grouped together in the new_prompts loop
prompts_dict_og = {}

og_utterance_count = 0
og_utterance_list = []

for prompt in prompts_list_og:
    utterances = prompt.split('__eou__')    
    for idx, utterance in enumerate(utterances):
        prompts_dict_og[utterance.lower().replace(' ', '').strip().replace("'",'').replace("-","")] = (utterance, og_utterance_count)
        og_utterance_list.append(utterance)
        og_utterance_count += 1

master_prompt_list_new = []

# Keep track of how many utterances are incomplete / not found
incomplete_count = 0

# List to store GRADE responses
response_list = []

# For each new prompt, check if utterance is in dict
# If so,  append it to the 'prompt list'
# Append prompt list to master prompt list
# this we I can 'cut out' the specific prompts used!

for idx, prompt_new in enumerate(prompts_list_new):
    
    most_recent_hit_utterance = ''

    prompt_list_new = []
    utterances_new = prompt_new.split('</s>')

    num_utterances = len(utterances_new)
    utterance_count = 0
    for utterance in utterances_new:
        if utterance.lower().replace(' ', '').strip().replace("'",'').replace("-","") in prompts_dict_og:
            prompt_list_new.append(prompts_dict_og[utterance.lower().replace(' ', '').strip().replace("'",'').replace("-","")])
            utterance_count += 1

            most_recent_hit_utterance = utterance
    
    if utterance_count != num_utterances:
        incomplete_count += 1
        print('incomplete num:', idx)
        # print(utterances_new) # OG
        # print(prompt_list_new) # Found prompts
        response_list.append('MISSING')
    else:
        next_utterance_id = prompts_dict_og[most_recent_hit_utterance.lower().replace(' ', '').strip().replace("'",'').replace("-","")][1]
        response_list.append(og_utterance_list[next_utterance_id + 1])

response_series = pd.Series(response_list)

response_series.to_excel(FINAL_PATH + "dailydialog_grade_groundtruth.xlsx")
print('total:', incomplete_count)