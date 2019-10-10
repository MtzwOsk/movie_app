import requests
from movie_app.settings import OMDB_API_KEY


def get_data_from_omdb(title=None):
    """
    Get data about movie from www.omdbapi.com
    :param title: str
    :return: dict, None
    """
    try:
        resp = requests.get(
            params={'t': title, 'apikey': OMDB_API_KEY, 'r': 'json'},
            url='http://www.omdbapi.com/'
        )
    except requests.RequestException:
        return None

    if resp.status_code != 200 or resp.json().get('Error'):
        return None

    return resp.json()
