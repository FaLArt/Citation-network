import requests, bs4


class AcmDlListOfProceedingsParser:
    domain = 'https://dl.acm.org/'
    publication_tab = '&_cf_containerId=cf_layoutareapubs&_cf_nodebug=true&_cf_nocache=true&_cf_clientid' \
                      '={1}&_cf_rc=1 '
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
    event = 'event_series.cfm?id={0}'
    url = domain + event + publication_tab

    def __init__(self):
        self.event_id = None
        self.client_id = None

    def parse(self, event_id, client_id):
        print('Starting parsing event with id: {0}'.format(event_id))

        self.event_id = event_id
        self.client_id = client_id
        self.url = self.url.format(event_id, client_id)

        proceeding_ids = []

        print('Downloading event from url: {0}'.format(self.url))
        response = requests.get(url=self.url, headers=self.headers)
        soup = bs4.BeautifulSoup(response.text, 'lxml')

        uls = soup.find_all('ul')

        for ul in uls:
            a = ul.find_all('a')
            for href in a:
                proceeding_ids.append(href['href'].split('=')[-1])

        print('Successfully!!! ^_^')
        return proceeding_ids


if __name__ == '__main__':
    parser = AcmDlListOfProceedingsParser()
    print(parser.parse('RE201', 'C3FE7A81D2B94946F9F673E2A6A2D243'))
