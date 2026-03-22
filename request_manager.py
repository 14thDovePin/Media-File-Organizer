import math
import requests
import os

from colorama import Fore, Back, Style
from dotenv import load_dotenv

from utils.colors import Colors


load_dotenv()
c = Colors()
# URL Definitions
API_KEY = os.getenv('omdb_api')
OMDB_BASE_URL = 'https://www.omdbapi.com/?apikey='


# def request_metadata(title_sequence: list=[], year: str='', imdb_id: str=''):
def request_metadata(
        title_sequence: list = [],
        year: str = '',
        type: str = '',
        imdb_id: str = '',
        return_type : str='json'
        ) -> dict:
    """Return the json metadata of a given title seqeunce or imdb id.

    Parameters
    ----------
    title_sequence : list
        A sequenced list of string composing the *rough* title to search for.
    year : str
        The year of the title.
    type : str
        The type of the show. "movie", "series" or "episode".
    imdb_id: str
        The IMDb ID of the given movie or series.
    return_type : str
    """
    # Get Metadata
    url = construct_request(
        title_sequence,
        year,
        type,
        imdb_id,
        return_type
    )
    metadata = requests.get(url).json()

    if title_sequence:
        title = ' '.join(title_sequence)
    elif imdb_id:
        title = imdb_id

    # Get Json Metadata
    if metadata['Response'] == 'False':
        c.print_error("Failed Processing ", end='')
        print(f"> [", end='')
        c.print_warning(title, end='')
        print("]")
    else:
        c.print_success("Succeeded Processing ", end='')
        print(f"> [", end='')
        c.print_warning(title, end='')
        print("]")

    # Return Metadata
    return metadata


def construct_request(
        title_sequence: list = [],
        year: str = '',
        type: str = '',
        imdb_id: str = '',
        return_type : str='json'
        ) -> str:
    """Return a constructed url that can request with OMDb.

    Parameters
        title: ['title', 'of', 'the', 'show']
        year: Year released
        type: 'movie', 'series', or 'episode'
        imdb_id: IMDb ID of the show
        return_type: 'json' or 'xml'
    """
    # Integrate Parameters
    PARAMETERS = {
        'title' : 't=',
        'year' : 'y=',
        'type' : 'type=',  # [movie, series, episode]
        'imdb_id' : 'i=',
        'return_type' : 'r='  # [json, xml]
    }

    # Construct the Title
    if not title_sequence:
        combined_title = ''
    else:
        combined_title = title_sequence[0]
        for word in title_sequence[1:]:
            combined_title += '+' + word

    PARAMETERS['title'] += combined_title
    PARAMETERS['year'] += year
    PARAMETERS['type'] += type
    PARAMETERS['imdb_id'] += imdb_id
    PARAMETERS['return_type'] += return_type

    # Construct Request
    request = OMDB_BASE_URL + API_KEY
    for param in PARAMETERS.values():
        request += '&' + param

    return request


def check_media_type(imdb_id) -> bool:
    """Return the type of a given IMDb ID."""
    metadata = request_metadata(imdb_id=imdb_id)

    return metadata["Type"]
