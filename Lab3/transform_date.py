import pandas as pd
import numpy as np
from datetime import datetime
import json

filename = 'C:\\Users\\Lenovo\\PycharmProjects\\Data_Analysis\\Lab1\\release_var\\format_rss_data.json'

df = pd.read_json(filename)
ar = np.array(df.pubDate)

tmp_list = []
for string in ar:
    tmp = string.split(' ')
    new_string = tmp[1] + tmp[2] + tmp[3] + tmp[4]
    dt_str = str(datetime.strptime(new_string, "%d%b%Y%H:%M:%S")).split(' ')
    new_dt_str = dt_str[0] + 'T' + dt_str[1] + 'Z'
    tmp_list.append(new_dt_str)

df.pubDate = tmp_list

parsed = json.loads(df.to_json(orient='records'))
result = json.dumps(parsed, ensure_ascii=False, indent=4)

with open('formatted_data.json', mode='w', encoding='utf-8') as f:
    print(result, file=f)
print("ALL DONE!")
