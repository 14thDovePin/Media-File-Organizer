import requests
import os

from time import sleep, time

from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from bs4 import BeautifulSoup
from dotenv import load_dotenv


# Global Setup
load_dotenv()
API_KEY = os.getenv('omdb_api')
OMDB_BASE_URL = 'https://www.omdbapi.com/?apikey='


def extract_series_ids(series_imdb_id:str, timeout:int=10) -> list:
    """Extract a list of IMDb IDs by scraping IMDb with a given series ID.

    Parameters
    ----------
    series_imdb_id : str
        - The series ID to extract episode IMDb IDs of.
    timeout : int, default 10
        - # of seconds before scraping times out on a webpage.
    """
    # Get the total number of seasons the show has.
    number_of_seasons = int(detailed_omdb_search(series_imdb_id)['totalSeasons'])

    # Grab all urls listing episodes per season.
    episode_list_pages = []

    for i in range(number_of_seasons):
        episode_list_pages.append(get_imdb_series_url(series_imdb_id, i+1))

    print("Web Scraping Information...")

    # Grab all documents for scraping.
    pages = []

    # Scrape information with selenium in the background.
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("user-agent=...")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)  # Add options=options in args.

    # Scrape pages for hrefs.
    hrefs = []

    for page in episode_list_pages:
        print(f'Scraping {page}')
        driver.get(page)

        see_all_xpath = '/html/body/div[2]/main/div/section/div/section/div/div[1]/section[2]/section[2]/article[51]/div/span[2]/button/span/span'
        episode_list_panel_xpath = '/html/body/div[2]/main/div/section/div/section/div/div[1]/section[2]/section[2]'

        # Wait for page section content to load.
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, episode_list_panel_xpath))
        )

        print("Page Loaded Successfully!")

        # Click see all button if present.
        see_all_button = None

        try:
            see_all_button = driver.find_element(By.XPATH, see_all_xpath)
        except:
            print('Button "See All" not found.')

        if see_all_button:
            driver.execute_script("arguments[0].click();", see_all_button)

            # Check for the number of items within episode list panel.
            episode_list_panel = driver.find_element(By.XPATH, episode_list_panel_xpath)
            count = len(episode_list_panel.find_elements(By.TAG_NAME, "article"))

            # Wait for episode list panel to finish updating.
            timeout_counter = 0

            print("Loading episode lists...")
            start_time = time()  # Track time.

            while True:
                sleep(0.2)
                current_count = len(episode_list_panel.find_elements(By.TAG_NAME, "article"))

                if count != current_count:
                    count = current_count
                    timeout_counter = 0

                if timeout_counter >= 2:  # Number of Seconds
                    break

                timeout_counter += 0.2

            end_time = time()
            total_time = round(end_time - start_time, 2)

            print(f"Time took to load all episodes... | {total_time}")

        print("Extracting IMDb IDs...")

        # Extract & filter hrefs from tags.
        elements = driver.find_elements(By.CLASS_NAME, "ipc-title-link-wrapper")

        for tag in elements:
            href = tag.get_attribute("href")

            if '_ep_' in href:
                hrefs.append(href)

    # Wrap up web scraping.
    driver.close()

    # Filter IMDb IDs.
    IDs = []

    for href in hrefs:
        raw = href.split('/')

        for i in raw:
            if i.startswith('tt'):
                IDs.append(i)

    print(f"Total IDs Gathered: {len(IDs)}")
    return IDs


def get_imdb_series_url(imdb_id:str, season_number:int) -> str:
    """Return an IMDb series url given an ID and its season number."""
    return f"https://www.imdb.com/title/{imdb_id}/episodes/?season={str(season_number)}"


def detailed_omdb_search(
        imdb_id: str,
        title : str='',
        year : int='',
        plot : str='',
        type : str=''
        ) -> dict | None:
    """Return a dictionary of search results based from given input.

    Parameters
    ----------
    imdb_id: str
        IMDb's official ID for the media.
    search_title : str
        The movie or show title to search for.
    year : int
        The year of the title.
    plot : str
        Print the plot in "short" or "full" versions. Defaults to short.
    type : str
        The type of the media to search for. "movie", "series" or "episode".

    Returns
    -------
    dict
        Title : str
        Year : str
        Season : str
        Episode : str
        Plot : str
        imdbID : str
        Type : str
        Response : str
    """
    # Construct url.
    url = OMDB_BASE_URL + API_KEY \
        + "&i=" + imdb_id \
        + "&t=" + title \
        + "&y=" + str(year) \
        + "&plot=" + plot \
        + "&type=" + type \

    # Process first request.
    response = requests.get(url).json()

    if 'Response' == 'False':
        return None
    else:
        return response


def search_omdb(
        search_title : str,
        year : int='',
        type : str='',
        page : int=1,
        page_limit : int=4
        ) -> dict | None:
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
        Search : [dict, dict, ...]
        totalResults : str
        Response : str
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

    if 'totalResults' not in response.keys():
        return None

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
    # Simple testing only.
    results = extract_series_ids("tt2741602")  # The Blacklist
    results = extract_series_ids("tt0388629")  # One Piece