import requests
from bs4 import BeautifulSoup

def get_latest_tutorials(count=5):
    """
    Fetches the latest tutorials from FreeCodeCamp's news page.

    :param count: The number of latest tutorials to fetch.
    :return: A list of dictionaries containing tutorial titles and URLs.
    """
    url = 'https://www.freecodecamp.org/news/'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code

        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article', limit=count)

        tutorials = []
        for article in articles:
            title = article.find('h2').get_text(strip=True)
            link = article.find('a')['href']
            tutorials.append({'title': title, 'url': f'https://www.freecodecamp.org{link}'})

        return tutorials
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
