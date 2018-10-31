from bs4 import BeautifulSoup
import requests
from nltk import tokenize
import docx2txt
import PySimpleGUI as gui
import ctypes
import textwrap

class Result:
    title: str
    link: str
    words: list
    def __init__(self, title, link, words):
        self.title = title
        self.link = link
        self.words = words
    def contains_word(self, new_word):
        for word in self.words:
            if word.lower() == new_word.lower():
                return True
        return False

def get_results(query: str):
    results = []
    media_html = requests.get('https://www.google.com/search?q=' + query.replace(" ", "+")).text
    soup = BeautifulSoup(media_html, 'lxml')
    results_block = soup.find("div", id="ires")
    for result in results_block.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['g']):
        link = result.find("a").get('href')
        if "http" not in link:
            continue
        new_result = Result(title=result.find("h3").get_text(),
                            link=link.split("://")[1].split('/')[0],
                            words=[])
        for word in result.find_all("b"):
            if word.string != "..." and not new_result.contains_word(word.string):
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
        else:
            chunks[i] = ' '.join(words)
        i += 1
    return chunks

ctypes.windll.shcore.SetProcessDpiAwareness(1)
filename = gui.PopupGetFile("Choose a document to check:", file_types=(("Word documents (*.docx)", "*.docx"),))
if (filename == None):
    exit()

try:
    document_text = docx2txt.process(filename)
except FileNotFoundError:
    gui.Popup("Cannot find file specified")
    exit()
except PermissionError:
    gui.Popup("Cannot access file")
    exit()

results = dict()
source_chunks = split_text(document_text)
for i, chunk in enumerate(source_chunks):
    if not gui.OneLineProgressMeter('Executing searches...', i + 1, len(source_chunks), 'search_meter') and i + 1 < len(source_chunks):
        exit()
    results[chunk] = get_results(chunk)

gui.SetOptions(element_padding=(0, 0))
layout = [[gui.T('Results:', font='Any 18')]]
for result in results.items():
    column_layout = [[gui.T('No matches', background_color='white', pad=(1,1))]] if len(result[1]) == 0 else [[]]
    for values in result[1]:
        column_layout.append([
            (gui.T(textwrap.fill(values.title, 55) + '\n' + values.link, background_color='white', pad=(1,1), size=(55, 3))),                        
            (gui.T(textwrap.fill('; '.join(values.words), 40), background_color='white', pad=(1,1), size=(40, 3)))
        ])
    header_rows = textwrap.wrap(result[0], 100)
    layout.extend([[gui.T('\n' + '\n'.join(header_rows), size=(120, len(header_rows) + 1), font='Bold')],
                   [gui.Column(column_layout)]])
wrapper = [[gui.Column(layout, scrollable=True, size=(920, 700))]]
window = gui.Window('Search results').Layout(wrapper)
window.Show()