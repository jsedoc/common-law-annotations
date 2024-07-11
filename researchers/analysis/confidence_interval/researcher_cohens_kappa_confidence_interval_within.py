"""
Creates 3 CSV files  required to calculate the Confidence Interval for Cohen's Kappa, for RESEARCHERS
Each CSV holds annotations of ONE category for TWO annotators, belonging to the SAME group (WITHIN)
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
FINAL_PATH = f"commonlaw/researchers/analysis/confidence_interval/results/within/"

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

        combined_df = pd.DataFrame(
            {"annotator1": annotations_1, "annotator2": annotations_2})

        combined_df.to_csv(
            FINAL_PATH + f"{GROUP_NO}_{CATEGORY}.csv", index=False)
