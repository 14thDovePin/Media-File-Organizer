import requests
import os

from dotenv import load_dotenv

from utils.colors import Colors


# Global Setup
load_dotenv()
API_KEY = os.getenv('omdb_api')
OMDB_BASE_URL = 'https://www.omdbapi.com/?apikey='


def search_omdb(
        search_title : str,
        year : int='',
        type : str='',
        page : int=1,
        page_limit : int=4
        ) -> dict:
    """Return a dictionary of search results based from given input.

    Parameters
    ----------
    search_title : str
        The movie or show title to search for.
    year : int
        The year of the title.
    type : str
        The type of the media to search for. "movie", "series" or "episode".
    page : int, default = 1
        Page to retrieve results from omdb.
    page_limit : int, default = 10
        Limit of pages to combine search results with.

    Returns
    -------
    dict
        "Search" : [dict, dict, ...]
        "totalResults" : str
        "Response" : str
            "True" or "False"
    """
    # Construct url.
    url = OMDB_BASE_URL + API_KEY \
        + "&s=" + search_title \
        + "&y=" + str(year) \
        + "&type=" + type \
        + "&page=" + str(page)

    # Process first request.
    response = requests.get(url).json()

    # Process consecutive request to merge results if `totalResults` > 10.
    totalResults = int(response['totalResults'])

    if totalResults > 10 and page == 1:
        count = totalResults / 10

        if totalResults % 10 != 0:
            count += 1

        count = int(count)

        if totalResults > page_limit * 10:
            print(f"PARSE EXCEEDED {page_limit} PAGES OF RESULTS! CUTTING EXCESS...")
            count = page_limit

        for i in range(count):
            if i == 0: continue
            consecutive_response = search_omdb(search_title, year, type, i+1)

            for result in consecutive_response["Search"]:
                if result not in response["Search"]:
                    response["Search"].append(result)

    return response


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


if __name__ == "__main__":
    results = search_omdb("after")["Search"]
    for i in results: print(f"[{i['imdbID']}] | {i['Title'], }")
    print("total results: ", len(results))