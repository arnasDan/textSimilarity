import argparse
import docx2txt
import search
import textwrap
import sys

parser = argparse.ArgumentParser()
parser.add_argument(dest='filename', help='docx document to be checked')

args = parser.parse_args()

filename = args.filename
if (filename == None):
    #TODO: do something else
    exit()
try: 
    document_text = docx2txt.process(filename)
except FileNotFoundError:
    #TODO: do something else
    exit()
except PermissionError:
    #TODO: do something else
    exit()

results = []
source_chunks = search.split_text(document_text)
for i, chunk in enumerate(source_chunks):
    results.append(search.get_results(chunk))

with open('results.html', 'w', encoding='utf-8') as file:
    file.write('<html> \n <head> \n <link rel="stylesheet" type="text/css" href="style.css"> \n <body>')
    for result in results:
        file.write(str(result))
    file.write('</html> \n </body>')

print("success")
