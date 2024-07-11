"""
Calculate cross-group             
"""

from re import M
import pandas as pd
import glob
import os


GROUP_NO = 2
PATH = f"amt/amt_data/crowdsource_data/group{GROUP_NO}/"
DATA_FILE = f"group{GROUP_NO}_final.csv"
# DATA_FILE = "prompts_modified.csv"

amt_df = pd.read_csv(PATH + DATA_FILE)

unique_workers = amt_df.WorkerId.unique()

# Read researcher annotation data from the 400

# Build final path to dataset
RESEARCHER_PATH = f"data_scripts/annotations/round6/group{GROUP_NO}/"

# Use glob to grab all .xlsx files
xlsx_files = glob.glob(RESEARCHER_PATH + '*.xlsx')

researcher_df_list = []
for xlsx_annotator in xlsx_files:
    researcher_df_list.append(pd.read_excel(xlsx_annotator, engine="openpyxl"))

# Give each prompt-response the amt_idx
amt_idx_list = []
skip_value = 7
for i in range(440):
    
    if i == skip_value:
        skip_value += 11
        continue

    amt_idx_list.append(i)

researcher_df_list[0]['amt_idx'] = pd.Series(amt_idx_list)
# researcher_df_list[1]['amt_idx'] = pd.Series(amt_idx_list)

for unique_worker in unique_workers:

    # Extract data for the unique worker
    worker_df = amt_df[amt_df['WorkerId'] == unique_worker]

    worker_data = {
        'amt_idx': [],
        'prompt' : [],
        'response' : [],
        'appropriateness' : [],
        'info-content' : [],
        'humanlikeness' : [],
        
    }

    # Create list of amt_idx, prompt, response, app,info,human annotated
    for idx, hit_row in worker_df.iterrows():
        for i in range(11):

            for list_name in worker_data.keys():

                if i==7:
                    continue

                if list_name in ['amt_idx', 'prompt', 'response']:
                    temp_values = hit_row[f'Input.{i}_' + list_name]
                else:
                    temp_values = hit_row[f'Answer.{i}_' + list_name]

                # Check if the worker did multiple HITS
                if isinstance(temp_values, pd.Series):
                    for hit_idx, hit in temp_values.iteritems():
                        worker_data[list_name].append(hit)
                else:
                    worker_data[list_name].append(temp_values)
    
    # Create xlsx sheet for annotator in amt_idx, prompt, response, app, info, human format
    worker_df = pd.DataFrame({
        'Appropriateness': worker_data['appropriateness'],
        'Information content of outputs': worker_data['info-content'],
        'Humanlikeness': worker_data['humanlikeness'],
        'prompt': worker_data['prompt'],
        'response': worker_data['response'],
        'amt_idx': worker_data['amt_idx']
    })

    # Read rater and create matching xlsx in amt_idx, prompt, response, app, info, human format
    rater_1_filtered_df = researcher_df_list[0][researcher_df_list[0]['amt_idx'].isin(worker_df['amt_idx'])]
    # rater_2_filtered_df = researcher_df_list[1][researcher_df_list[1]['amt_idx'].isin(worker_df['amt_idx'])]

    # Make directory with annotator name
    WORKER_PATH = PATH + unique_worker + '/'
    os.mkdir(PATH + unique_worker)

    rater_1_filtered_df.to_excel(WORKER_PATH + 'rater1.xlsx', engine='openpyxl')
    # rater_2_filtered_df.to_excel(WORKER_PATH + 'rater2.xlsx', engine='openpyxl')
    worker_df.to_excel(WORKER_PATH + unique_worker + '.xlsx', engine='openpyxl')

