import argparse
import docx2txt
import PySimpleGUI as gui
import ctypes
from search import split_text, get_results
import textwrap

parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f', dest='filename', help='file name of docx document to be checked')

args = parser.parse_args()

ctypes.windll.shcore.SetProcessDpiAwareness(1)
filename = args.filename or gui.PopupGetFile("Choose a document to check:", file_types=(("Word documents (*.docx)", "*.docx"),))
if (filename == None):
    exit()

try:
    document_text = docx2txt.process(filename)
except FileNotFoundError:
    gui.Popup("Cannot find file specified")
    exit()
except PermissionError:
    gui.Popup("Cannot access file. Is it still open?")
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
wrapper = [[gui.Column(layout, scrollable=True, size=(800, 500))]]
window = gui.Window('Search results').Layout(wrapper)
window.Show()