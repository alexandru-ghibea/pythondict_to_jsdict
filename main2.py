"""
How to convert excel worksheets to python dictionary and then convert it to javascript dictionary

"""
import pandas as pd
import numpy as np
import os
import json
import re
from sqlalchemy import create_engine
# create database connection
engine = create_engine('sqlite:///my_database.db')

file_path = os.getcwd()+"/item_original.xlsx"

df = pd.read_excel(file_path)
item_list = df.to_dict(orient="records")
item_list2 = df.set_index("Section").to_dict(orient="records")


def save_file(dictionary, file_name):
    ''' Function that converts python dictionary into javascript dictionary  where dictionary is the dict that we want to modify to js format
    and file_name is the name of the file where we will save it
    '''
    json_str = json.dumps(dictionary, indent=4, ensure_ascii=False)
    remove_quotes = re.sub("\"([^\"]+)\":", r"\1:", json_str)
    file_name_cleaned = file_name.split(" ")[0]

    with open(file_name_cleaned + ".ts", "w", encoding='utf_8') as outfile:
        outfile.write("export const " + file_name_cleaned +
                      " = " + remove_quotes + ";")


# Load Excel file using Pandas
f = pd.ExcelFile(file_path)

# Define an empty list to store individual DataFrames
list_of_dfs = []

# Iterate through each worksheet
for sheet in f.sheet_names:

    # Parse data from each worksheet as a Pandas DataFrame
    df = f.parse(sheet)
# And append it to the list
    list_of_dfs.append(df)


# Combine all DataFrames into one
data = pd.concat(list_of_dfs, ignore_index=True)
# write the data frame to the data base
data.to_sql("data", engine, if_exists='replace')
print(engine.execute("select * from data").fetchone())
# save the merged DataFrames
save_file(data.to_dict(orient="records"), "test_data_frame")

# Save each Data Frame to a single file
dicts = []

# iterate through each data frames
for item in list_of_dfs:
    # transform the data frame to dictionary
    item_dict = item.to_dict(orient="records")
    dicts.append(item_dict)

# iterate through each dictionary
for i in range(len(dicts)):
    save_file(dicts[i], f"sheet{i}")
