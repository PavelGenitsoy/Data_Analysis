import json
import pandas as pd


with open('C:\\Users\\Lenovo\\PycharmProjects\\Data_Analysis\\Lab1\\release_var\\all_feed.txt', mode='r',
          encoding='utf-8') as file:
    text_buffer = file.read().splitlines()
    list_for_data, list_for_data_to_dict = [], []
    str_list = [x for x in text_buffer if len(x) > 0]
    dict_generic, dict1 = {}, {}
    flag1, flag2, flag3, flag4, last = False, False, False, False, False

    for index in range(len(str_list)):
        if index < len(str_list):
            if 'Date of publication: ' in str_list[index]:
                if not flag1:
                    flag1 = True
                list_for_data.append(str_list[index][len('Date of publication') + 2:])

            elif 'Title: ' in str_list[index]:
                if not flag2:
                    flag2 = True
                list_for_data.append(str_list[index][len('Title') + 2:])

            elif 'Link: ' in str_list[index]:
                if not flag3:
                    flag3 = True
                list_for_data.append(str_list[index][len('Link') + 2:])

            elif 'Summary: ' in str_list[index]:
                if not flag4:
                    flag4 = True

                if index < len(str_list) - 1:
                    inner_index = index + 1
                else:
                    last = True

                temp = ''
                if inner_index < len(str_list) and not last:
                    while 'From RSS-feed: ' not in str_list[inner_index]:
                        temp += str_list[inner_index]
                        inner_index += 1
                        if inner_index == len(str_list):
                            break
                list_for_data.append(str_list[index][len('Summary') + 2:] + temp)

            if flag1 and flag2 and flag3 and flag4:
                flag1, flag2, flag3, flag4 = False, False, False, False
                list_for_data_to_dict.append({'title': list_for_data[1], 'textBody': list_for_data[3],
                                              'pubDate': list_for_data[0], 'URL': list_for_data[2]})
                list_for_data = []

df = pd.DataFrame(list_for_data_to_dict).to_json(orient='records')
parsed = json.loads(df)
result = json.dumps(parsed, ensure_ascii=False, indent=4)

path_to_file = 'C:\\Users\\Lenovo\\PycharmProjects\\Data_Analysis\\Lab1\\release_var\\format_rss_data.json'

with open(path_to_file, mode='w', encoding='utf-8') as f:
    print(result, file=f)
    print("ALL DONE!")
