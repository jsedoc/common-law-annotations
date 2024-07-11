import pandas as pd
import glob

PATH = "./amt/amt_data/"
DATA_FILE = "prompts_de_emojified_group56_screening.xlsx"
# DATA_FILE = "prompts_modified.csv"
# NO_ROWS = 3 # Number of rows
ATTENTION_CHECKS = [7,17,27,37,47]
IDX_CHECKS = [6,16,26,36,46]
NO_QUESTIONS = 55

prompts_df = pd.read_excel(PATH + DATA_FILE, engine="openpyxl")


# Initialize prompts & responses. 10 prompt response + 1 attention check
ten_prompts = {
 }

for i in range(len(IDX_CHECKS)):
    ten_prompts[f'attention_check_prompt_{i}'] = []
    ten_prompts[f'attention_check_response_{i}'] = []
    ten_prompts[f'attention_check_amt_idx_{i}'] = []

for prompt_no in range(NO_QUESTIONS):    
    # if prompt_no == 7:
    if prompt_no in ATTENTION_CHECKS:
        continue
    ten_prompts[f'{prompt_no}_prompt'] = []
    ten_prompts[f'{prompt_no}_response'] = []
    ten_prompts[f'{prompt_no}_amt_idx'] = []

idx = 0
for prompt_no, row in prompts_df.iterrows():
    prompt_idx = idx % 55
    # prompt_idx = idx % 55

    ten_prompts[f'{prompt_idx}_prompt'].append(row['prompt'].replace('\n', '<br>'))
    ten_prompts[f'{prompt_idx}_response'].append(row['response'])
    ten_prompts[f'{prompt_idx}_amt_idx'].append(idx)

    idx += 1

    # Add attention check
    if prompt_idx in IDX_CHECKS:
        attention_check_id = IDX_CHECKS.index(prompt_idx)
        ten_prompts[f'attention_check_prompt_{attention_check_id}'].append('This is an attention check. Please enter the same annotation values as the previous question')
        ten_prompts[f'attention_check_response_{attention_check_id}'].append('This is an attention check. Please enter the same annotation values as the previous question')
        ten_prompts[f'attention_check_amt_idx_{attention_check_id}'].append(idx)
        idx += 1

    # if attention_counter == 9:
    #     new_prompts_list.append('This is an attention check. Please enter the same annotation values as the previous question')
    #     responses_list.append('This is an attention check. Please enter the same annotation values as the previous question')
    #     idx_list.append(idx)
    #     idx += 1
    #     attention_counter = 0


# Filler to make lengths equal
# ten_prompts[f'attention_check_prompt'].append('This is an attention check. Please enter the same annotation values as the previous question')
# ten_prompts[f'attention_check_response'].append('This is an attention check. Please enter the same annotation values as the previous question')
# ten_prompts[f'attention_check_amt_idx'].append(idx + 1)
# ten_prompts[f'10_prompt'].append('Filler')
# ten_prompts[f'10_response'].append('Filler')
# ten_prompts[f'10_amt_idx'].append(idx + 1)

prompt_response_df = pd.DataFrame(ten_prompts)
prompt_response_df.to_csv(PATH + f"prompts_modified_{NO_QUESTIONS}_group56_screening.csv", index=False)
