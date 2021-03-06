# -*- coding: utf-8 -*-
"""CSV to JSON.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yGSZqSgUg-wMrtZeakotBayHyD2mj5tn
"""

from os import sep
import pandas as pd
import json

data = {}
pd.options.display.max_colwidth = 190  # set a value as your need

def remove_empty_elements(d):
  """recursively remove empty lists, empty dicts, or None elements from a dictionary"""
  def empty(x):
    return x is None or x == {} or x == [] or x ==''
  if not isinstance(d, (dict, list)):
    return d
  elif isinstance(d, list):
    return [v for v in (remove_empty_elements(v) for v in d) if not empty(v)]
  else:
    return {k: v for k, v in ((k, remove_empty_elements(v)) for k, v in d.items()) if not empty(v)}

df = pd.read_excel(r'MappingDocumentExercise.xlsx')
df[['WelcomeLabel', 'OtherSoftwareTag', 'CountryLevel']] = pd.DataFrame(df['WelcomeLabel,OtherSoftwareTag,CountryLevel'].str.split(',').tolist())
df = df.iloc[: , 1:]
df['json'] = df.apply(lambda x: x.to_json(), axis=1)
# print(df["json"])
data = df["json"].to_list()
# print(data)
str = ",".join(data)
str = "[" + str + "]"
# print(str)
json_object = json.loads(str)
# print(json_object)
json_object = remove_empty_elements(json_object)
# print(type(json_object))
json_string = json.dumps(json_object)
with open("output.json", "w") as outfile:
  outfile.write(json_string)