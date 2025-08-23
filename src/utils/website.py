import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


class Website:

    def __init__(self, url):
        """
        This utility creates a website object from given URL using BeautifulSoup library.
        :param url:
        """
        self.url = url
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(['style', 'script', '[document]', 'head', 'title']):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)
