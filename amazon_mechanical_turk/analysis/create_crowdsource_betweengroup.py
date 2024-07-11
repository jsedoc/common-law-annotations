"""
Parse crowdsourced data from AMT to calculate IAA later - comparing common annotated HITs
& extracting corresponding values from the researchers
"""

from re import M
import pandas as pd
import glob
import os


GROUP_NO = 5
GROUP_NO2 = 6
PATH1 = f"amt/amt_data/crowdsource_data/group{GROUP_NO}/"
DATA_FILE1 = f"group{GROUP_NO}_amt.csv"
PATH2 = f"amt/amt_data/crowdsource_data/group{GROUP_NO2}/"
FINAL_PATH = f"amt/amt_data/crowdsource_data/between_group_kappa/"
DATA_FILE2 = f"group{GROUP_NO2}_amt.csv"
# DATA_FILE = "prompts_modified.csv"

amt_df1 = pd.read_csv(PATH1 + DATA_FILE1)
amt_df2 = pd.read_csv(PATH2 + DATA_FILE2)

groups_list = [amt_df1, amt_df2]
groups_list_workers = [[], []]
for group_idx, amt_df in enumerate(groups_list):

    unique_workers = amt_df.WorkerId.unique()

    # Read researcher annotation data from the 400

    # Build path to researcher dataset
    RESEARCHER_PATH = f"data_scripts/annotations/round2/group{GROUP_NO}/"

    # Use glob to grab all .xlsx files
    xlsx_files = glob.glob(RESEARCHER_PATH + '*.xlsx')

    researcher_df_list = []
    for xlsx_annotator in xlsx_files:
        researcher_df_list.append(pd.read_excel(
            xlsx_annotator, engine="openpyxl"))

    # Give each prompt-response the amt_idx
    amt_idx_list = []
    skip_value = 7
    ATTENTION_CHECKS = [7, 17, 27, 37, 47]
    # 45, 46, 48, 49, ... 54

    # CREATING AMT IDs for RESEARCHERS.
    for unique_worker in unique_workers:

        # Extract data for the unique worker
        worker_df = amt_df[amt_df['WorkerId'] == unique_worker]

        worker_data = {
            'amt_idx': [],
            'prompt': [],
            'response': [],
            'appropriateness': [],
            'info-content': [],
            'humanlikeness': [],

        }

        # Create list of amt_idx, prompt, response, app,info,human annotated
        for idx, hit_row in worker_df.iterrows():
            for i in range(55):

                for list_name in worker_data.keys():

                    if i in ATTENTION_CHECKS:
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

        groups_list_workers[group_idx].append(worker_df)


worker_list_1 = groups_list_workers[0]
worker_list_2 = groups_list_workers[1]

for idx1, worker1 in enumerate(worker_list_1):
    for idx2, worker2 in enumerate(worker_list_2):

        indices1 = worker1['amt_idx'].isin(worker2['amt_idx'])
        worker_df_new1 = worker1[indices1]

        indices2 = worker2['amt_idx'].isin(worker1['amt_idx'])
        worker_df_new2 = worker2[indices2]
        WORKER_PATH = FINAL_PATH + "final_" + str(idx1) + "_" + str(idx2) + '/'

        os.mkdir(WORKER_PATH)

        # Make directory with annotator name

        worker_df_new1.to_excel(WORKER_PATH + 'rater1.xlsx', engine='openpyxl')
        worker_df_new2.to_excel(WORKER_PATH + 'rater2.xlsx', engine='openpyxl')
