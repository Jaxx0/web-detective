import requests
from bs4 import BeautifulSoup


def crawler(url):
    """ This function crawls a URL and extracts the title from the document"""

    try:
        page = requests.get(str(url))
        soup = BeautifulSoup(page.text, 'html.parser')
        title = soup.find('title').get_text()
        return {'title': title}
    except requests.exceptions.ConnectionError as e:
        return str(e)