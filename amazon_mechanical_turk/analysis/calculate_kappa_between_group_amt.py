"""
Calculate AVERAGE Cohen's Kappa between annotators of DIFFERENT groups. Parse groupx_amt.csv and find common AMT ID's

"""

from re import M
from tkinter import W
import pandas as pd
import itertools
from itertools import combinations
import numpy as np
from sklearn.metrics import cohen_kappa_score

# Give each prompt-response the amt_idx
skip_value = 7
# TOTAL_NUM_QUESTIONS = 55
# ATTENTION_CHECKS = [7,17,27,37,47]
TOTAL_NUM_QUESTIONS = 11
ATTENTION_CHECKS = [7]
CATEGORIES = ["appropriateness", "humanlikeness", "info-content"]
FINAL_PATH = f"amt/amt_data/crowdsource_data/between_group_kappa/"

# 45, 46, 48, 49, ... 54

# Dictionary to store all average Cohen's Kappa values for each user_user combo
all_kappas_dict = {}
for CATEGORY in CATEGORIES:
    all_kappas_dict[CATEGORY] = []
all_kappas_index = []

for GROUP_NO in range(1, 5):
    for GROUP_NO2 in range(1, 5):
        if GROUP_NO == GROUP_NO2:
            continue

        PATH1 = f"commonlaw/amazon_mechanical_turk/amt_data/crowdsource_data/group{GROUP_NO}/"
        DATA_FILE1 = f"group{GROUP_NO}_amt.csv"
        PATH2 = f"commonlaw/amazon_mechanical_turk/amt_data/crowdsource_data/group{GROUP_NO2}/"
        DATA_FILE2 = f"group{GROUP_NO2}_amt.csv"

        # DATA_FILE = "prompts_modified.csv"

        amt_df1 = pd.read_csv(PATH1 + DATA_FILE1)
        amt_df2 = pd.read_csv(PATH2 + DATA_FILE2)

        amt_df_list = [amt_df1, amt_df2]

        # List of each group's workers and their annotations
        worker_annotation_dicts = []  # size 2, one for each group

        for amt_df in amt_df_list:

            unique_workers = amt_df.WorkerId.unique()
            annotation_dicts = []

            # Extract annotations for each unique worker
            for unique_worker in unique_workers:

                # Dictionary to store annotation value of each amt idx prompt
                # idx_category
                annotation_dict = {}

                # Extract data for the unique worker
                worker_df = amt_df[amt_df['WorkerId'] == unique_worker]

                # Create list of amt_idx, prompt, response, app,info,human annotated
                for idx, hit_row in worker_df.iterrows():
                    for i in range(TOTAL_NUM_QUESTIONS):  # Loop through each question

                        # Skip attention check
                        if i in ATTENTION_CHECKS:
                            continue

                        # For each annotation category, store the annotation value
                        for CATEGORY in CATEGORIES:
                            amt_idx = hit_row[f"Answer.{i}_amt_idx"]
                            annotation_dict[f"{amt_idx}_{CATEGORY}"] = hit_row[f"Answer.{i}_{CATEGORY}"]

                annotation_dicts.append(annotation_dict)

            worker_annotation_dicts.append(annotation_dicts)

        group1_annotation_dicts = worker_annotation_dicts[0]
        group2_annotation_dicts = worker_annotation_dicts[1]

        worker_combinations = itertools.product(
            group1_annotation_dicts, group2_annotation_dicts)

        # Calculate Cohen's Kappa for each unique worker pair in annotation_dicts:
        kappa_values = {}
        for CATEGORY in CATEGORIES:
            kappa_values[CATEGORY] = []

        for worker_combination in worker_combinations:

            worker_0 = worker_combination[0]
            worker_1 = worker_combination[1]

            # Calculate Cohen's Kappa for each category
            for CATEGORY in CATEGORIES:
                # Fill array of each worker's annotations. 2D
                raters = [[], []]
                for idx in range(500):
                    amt_idx = f"{idx}_{CATEGORY}"

                    # If either of the workers did NOT annotate the prompt, skip
                    if (amt_idx not in worker_0) or (amt_idx not in worker_1):
                        continue

                    raters[0].append(worker_0[amt_idx])
                    raters[1].append(worker_1[amt_idx])

                data = np.zeros((len(raters), len(raters)))

                # Calculate cohen_kappa_score for every combination of raters
                # Combinations are only calculated j -> k, but not k -> j, which are equal
                # So not all places in the matrix are filled.
                labels = [1, 2, 3, 4, 5]
                for j, k in list(itertools.combinations(range(len(raters)), r=2)):
                    data[j, k] = cohen_kappa_score(
                        raters[j], raters[k], weights='linear', labels=labels)
                # [[0.        , 0.11764706, 0.        ],
                #  [0.        , 0.        , 0.25      ],
                #  [0.        , 0.        , 0.        ]]

                # ------- PLOT DATA -------
                # scores_dict[annotation_category].append(data[0][1])

                if not np.isnan(data[0][1]):
                    kappa_values[CATEGORY].append(data[0][1])

        kappa_df = pd.DataFrame(kappa_values)

        # Calculate the mean Kappa values for each category
        average_s = kappa_df.mean()

        all_kappas_index.append(f"{GROUP_NO}_{GROUP_NO2}")

        # Append the user combo's average kappa
        for CATEGORY in CATEGORIES:
            all_kappas_dict[CATEGORY].append(average_s[CATEGORY])
        # kappa_df.to_excel(FINAL_PATH + f"{GROUP_NO}_{GROUP_NO2}_between_kappa.xlsx", engine='openpyxl')
        # Calculate Cohen's Kappa


print(all_kappas_dict)
df = pd.DataFrame(all_kappas_dict, index=all_kappas_index)
df.to_excel(FINAL_PATH + f"all_groups_between_kappa.xlsx", engine='openpyxl')