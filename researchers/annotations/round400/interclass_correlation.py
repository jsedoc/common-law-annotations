import pingouin as pg
import pandas as pd
import glob

PATH = "/Users/seunggunlee/nyu/research/research_sedoc/data_scripts/annotations/round400/"
GROUP_NO = 5
FINAL_PATH = PATH + f"group{GROUP_NO}/"

xlsx_files = glob.glob(FINAL_PATH + '*.xlsx')

for xlsx_file in xlsx_files:
    df = pd.read_excel(xlsx_file)

data = pg.read_dataset("icc")
print(data)


# targets = category (app, human, )
# raters = 2 different raters
# ratings = 1 ~ 5