import cgi
from elasticsearch import Elasticsearch


form = cgi.FieldStorage()
query = form.getfirst("query", "Query not defined")
src = form.getfirst("src", "Source not defined")


es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])


body = \
    {
        'query': {
            'bool': {
                'must': [
                    {
                        'multi_match': {
                            'query': query,
                            'fields': ['title', 'textBody']
                        }
                    }
                ],
                'filter': [
                    {
                        'match': {
                            'URL': src
                        }
                    }
                ]
            }
        },
        'size': 100
    }

res = es.search(index="my_pavel_index", body=body)

print("Content-type: text/html\n\n\n<html><body bgcolor=#00ffff >")
print("""<!DOCTYPE HTML>
        
        <head>
            <meta charset="utf-8">
            <title>Обработка данных форм</title>
        </head>
        """)

print("<h1>Обработка данных форм!</h1>")
print(f"<p><b>Found: {res['hits']['total']['value']}</b></p><hr>")

for index, i in enumerate(res['hits']['hits']):
    print(f"<ol>{index + 1}. <b>{i['_source']['title']}</b>")
    print(f"<br>{i['_source']['textBody']}</br>")
    print(f"<br><i>{i['_source']['URL']}</i><hr></ol>")
print("""</body>
        </html>""")
