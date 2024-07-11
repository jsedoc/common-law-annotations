'''
Calculate Cohen's kappa for Crowdsourced data
'''

import itertools
import statistics
from sklearn.metrics import cohen_kappa_score
import numpy as np
import glob
import pandas as pd
import os

# File path to annotations folder
# BASE_PATH = './data_scripts/annotations/'
GROUP_NO = 5
# BASE_PATH = f"amt/amt_data/crowdsource_data/group{GROUP_NO}/"
BASE_PATH = f"amt/amt_data/crowdsource_data/between_group_kappa/"

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
turker_ids = []

# For each group, calculate their cohen's kappa
# for group_no in range(1, NUMBER_OF_GROUPS+1):

workers_paths = glob.glob(BASE_PATH + '*/')

# Average agreement
scores_dict = {
    'Appropriateness': [],
    'Information content of outputs': [],
    'Humanlikeness': [],
    'worker_name': []
}


# For each worker
for worker_path in workers_paths:

    worker_dict = {
        'Appropriateness': [],
        'Information content of outputs': [],
        'Humanlikeness': [],
    }

    # Calculate the agreement
    # Use glob to grab all .xlsx files
    # [researcher1, Amazon worker, researcher2]
    xlsx_files = glob.glob(worker_path + '*.xlsx')

    # Pair Turker with each rater
    if GROUP_NO == 1:
        researcher_set = [xlsx_files]
    else:
        researcher_set = [
            [xlsx_files[0], xlsx_files[1]],  # rater2, amt
            # [xlsx_files[2], xlsx_files[1]], # rater1, amt
        ]

    # For each unique turker-researcher pair
    for turker_researcher_pair in researcher_set:

        # For each annotation category, compile annotations
        for annotation_category in ANNOTATION_CATEGORIES:

            # Read xlsx files into pandas dataframe
            raters = []

            for xlsx_annotator in turker_researcher_pair:
                annotator_df = pd.read_excel(xlsx_annotator, engine="openpyxl")

                print(annotation_category)

                # Convert each column (series) into lists
                annotations = annotator_df[annotation_category].tolist()

                raters.append(annotations)

            # Test
            # raters = [[3,2,3,4,5],[1,2,3,4,5]]

            data = np.zeros((len(raters), len(raters)))

            # Calculate cohen_kappa_score for every combination of raters
            # Combinations are only calculated j -> k, but not k -> j, which are equal
            # So not all places in the matrix are filled.
            labels = [1, 2, 3, 4, 5]
            for j, k in list(itertools.combinations(range(len(raters)), r=2)):
                data[j, k] = cohen_kappa_score(
                    raters[j][:50], raters[k][:50], weights='linear', labels=labels)
            # [[0.        , 0.11764706, 0.        ],
            #  [0.        , 0.        , 0.25      ],
            #  [0.        , 0.        , 0.        ]]

            # ------- PLOT DATA -------
            # scores_dict[annotation_category].append(data[0][1])
            worker_dict[annotation_category].append(data[0][1])
            print(data)

    # Calculate average of worker scores across two annotators
    for annotation_category in ANNOTATION_CATEGORIES:
        scores_dict[annotation_category].append(
            statistics.mean(worker_dict[annotation_category]))
        # scores_dict[annotation_category].append(max(worker_dict[annotation_category]))
    scores_dict['worker_name'].append(worker_path.split('/')[-2])

# for category in scores_dict.keys():
#     print(category, sum(scores_dict[category]) / len(scores_dict[category]))
#     print(category, 'median', statistics.median(scores_dict[category]))

df = pd.DataFrame(scores_dict)
df.to_excel(BASE_PATH + f'{GROUP_NO}_histogram.xlsx', engine='openpyxl')
print(df.shape)
