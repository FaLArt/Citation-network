import json, AcmDlListOfProceedingsParser, AcmDlArticleParser

json_file = open('json_temp_db.json', 'w')

event_id = 'RE201'
client_id = 'C3FE7A81D2B94946F9F673E2A6A2D243'

article_ids_parser = AcmDlListOfProceedingsParser.AcmDlListOfProceedingsParser()

json_file.write('[\n')

article_ids = article_ids_parser.parse(event_id, client_id)


for article_id in article_ids[:5]:
    print('Current: {0}/{1}'.format(article_ids.index(article_id) + 1, len(article_ids)))
    try:
        article_data = json.dumps(AcmDlArticleParser.AcmDlArticleParser().parse(article_id), indent=4)
    except:
        continue
    json_file.write(article_data)
    json_file.write('\n,')
    print('#' * 100)
json_file.write(']\n')
