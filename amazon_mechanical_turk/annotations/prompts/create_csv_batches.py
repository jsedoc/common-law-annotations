"""
Create CSV file containing prompts to be used for Amazon Mechanical Turk.
Enters randomized checks + creates batches of csv files - ie. batches of 10, 100, 1000..

Puts csv files in a new directory, titled amt_10, amt_100, amt_1000, where amt_x contains csv of x lines,
including one attention check per 9 
"""

import codecs
import os

from numpy import source

PATH = 'amt/amt_data/prompts/'
FILE_NAME = 'prompts_modified_emoji.csv'
BATCH_SIZE = 50

BATCH_PATH = PATH + "amt_" + str(BATCH_SIZE) + "/"

# Create directory
try:
    os.mkdir(BATCH_PATH)
except FileExistsError:
    print('Dir exists, moving on..')


with codecs.open(PATH + FILE_NAME, encoding='utf-8') as source_file:

    batch_number = 0
    batch_lines = []  # List of lines to store for each batch csv
    lines = source_file.readlines()
    header = ""
    for idx, line in enumerate(lines):

        # Save the header
        if idx == 0:
            header = line
            continue

        batch_lines.append(line)

        if len(batch_lines) == BATCH_SIZE:
            with codecs.open(BATCH_PATH + 'amt_' + str(BATCH_SIZE) + '_' + str(batch_number) + '.csv', 'w', encoding='utf-8') as file:
                file.write(header)
                file.writelines(batch_lines)
                batch_lines = []
                batch_number += 1


# with codecs.open(PATH + FILE_NAME, encoding='utf-8') as source_file:

#     batch_number = 0
#     batch_lines = [] # List of lines to store for each batch csv
#     lines = source_file.readlines()
#     header = ""
#     for idx, line in enumerate(lines):
#         if idx == 0:
#             header = line
#             continue
#         batch_lines.append(line)

#         if len(batch_lines) == BATCH_SIZE:
#             with codecs.open(BATCH_PATH + 'amt_' + str(BATCH_SIZE) + '_' + str(batch_number) + '.csv', 'w', encoding='utf-8') as file:
#                 file.write(header)
#                 file.writelines(batch_lines)
#                 batch_lines = []
#                 batch_number += 1
