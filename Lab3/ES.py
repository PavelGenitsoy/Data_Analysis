# -*- coding: utf-8 -*-
import json
import requests
from elasticsearch import Elasticsearch

# filename = 'C:\\Users\\Lenovo\\PycharmProjects\\Data_Analysis\\Lab1\\release_var\\format_rss_data.json'
filename = 'formatted_data.json'

res = requests.get('http://localhost:9200')
print(res.content)
es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])

# index = 1

file = open(filename, encoding='utf-8')
content = file.read()
# Send the data into es
for index, data in enumerate(json.loads(content)):
    res = es.index(index='final_index', ignore=400, id=index + 1, body=data)
    # index += 1
    if (index + 1) % 100 == 0:
        print(res)
file.close()

print("ALL DONE!")
# result_some = es.get(index='my_pavel_index', id=2)
# print(result_some['_source']['title'])
