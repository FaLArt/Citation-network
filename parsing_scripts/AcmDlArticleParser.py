import requests, bs4, json, re
from bibtexparser.bparser import BibTexParser


class AcmDlArticleParser:
    mode_layout = 'flat'
    exp_format = 'bibtex'
    domain = 'https://dl.acm.org/'
    article = 'citation.cfm?id={0}&'
    parameters = 'preflayout={0}'.format(mode_layout)
    url = domain + article + parameters
    url_download_bibtex = domain + 'downformats.cfm?id={0}&parent_id=&expformat={1}'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}

    def __init__(self):
        self.id = None

    def parse(self, article_id):
        print('Start parsing article with id: {0}'.format(article_id), 'Initializing...', sep='\n')
        self.id = article_id
        self.url = self.url.format(article_id)
        self.url_download_bibtex = self.url_download_bibtex.format(article_id, self.exp_format)

        article_data = {}

        print('Downloading article from url: {0}'.format(self.url))
        response = requests.get(url=self.url, headers=self.headers)
        soup = bs4.BeautifulSoup(response.text, 'lxml')

        open('bibtex.bib', 'w').write(requests.get(url=self.url_download_bibtex, headers=self.headers).text)
        bibtex_file = open('bibtex.bib', 'r')
        bibtex_dict = BibTexParser(interpolate_strings=False).parse_file(bibtex_file).entries

        article_data['article_id'] = article_id
        article_data['url'] = self.url
        article_data['title'] = re.sub('[\'\']', '', repr(bibtex_dict[0].get('title', None)))
        article_data['doi'] = re.sub('[\'\']', '', repr(bibtex_dict[0].get('doi', None)))
        article_data['year'] = re.sub('[\'\']', '', repr(bibtex_dict[0].get('year', None)))

        print('Getting authors...')
        self.__get_authors(soup, article_data)

        print('Getting abstract...')
        self.__get_abstract(soup, article_data)

        print('Getting venue...')
        self.__get_venue(soup, article_data)

        print('Get citations...')
        self.__get_cited_by(soup, article_data)

        print('Successfully!!! ^_^')
        return article_data

    def __get_authors(self, soup, article_data):
        divmain = soup.find('div', id='divmain')

        authors_tags = divmain.find_all('td', {'style': 'padding-right:3px;', 'valign': 'top', 'nowrap': 'nowrap'})
        authors = []

        for author_tag in authors_tags:
            name = author_tag.text
            authors.append({'name': name.strip(),
                            'url': self.domain + author_tag.find('a')['href']})

        article_data['authors'] = authors

    @staticmethod
    def __get_abstract(soup, article_data):
        layout = soup.find('div', {'class': 'layout'})
        flatbody = layout.find('div', {'class': 'flatbody'})

        abstract = re.sub('[\'\']', '', repr(flatbody.text.strip()))
        article_data['abstract'] = abstract

    def __get_venue(self, soup, article_data):
        td = soup.find('td', string='Conference')

        if td:
            td = td.nextSibling.nextSibling
            venue = re.sub('[\'\']', '', repr(td.strong.text.strip()))
            url_conference = td.a['href']
        else:
            venue = None
            url_conference = 'None'

        article_data['venue'] = {'name': venue,
                                 'url': self.domain + url_conference}

    @staticmethod
    def __get_cited_by(soup, article_data):
        flatbody = soup.find_all('div', {'class': 'flatbody'})
        cited_by = []
        for a in flatbody[3].find_all('a'):
            cited_by.append(a['href'].split('=')[-1])

        article_data['cited_by'] = cited_by

    @staticmethod
    def __dump_to_json_file(data_dict):
        open('data.json', 'w').write(json.dumps(data_dict, indent=4))


if __name__ == '__main__':
    parser = AcmDlArticleParser()
    article_data = parser.parse('1295014')
    open('data.json', 'w').write(json.dumps(article_data, indent=4))
