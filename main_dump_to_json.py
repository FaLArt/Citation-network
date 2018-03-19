import json
from AcmDlListOfArticlesParser import AcmDlListOfArticlesParser
from AcmDlArticleParser import AcmDlArticleParser
from AcmDlListOfProceedingsParser import AcmDlListOfProceedingsParser

json_file = open('json_temp_db.json', 'w')
json_file.write('[\n')

event_id = 'RE201'
client_id = 'C3FE7A81D2B94946F9F673E2A6A2D243'

proceeding_parser = AcmDlListOfProceedingsParser()
# proceeding_ids = proceeding_parser.parse(event_id, client_id)

article_list_parser = AcmDlListOfArticlesParser()
article_ids = article_list_parser.parse('1294904')

print(article_ids)

for article in article_ids:
    article_parser = AcmDlArticleParser()
    json_file.write(json.dumps(article_parser.parse(article), indent=4))
    json_file.write(',\n')
json_file.write(']')

'''
for proceeding in proceeding_ids:
    article_list_parser = AcmDlListOfArticlesParser()
    article_ids = article_list_parser.parse(proceeding)
    for article_id in article_ids:
        article_parser = AcmDlArticleParser()
        article_data = article_parser.parse(article_id)
        json_file.write(json.dumps(article_data, indent=4))
        json_file.write(',\n')
json_file.write(']')
'''
