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
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            self.title = soup.title.string if soup.title else "No title found"
            if soup.body:
                for irrelevant in soup.body(["script", "style", "img", "input"]):
                    irrelevant.decompose()
                self.text = soup.body.get_text(separator="\n", strip=True)
            else:
                self.text = ""
            links = [link.get('href') for link in soup.find_all('a')]
            self.links = [link for link in links if link]
        except requests.exceptions.RequestException:
            self.text = ""
            self.title = "No title found"

    def get_contents(self):
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"