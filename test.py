import bs4, requests

url = 'https://dl.acm.org/citation.cfm?id=2492591&preflayout=flat'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}

response = requests.get(url=url, headers=headers)
soup = bs4.BeautifulSoup(response.text, 'html.parser')

result = soup.find('body')


with open('test.html', 'wb') as file:
    file.write(result.encode('utf-8'))
