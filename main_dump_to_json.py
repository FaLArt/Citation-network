import json
from AcmDlListOfArticlesParser import AcmDlListOfArticlesParser
from AcmDlArticleParser import AcmDlArticleParser
from AcmDlListOfProceedingsParser import AcmDlListOfProceedingsParser

json_file = open('json_temp_db.json', 'w')

event_id = 'RE201'
client_id = 'C3FE7A81D2B94946F9F673E2A6A2D243'

proceeding_parser = AcmDlListOfProceedingsParser()
proceeding_ids = proceeding_parser.parse(event_id, client_id)

article_list_parser = AcmDlListOfArticlesParser()
article_ids = article_list_parser.parse(proceeding_ids[0])

print(article_ids)
