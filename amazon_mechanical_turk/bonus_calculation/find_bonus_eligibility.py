"""
Creates a sheet of workers that are eligible for a bonus
- Worker ID
- How many HITS they completed
"""

from re import M
import pandas as pd
import glob
import os


GROUPS = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "5_2",
    "6_2",
    "5_3",
]
for GROUP_NO in GROUPS:

    SOURCE_PATH = f"amt/amt_data_final/"
    FINAL_PATH = f"amt/amt_data_final/counts/"
    DATA_FILE = f"commonlaw_group{GROUP_NO}_final.csv"
    # DATA_FILE = "prompts_modified.csv"

    amt_df = pd.read_csv(SOURCE_PATH + DATA_FILE)
    count_df = amt_df.WorkerId.value_counts()

    count_df.to_excel(FINAL_PATH + f"count_{GROUP_NO}.xlsx", engine="openpyxl")

    print(amt_df.size)
    # Read researcher annotation data from the 400
