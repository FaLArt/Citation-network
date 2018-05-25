import json
import re
import bs4
import requests

from bibtexparser.bparser import BibTexParser


class ArticleParser:
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
        article_data['title'] = re.sub('[\'\"]', '', repr(bibtex_dict[0].get('title', None)))
        article_data['doi'] = re.sub('[\'\"]', '', repr(bibtex_dict[0].get('doi', None)))
        article_data['year'] = re.sub('[\'\"]', '', repr(bibtex_dict[0].get('year', None)))
        article_data['venue'] = {'name': re.sub('[\'\"]', '', repr(bibtex_dict[0].get('journal', None))),
                                 'url': self.domain + 'None'}

        print('Getting authors...')
        self.__get_authors_and_affiliations(soup, article_data)

        print('Getting abstract...')
        self.__get_abstract(soup, article_data)

        print('Getting venue...')
        self.__get_venue(soup, article_data)

        print('Get citations...')
        self.__get_cited_by(soup, article_data)

        print('Successfully!!! ^_^')
        return article_data

    def __get_authors_and_affiliations(self, soup, article_data):
        divmain = soup.find('div', id='divmain')

        authors_tags = divmain.find_all('a', href=re.compile('author_page.cfm\?id=*'))
        authors_and_affiliations = []

        affiliation_tags = divmain.find_all('a', href=re.compile('inst_page.cfm\?id=*'))

        for author, affiliation in zip(authors_tags, affiliation_tags):
            authors_and_affiliations.append({'name': re.sub('[\'\"]', '', repr(author.text.strip())),
                                             'url': self.domain + author['href'],
                                             'affiliation': {
                                                 'name': re.sub('[\'\"]', '', repr(affiliation.text.strip())),
                                                 'url': self.domain + affiliation['href']}})

        article_data['authors_and_affiliations'] = authors_and_affiliations

    @staticmethod
    def __get_abstract(soup, article_data):
        layout = soup.find('div', {'class': 'layout'})
        flatbody = layout.find('div', {'class': 'flatbody'})

        abstract = re.sub('[\'\"]', '', repr(flatbody.text.strip()))
        article_data['abstract'] = abstract

    def __get_venue(self, soup, article_data):
        if article_data['venue']['name'] != 'None':
            return

        td = soup.find('td', string='Conference')

        if td:
            td = td.nextSibling.nextSibling
            venue = re.sub('[\'\"]', '', repr(td.strong.text.strip()))
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
    parser = ArticleParser()
    article_data = parser.parse('2008553')
    open('data.json', 'w').write(json.dumps(article_data, indent=4))
