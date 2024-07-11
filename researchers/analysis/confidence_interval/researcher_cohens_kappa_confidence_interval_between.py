"""
Creates 3 CSV files  required to calculate the Confidence Interval for Cohen's Kappa, for RESEARCHERS
Each CSV holds annotations of ONE category for TWO annotators, belonging to DIFFERENT groups (BETWEEN)
3 Categories --> Total of 3 CSV Files
Related Slack : https://j-codes.slack.com/archives/C02UA64TJCX/p1666198962473619
Columns : The annotation category of two different annotators
No. of Cols : 2
No. of Rows : Unlimited. Each row is an annotation of an item

Read files

Create Dataframe
"""

import pandas as pd
from itertools import combinations
import glob

# ATTENTION_CHECKS = [7,17,27,37,47]
TOTAL_NUM_QUESTIONS = 11
ATTENTION_CHECKS = [7]
CATEGORIES = ["Appropriateness", "Humanlikeness",
              "Information content of outputs"]

ROUND_NO = 400
FINAL_PATH = f"commonlaw/researchers/analysis/confidence_interval/results/between/"

all_annotations_dict = {}

for GROUP_NO in range(2, 5):
    PATH = f"data_scripts/annotations/round{ROUND_NO}/group{GROUP_NO}/"

    # Extract annotations for each annotator
    xlsx_files = glob.glob(PATH + '*.xlsx')
    annotation_dfs = []

    for xlsx_file in xlsx_files:
        annotation_df = pd.read_excel(xlsx_file, engine="openpyxl")
        annotation_dfs.append(annotation_df)

    # Create a combined CSV for annotations for each category
    for CATEGORY in CATEGORIES:
        annotations_1 = list(annotation_dfs[0][CATEGORY])
        annotations_2 = list(annotation_dfs[1][CATEGORY])

        all_annotations_dict[f"{GROUP_NO}_{CATEGORY}_0"] = annotations_1
        all_annotations_dict[f"{GROUP_NO}_{CATEGORY}_1"] = annotations_2

worker_combinations = [comb for comb in combinations(
    all_annotations_dict.keys(), 2) if (comb[0][0] != comb[1][0]) and (comb[0][3] == comb[1][3])]

for worker_combination in worker_combinations:

    combined_df = pd.DataFrame(
        {"annotator1": all_annotations_dict[worker_combination[0]], "annotator2": all_annotations_dict[worker_combination[1]]})

    CATEGORY = worker_combination[0].split("_")[1]
    if CATEGORY.isnumeric():
        print(CATEGORY)
    combined_df.to_csv(
        FINAL_PATH + f"{worker_combination[0][0]}_{worker_combination[1][0]}_{worker_combination[0][-1]}{worker_combination[1][-1]}_{CATEGORY}.csv", index=False)
