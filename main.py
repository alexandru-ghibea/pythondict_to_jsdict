"""
How to convert dictionaries python dictionary to js dictionary 
"""
import pandas as pd
import os
import json
import re


path = os.getcwd()+"/S18items.xlsx"

df = pd.read_excel(path)
item_list = df.to_dict(orient="index")
# item_list2 = df.set_index("Type").to_dict(orient="records")


def save_file(dictionary, file_name):
    ''' Function that converts python dictionary into javascript dictionary '''
    json_str = json.dumps(dictionary, indent=4, ensure_ascii=False)
    remove_quotes = re.sub("\"([^\"]+)\":", r"\1:", json_str)
    file_name_cleaned = file_name.split(" ")[0]

    with open(file_name_cleaned + ".js", "w", encoding='utf_8') as outfile:
        outfile.write("export const " + file_name_cleaned +
                      " = " + remove_quotes + ";")


save_file(item_list, "test")
