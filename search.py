from bs4 import BeautifulSoup
import requests
from nltk import tokenize
import docx2txt
import PySimpleGUI as gui
import ctypes

class Result:
    source_chunk: str
    title: str
    link: str
    words: list
    def __init__(self, title, link, words, chunk):
        self.title = title
        self.link = link
        self.words = words
        self.source_chunk = chunk

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
                            words=[],
                            chunk=query)
        for word in result.find_all("b"):
            if word.string != "...":
                new_result.words.append(word.string)
        results.append(new_result)
    return results

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
        i += 1
    return chunks

ctypes.windll.shcore.SetProcessDpiAwareness(1)
filename = gui.PopupGetFile("Choose a file:", file_types=(("Word documents (*.docx)", "*.docx"),))

try:
    document_text = docx2txt.process(filename)
except FileNotFoundError:
    gui.Popup("Cannot find file specified")
    exit()

results = []
for chunk in split_text(document_text):
    results.extend(get_results(chunk))

layout = [[gui.T('Table Test')]]
for result in results:
    layout.append([
        gui.T(result.source_chunk, background_color='white', pad=(1,1)),
        gui.T(result.title, background_color='white', pad=(1,1)),
        gui.T(result.link, background_color='white', pad=(1,1)),
        gui.T('; '.join(result.words), background_color='white', pad=(1,1))
        ])
gui.FlexForm('Table', grab_anywhere=True).LayoutAndRead(layout)