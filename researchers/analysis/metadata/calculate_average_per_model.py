"""
Calculates average annotation rating per model - per group. Researchers
"""

import itertools

from sklearn.metrics import cohen_kappa_score
import numpy as np
import glob
import pandas as pd
import matplotlib.pyplot as plt

# File path to annotations folder
# BASE_PATH = './data_scripts/annotations/'
BASE_PATH = "/commonlaw/researchers/annotations/group56/"

NUMBER_OF_ROUNDS = 6
NUMBER_OF_GROUPS = 2

ANNOTATION_CATEGORIES = ['Appropriateness',
                         'Information content of outputs', 'Humanlikeness']
# Possible Cohen's Kappa Calculation Combos:
# 1. Same round, within group (in two's)
# 2. Same round, everyone
# 2. Different rounds, same person (see how much the agreement changes)
# 2. Same round, across groups (average groups - calculate kappa across groups)


# ------- CALUCLATE COHEN'S KAPPA -------

# Data for all ratings
raters_appropriateness = []
raters_information = []
raters_humanness = []

# For each group, calculate their cohen's kappa
# for group_no in range(1, NUMBER_OF_GROUPS+1):

final_df = pd.DataFrame({
    'model': [], 'Appropriateness': [], 'Information content of outputs': [], 'Humanlikeness': [], 'round': [], 'group': []
})

for ROUND_NUMBER in range(1, NUMBER_OF_ROUNDS + 1):

    if ROUND_NUMBER == 6:
        ROUND_NUMBER = 400
    # Read model list df
    MODEL_LIST_PATH = f"data_scripts/annotations/model_names/round{ROUND_NUMBER}_models.xlsx"
    models_df = pd.read_excel(MODEL_LIST_PATH, engine="openpyxl")

    for GROUP_NO in range(1, NUMBER_OF_GROUPS + 1):

        # Build final path to dataset
        FINAL_PATH = BASE_PATH + 'round' + \
            str(ROUND_NUMBER) + '/group' + str(GROUP_NO) + '/'

        # Use glob to grab all .xlsx files
        xlsx_files = glob.glob(FINAL_PATH + '*.xlsx')

        for xlsx_file in xlsx_files:
            annotator_df = pd.read_excel(xlsx_file, engine="openpyxl")

            annotator_df = annotator_df[[
                'model', 'Appropriateness', 'Information content of outputs', 'Humanlikeness']]

            # Append the model column
            annotator_df["model"] = annotator_df["model"]

            # Calculate category average
            mean_df = annotator_df.groupby(["model"]).mean().reset_index()
            mean_df["round"] = ROUND_NUMBER
            mean_df["group"] = GROUP_NO

            final_df = final_df.append(mean_df, ignore_index=True)
            # Convert each column (series) into lists

# final_df = final_df.groupby(["group", "round"]).mean()
final_df.to_csv(
    "commonlaw/researchers/analysis/metadata/means/means_56.csv")
final_df.groupby(["group", "model"]).mean().to_csv(
    "commonlaw/researchers/analysis/metadata/means/means_grouped_56.csv")
