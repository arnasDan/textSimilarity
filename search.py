from bs4 import BeautifulSoup
import requests
from nltk import tokenize
from dataclasses import dataclass

@dataclass
class Result:
    search_string: str
    results: str
    def __str__(self):
        return '<input class="block-header" readonly value="%s">\n%s' % (self.search_string, self.results)

def get_results(query: str):
    media_html = requests.get('https://www.google.com/search?q=' + query.replace(" ", "+")).text
    soup = BeautifulSoup(media_html, 'lxml')
    results = soup.find('div', id='ires')
    #replace ires id with ires class so that multiple can be included     
    del results['id']
    results['class'] = 'ires'
    #replace video results with regular-style results (no thumbnail)
    for table_element in soup.find_all(['table', 'tbody', 'tr']):
        table_element.unwrap()
    for td in soup.find_all('td'):
        if (td.find('span', {'class': 'st'})):
            td.name = 'div'
            del td['style']
            del td['valign']
            td['class'] = 's'
        elif (td.find('h3')):
            td.unwrap()
        else:
           td.extract()

    return Result(query, str(results))

def split_text(text: str):
    chunks = tokenize.sent_tokenize(text)
    i = 0
    while i < len(chunks):
        words = chunks[i].split()
        if len(words) > 32:
            chunks.insert(i + 1, ' '.join(words[32:]))
            chunks[i] = ' '.join(words[:32])
        elif i > 0 and len(words) + len(chunks[i - 1].split()) <= 32:
            chunks[i - 1] += ' ' + ' '.join(words)
            del chunks[i]
            i -= 1
        else:
            chunks[i] = ' '.join(words)
        i += 1
    return chunks
