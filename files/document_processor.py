import requests
from bs4 import BeautifulSoup

""" This function crawls a URL and extracts the title from the document"""


def crawler(url):
    try:
        page = requests.get(str(url))
        soup = BeautifulSoup(page.text, 'html.parser')
        title = soup.find('title').get_text()
        return {'title': title}
    except requests.exceptions.RequestException as e:
        return str(e)