"""
Parse crowdsourced data from AMT to calculate IAA later - comparing common annotated HITs
& extracting corresponding values from the researchers
"""

from re import M
import pandas as pd
import glob
import os


GROUP_NO = 5
PATH = f"amt/amt_data/crowdsource_data_amtkappa/group{GROUP_NO}/"
DATA_FILE = f"group{GROUP_NO}_final_2.csv"
# DATA_FILE = "prompts_modified.csv"

amt_df = pd.read_csv(PATH + DATA_FILE)

unique_workers = amt_df.WorkerId.unique()

# Read researcher annotation data from the 400


# Give each prompt-response the amt_idx
amt_idx_list = []
skip_value = 7
for i in range(440):
    
    if i == skip_value:
        skip_value += 11
        continue

    amt_idx_list.append(i)

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

    checking_worker_dfs = []

    # Loop through all other workers in 
    for checking_worker in unique_workers:
        if unique_worker == checking_worker:
            continue

            
        # Extract data for the unique worker
        checking_worker_df = amt_df[amt_df['WorkerId'] == checking_worker]

        checking_worker_data = {
            'amt_idx': [],
            'prompt' : [],
            'response' : [],
            'appropriateness' : [],
            'info-content' : [],
            'humanlikeness' : [],
            
        }

        # Create list of amt_idx, prompt, response, app,info,human annotated
        for idx, hit_row in checking_worker_df.iterrows():
            for i in range(11):

                for list_name in checking_worker_data.keys():

                    if i==7:
                        continue

                    if list_name in ['amt_idx', 'prompt', 'response']:
                        temp_values = hit_row[f'Input.{i}_' + list_name]
                    else:
                        temp_values = hit_row[f'Answer.{i}_' + list_name]

                    # Check if the worker did multiple HITS
                    if isinstance(temp_values, pd.Series):
                        for hit_idx, hit in temp_values.iteritems():
                            checking_worker_data[list_name].append(hit)
                    else:
                        checking_worker_data[list_name].append(temp_values)
        
        # Create xlsx sheet for annotator in amt_idx, prompt, response, app, info, human format
        checking_worker_df = pd.DataFrame({
            'worker_name': checking_worker,
            'Appropriateness': checking_worker_data['appropriateness'],
            'Information content of outputs': checking_worker_data['info-content'],
            'Humanlikeness': checking_worker_data['humanlikeness'],
            'prompt': checking_worker_data['prompt'],
            'response': checking_worker_data['response'],
            'amt_idx': checking_worker_data['amt_idx']
        })


        # Read rater and create matching xlsx in amt_idx, prompt, response, app, info, human format
        checking_worker_filtered_df = checking_worker_df[checking_worker_df['amt_idx'].isin(worker_df['amt_idx'])]
        checking_worker_dfs.append(checking_worker_filtered_df)

    # Make directory with annotator name
    WORKER_PATH = PATH + unique_worker + '/'
    os.mkdir(PATH + unique_worker)

    for checking_worker_filtered_df in checking_worker_dfs:
        checking_worker_filtered_df.to_excel(WORKER_PATH + f"{checking_worker_filtered_df['worker_name'].iloc[0]}.xlsx", engine='openpyxl')
