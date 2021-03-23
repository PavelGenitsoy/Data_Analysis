import feedparser


def grep(filename, pattern):
    for n, line in enumerate(open(filename, encoding='utf-8')):
        if pattern in line:
            return True
    return False


def parse_rss(link_main):
    link_of_source = feedparser.parse(link_main)
    path_to_file = 'C:\\Users\\Lenovo\\PycharmProjects\\Data_Analysis\\Lab1\\habr.txt'

    x_left = link_main.find("//") + 2
    x_right = link_main.find("/", x_left)

    with open(path_to_file, mode="a+", encoding='utf-8') as f:
        for _, val in reversed(list(enumerate(link_of_source.entries))):
            flag = False

            if not grep(path_to_file, val.link):
                try:
                    temp_val = val.summary.rfind('\n') - val.summary.find('\n') + 1

                    if temp_val > 1:
                        flag = True
                        var = val.summary[val.summary.find('\n'):val.summary.rfind('\n'):1]
                        summary_upd = val.summary.replace(var, '')

                    if flag:
                        print('Date of publication: ' + val.published + '\n' + 'Title: ' + val.title + '\n' + 'Link: ' +
                              val.link + '\n' + 'Summary: ' + summary_upd + '\n\n\n', file=f)
                    else:
                        print('Date of publication: ' + val.published + '\n' + 'Title: ' + val.title + '\n' + 'Link: ' +
                              val.link + '\n' + 'Summary: ' + val.summary + '\n\n\n', file=f)

                    print(f'{link_main[x_left:x_right:1]} --> added new info: \n{val.title}\n{val.link}\n\n')
                except AttributeError:
                    pass
            else:
                pass


if __name__ == '__main__':
    with open('C:\\Users\\Lenovo\\PycharmProjects\\Data_Analysis\\Lab1\\ref.txt', mode='r', encoding='utf-8') as file:
        for link in file.readlines():
            parse_rss(link)
