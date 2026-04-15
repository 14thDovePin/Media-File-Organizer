import json
import os
import re

from colorama import Fore

from utils.colors import Colors
from utils.data_sets import video_extensions, video_qualities


VE = video_extensions()
VQ = video_qualities()


def prompt_root_directory() -> str:
    """Prompt the root directory and return it as a string."""
    while True:
        media_directory = input("Enter Media Root Directory: ")

        if media_directory.lower() in ['exit', 'quit']:
            exit()

        if not media_directory:
            continue

        if not os.path.exists(media_directory):
            print("--- Invalid Directory! ---")
        else:
            return media_directory


def parse_media_information(filename) -> dict:
    """Parse a given filename for its media related information.

    Parameters
    ----------
    **filename** : str
        Filename to parse.

    Returns
    -------
    dict
        title : str
        year : int
        type : str
            "movie" or "series"
        season_number : int
        episode_number : int
    """
    ignore_case = re.IGNORECASE

    # Patterns
    year_pattern = r'19\d\d|20\d\d'
    season_pattern = r'[\d\s.]SEASON[\s.]?(\d+)|SEASON|[\d\s.]?S(\d+)'
    episode_pattern = r'[\d\s.]EPISODE[\s.]?(\d+)|EPISODE|[\d\s.]?EP?(\d+)'
    enclosed_pattern = r'[\s.]?\([^\)]+\)|[\s.]?\[[^\]]+\]'
    word_pattern = r'[^. \s]+'

    media_data = {
        "title": str(),
        "year": int(),
        "type": str(),
        "season_number": int(),
        "episode_number": int(),
        "file_extension": str()
    }

    # Parse data into dictionary.

    # Extract Year
    year = re.search(year_pattern, filename)

    if year:
        year = year.group(0)
        media_data["year"] = year

    # Extract Season Number
    season = re.search(season_pattern, filename, ignore_case)

    if season:
        if season.group(1):
            media_data['season_number'] = season.group(1)
        else:
            media_data['season_number'] = season.group(2)

    # Extract Episode Number
    episode = re.search(episode_pattern, filename, ignore_case)

    if episode:
        if episode.group(1):
            media_data['episode_number'] = episode.group(1)
        else:
            media_data['episode_number'] = episode.group(2)

    # Extract File Extension
    for extension in VE:
        if extension in filename:
            media_data['file_extension'] = extension

    # Determine Title Type
    if media_data['season_number'] and media_data['episode_number']:
        media_data['type'] = 'series'
    elif media_data['year']:
        media_data['type'] = 'movie'

    # Special Case/s

    # Remove anything enclosed in () or [], But if it
    # contains the Year, then remove () or [].
    enclosed_words = re.findall(enclosed_pattern, filename)

    for matched_word in enclosed_words:
        year = re.search(year_pattern, matched_word)

        if year:
            s_char = matched_word[0]  # Starting Character
            starting_char = s_char if s_char != '(' else ''
            year_final = starting_char + year.group(0)
            filename = filename.replace(matched_word, year_final)
        else:
            filename = filename.replace(matched_word, '')

    # Process Title

    # Sequence words.
    word_sequence = re.findall(word_pattern, filename)

    # Cut List
    indexes = []
    for word in word_sequence:
        store_index = False

        # File Extension
        if word in VE:
            store_index = True

        # Year
        if re.search(year_pattern, word):
            store_index = True

        # Video Quality
        if word in VQ:
            store_index = True

        # Season/Episode #
        s_check = re.search(season_pattern, word, ignore_case)
        e_check = re.search(episode_pattern, word, ignore_case)

        if s_check or e_check:
            store_index = True

        # Store Index
        if store_index:
            indexes.append(word_sequence.index(word))

    if indexes:
        final_index = min(indexes)
        word_sequence = word_sequence[:final_index]

    media_data["title"] = " ".join(word_sequence)

    return media_data


def check_video(filename: str) -> bool:
    """Check if filename is a video by its extension."""
    for ext in VE:
        if ext in filename:
            return True

    return False


if __name__ == "__main__":
    files_and_directories = []
    walk = os.walk("test\\simulated_media_files")

    for _, dirs, files in walk:
        for i in dirs:
            files_and_directories.append(i)

        for i in files:
            files_and_directories.append(i)

    print(len(files_and_directories))

    test_results = list()

    for i in files_and_directories:
        test_results.append(parse_media_information(i))

    for i in test_results: print(i)
    print(len(test_results))