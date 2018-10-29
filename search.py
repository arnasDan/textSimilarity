from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from nltk import tokenize

class Result:
    title: str
    link: str
    words: list
    def __init__(self, title, link, words):
        self.title = title
        self.link = link
        self.words = words

def get_results(query: str):
    results = []
    media_html = requests.get('https://www.google.com/search?q=' + query.replace(" ", "+")).text
    soup = BeautifulSoup(media_html, 'lxml')
    results_block = soup.find("div", id="ires")
    for result in results_block.find_all("div", class_="g"):
        link = result.find("a").get('href')
        if "http" not in link:
            continue
        new_result = Result(title=result.find("h3").get_text(),
                            link=link.split("://")[1].split('/')[0],
                            words=[])
        for word in result.find_all("b"):
            if word.string != "...":
                new_result.words.append(word.string)
        results.append(new_result)
    return results

def split_text(text: str):
    chunks = tokenize.sent_tokenize(text, language="english")
    print(chunks)
    
    i = 0
    while i < len(chunks):
        words = chunks[i].split()
        if len(words) > 32:
            chunks.insert(i + 1, ' '.join(words[32:]))
            chunks[i] = ' '.join(words[:32])
        elif len(words) + len(chunks[i - 1].split()) <= 32:
            chunks[i - 1] += ' ' + ' '.join(words)
            del chunks[i]
            i -= 1
        i += 1
            
    print(chunks)
    return chunks

for result in get_results("test"):
    print(result.title)
    print(result.link)
    print(result.words)
    print('\n')