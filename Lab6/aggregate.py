from elasticsearch import Elasticsearch
import pandas as pd


es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])

body = \
    {
        'query': {
            'multi_match': {
                'query': 'Google',
                'fields': ['title', 'textBody']
            }
        },
        'aggregations': {
            'dates_with_holes': {
                'date_histogram': {
                    'field': 'pubDate',
                    'calendar_interval': 'day',
                    'min_doc_count': 0
                }
            }
        },
        'size': 1000
    }

res = es.search(index="final_index", body=body)

tmp_list_for_str, tmp_list_for_count = [], []
for dict in res['aggregations']['dates_with_holes']['buckets']:
    tmp_list_for_str.append(dict['key_as_string'][:10])
    tmp_list_for_count.append(dict['doc_count'])

dict_last_var = {'key_as_string': tmp_list_for_str, 'doc_count': tmp_list_for_count}
df = pd.DataFrame(data=dict_last_var)

df.to_excel('statistics.xlsx')

print("ALL DONE!")
