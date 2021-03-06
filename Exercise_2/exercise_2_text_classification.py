# -*- coding: utf-8 -*-
"""Exercise_2_Text Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EbeDuu-hpIZ6q-dyxHrJ74GM8MlDtc0z
"""

from urllib.request import urlopen
import json
import collections
import re
import string
import pandas as pd

url = "https://api.welcomesoftware.com/v2/feed/49e82ccda46544ff4e48a5fc3f04e343?format=json"
response = urlopen(url)
  
# storing the JSON response 
# from url in data
data_json = json.loads(response.read())

def remove_number(str):
    str = re.sub(r'[0-9]+', '', str)
    return str

def remove_comma_semi_colon(str):
    str = re.sub(r'[,:;\()]', '', str)
    return str

def split_with_hyphen(str):
    str = re.sub(r'-', ' ', str)
    return str

contents = dict()
count = {}
guid_map = {}
for x in data_json["entries"]:
  str = x["content"]
  guid_map[str["guid"]] = str
  str["title"] = remove_comma_semi_colon(str["title"])
  
  words = str["title"].split()
  words = [word.lower() for word in words]
  # print(words)
  for word in words:
    if word in count:
      count[word] += 1
    else:
      count[word] = 1
  contents[str["guid"]]=words
score = {}
for key in contents:
  sum=0
  for word in contents[key]:
    sum+=count[word]
  score[key] = sum

score = dict(sorted(score.items(), key=lambda kv: kv[1], reverse=True))

dd = collections.defaultdict(list)
for k,v in score.items():
    dd[v].append(k)
topScores = sorted(dd.items())
df = pd.DataFrame(columns=['Guid','Title','Related Image Urls','Publish Date','Creation Date','Recurrence count sum of words'])

for i in range(1, 4):
  value = topScores[-i][0]
  guids = topScores[-i][1]
  for guid in guids:
    content = guid_map[guid]
    image_urls = []
    for image in content["images"]:
      image_urls.append(image["url"])
    row = {'Guid': content["guid"], 'Title': content["title"], 
           'Related Image Urls': ",".join(image_urls),
           'Publish Date': content["published_at"],
           'Creation Date': content["created_at"],
           'Recurrence count sum of words': value}
    df = df.append(row, ignore_index=True)

df.to_csv('reccurrence.csv', index=False)