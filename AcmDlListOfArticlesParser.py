import requests, re, bs4


class AcmDlListOfArticlesParser:
    domain = 'https://dl.acm.org/'
    mode_layout = 'flat'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
    proceeding = 'citation.cfm?id={0}&'
    parameters = 'preflayout={0}'.format(mode_layout)
    url = domain + proceeding + parameters

    def __init__(self):
        self.proceeding_id = None

    def parse(self, proceeding_id):
        print('Starting parsing proceeding with id: {0}'.format(proceeding_id))

        self.proceeding_id = proceeding_id
        self.url = self.url.format(self.proceeding_id)

        print('Downloading proceeding from url: {0}'.format(self.url))
        response = requests.get(url=self.url, headers=self.headers)
        soup = bs4.BeautifulSoup(response.text, 'lxml')

        article_ids = []

        layout = soup.find('div', {'class': 'layout'})
        table = layout.find('table', {'class': 'text12'})
        refs_for_articles = table.find_all(href=re.compile(r'citation.cfm\?id=.*'))

        for a in refs_for_articles:
            article_ids.append(a['href'].split('=')[-1])

        print('Successfully!!! ^_^')
        return article_ids


if __name__ == '__main__':
    parser = AcmDlListOfArticlesParser()
    print(parser.parse('1294921'))