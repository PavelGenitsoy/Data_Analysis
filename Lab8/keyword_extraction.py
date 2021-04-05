from elasticsearch import Elasticsearch
import re
import numpy as np

es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])

body = \
    {
        'query': {
            'multi_match': {
                'query': 'Microsoft',
                'fields': ['title', 'textBody']
            }
        },
        'size': 1000
    }

res = es.search(index="final_index", body=body)

all_word_list = ""
for it, i_dict in enumerate(res['hits']['hits']):
    all_word_list += " " + i_dict['_source']['title'] + " " + i_dict['_source']['textBody']

all_word_list = all_word_list.lower()

t = re.sub(r"&nbsp;", " ", all_word_list)
t = re.sub(r"<p>", " ", t)
t = re.sub(r"&#[0-9][0-9][0-9][0-9];", " ", t)

save_str = ""
flag = True
tmp_str = t
while flag:
    left_part_string, _, right_part_string = tmp_str.partition('<')
    save_str += " " + left_part_string
    if '>' in right_part_string:
        right_part_string = right_part_string[right_part_string.find('>')+1:]
        tmp_str = right_part_string
    else:
        flag = False

formatted_save_str = re.sub(r"читать дальше &rarr;", " ", save_str)
formatted_save_str = re.sub(r"ещ", " ", formatted_save_str)

save_str_ = ""
flag_ = True
tmp_str_ = formatted_save_str
while flag_:
    left_part_string, _, right_part_string = tmp_str_.partition('&')
    save_str_ += " " + left_part_string
    if ';' in right_part_string:
        right_part_string = right_part_string[right_part_string.find(';')+1:]
        tmp_str_ = right_part_string
    else:
        flag_ = False
save_str_ = save_str_[:-17]

str_last_var = list(filter(None, re.split(r"[^a-zа-я]", save_str_)))
str_last_var = [x for x in str_last_var if len(x) > 1]

count = 0
dict_original_word = {}
for word in str_last_var:
    if word not in dict_original_word.keys():
        dict_original_word[word] = count
        count += 1

dict_for_repeat_word = {}
for unique_word in dict_original_word.keys():
    amount_repeat_word = (np.array(str_last_var) == unique_word).sum()
    dict_for_repeat_word[unique_word] = amount_repeat_word

with open('stop-words_russian_1_ru.txt', encoding='utf-8') as file:
    list_stop_words_ru = [line.rstrip() for line in file.readlines()]
    list_stop_words_ru[0] = 'а'

with open('stop-words_english_1_en.txt', encoding='utf-8') as file:
    list_stop_words_en = [line.rstrip() for line in file.readlines()]
    list_stop_words_en[0] = 'able'

list_stop_words = list_stop_words_ru + list_stop_words_en

counter, max_lim = 1, 30
sorted_dict = {}
sorted_keys = sorted(dict_for_repeat_word, key=dict_for_repeat_word.get, reverse=True)  # [1, 3, 2]
with open('output.txt', 'w', encoding='utf-8') as file:
    for word in sorted_keys:
        sorted_dict[word] = dict_for_repeat_word[word]
        internal_flag = True
        for i in range(len(list_stop_words)):
            if list_stop_words[i] == word:
                internal_flag = False
        if internal_flag:
            if counter == 1:
                print("A list of the 30 most important words on the topic identified by Microsoft:\n", file=file)
            print(f"\t{counter}) {word} - {sorted_dict[word]}", file=file)
            counter += 1
        if counter > max_lim:
            break

print("ALL DONE")
