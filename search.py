from bs4 import BeautifulSoup
import requests
from nltk import tokenize
from dataclasses import dataclass

@dataclass
class Result:
    search_string: str
    results: str
    def __str__(self):
        return '<input id="block-header" readonly value="' + self.search_string + '"> \n' + self.results

def get_results(query: str):
    results = []
    media_html = requests.get('https://www.google.com/search?q=' + query.replace(" ", "+")).text
    soup = BeautifulSoup(media_html, 'lxml')
    results = soup.find("div", id="ires")
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
