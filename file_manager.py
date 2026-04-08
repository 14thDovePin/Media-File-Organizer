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


def parse_name(filename: str, metadata: dict=None,
                     file_info: dict=None) -> dict:
    """ Return a dictionary of information regarding the given filename.
    Generate title sequence and information with a given filename.

    Parameters
    ----------
    **filename** : str
        Filename to process title sequence & pull information from.
    **metadata** : dict
        Information regarding metadata are stored inside the passed dict.
    **file_info** : dict
        Information regarding file information
        are stored inside the passed dict.
    """
    ignore_case = re.IGNORECASE

    # Patterns
    year_pattern = r'19\d\d|20\d\d'
    season_pattern = r'[\d\s.]SEASON[\s.]?(\d+)|SEASON|[\d\s.]?S(\d+)'
    episode_pattern = r'[\d\s.]EPISODE[\s.]?(\d+)|EPISODE|[\d\s.]?EP?(\d+)'
    number_pattern = r'\d+'
    enclosed_pattern = r'[\s.]?\([^\)]+\)|[\s.]?\[[^\]]+\]'
    word_pattern = r'[^. \s]+'

    # Store data into dictionaries.
    if metadata and file_info:
        # Store Filename
        file_info['filename'] = '.'.join(filename.split('.')[:-1])

        # Extract Year
        year = re.search(year_pattern, filename)

        if year:
            year = year.group(0)
            metadata['year'] = year

        # Extract Season Number
        season = re.search(season_pattern, filename, ignore_case)
        if season:
            if season.group(1):
                metadata['season'] = season.group(1)
            else:
                metadata['season'] = season.group(2)

        # Extract Episode Number
        episode = re.search(episode_pattern, filename, ignore_case)

        if episode:
            if episode.group(1):
                metadata['episode'] = episode.group(1)
            else:
                metadata['episode'] = episode.group(2)

        # Extract File Extension
        for extension in VE:
            if extension in filename:
                file_info['extension'] = extension

        # Determine Title Type
        if metadata['season'] and metadata['episode']:
            metadata['type'] = 'series'
        elif metadata['year']:
            metadata['type'] = 'movie'

        # Special Case/s

        # Remove anything enclosed in () or [], But if it
        # contains the Year, then replace it with it.
        parenthesized_words = re.findall(enclosed_pattern, filename)

        for matched_word in parenthesized_words:
            year = re.search(year_pattern, matched_word)

            if year:
                s_char = matched_word[0]  # Starting Character
                starting_char = s_char if s_char != '(' else ''
                year_final = starting_char + year.group(0)
                filename = filename.replace(matched_word, year_final)
            else:
                filename = filename.replace(matched_word, '')

    # Process Title Sequence

    # Pull Word Sequence
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

    return word_sequence


def check_video(filename: str) -> bool:
    """Check if filename is a video by its extension."""
    for ext in VE:
        if ext in filename:
            return True

    return False
