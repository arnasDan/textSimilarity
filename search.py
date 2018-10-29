from selenium import webdriver
from bs4 import BeautifulSoup
import requests

media_html = requests.get('https://www.google.com/search?q=testas').text
soup = BeautifulSoup(media_html, 'lxml')
results_block = soup.find("div", id="ires")
for result in results_block.find_all("div", class_="g"):
    print(result.find("a").get('href').split("://")[1].split('/')[0])
    print(result.find("h3").get_text())
    for word in result.find_all("b"):
        if (word.string != "..."):
            print(word.string)
    print('\n')