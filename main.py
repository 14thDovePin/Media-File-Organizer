""" June 30, 2025
What is this script about?
This script formats any Movie or Series file names into their proper
titles that are readable by Plex's or Jellyfin's media file namescheming.

How does it work?
Below is the script's procedure. (may change as the script is developed)

1. Locate the media files.
    - Extract parent directory name.
    - Extract filename/s.
2. Process title/s from either directory name or filename/s.
3. Determine media type (movie or show).
4. Obtain the proper parent directory name as well as media filename/s from OMDb or OMDb.
5. Format title to Plex's media file namescheming.
6. Rename all media files.

External Libraries Used:
  colorama
  dotenv
  googlesearch-python

Developer Notes
I overengineered this a little bit. But that's part
of trying to implement new things I've learned!
"""

import os

from file_manager import prompt_root_directory
from data_processor import (
    parse_imdb_ids,
    process_directory_data,
    process_filenames_data,
    resolve_ids,
    unify_title_sequences
)
from request_manager import check_media_type
from utils.colors import Colors
from utils.templates import GenerateTemplate


DEBUG_MODE = False

ROOT_DIR = str()
DIR_NAME = str()


def main():
    print('Media File Organizer')
    print('====================')
    print('[Type "exit" or "quit" to end script...]')

    # Prompt the root directory of the media.
    ROOT_DIR = prompt_root_directory()

    # Extract Directory Name
    DIR_NAME = ROOT_DIR.split('\\').pop()

    '''Directory Scanning Plan

    As of now the setup currently assumes that the directory is currently a movie or tv show.
    In the near future updates the script needs to scan a directory full of either movies or shows.
    For each scan: A data structure should represent a directory, and all the files within it.
    For each of this data structure should be tested if its either a movie or show.
    '''

    # Extract Filenames
    walk = os.walk(ROOT_DIR)
    _, _, filenames = next(walk)
    print(filenames)

    # Integrate sample in test. Integarte in debug mode?


    # media_directory, directory_name, filenames = prompt_root_directory()

    return

    # Process media data.
    directory_data = process_directory_data(media_directory, directory_name)
    files_data = process_filenames_data(media_directory, filenames)

    # Unify Title Sequences
    title_sequences = unify_title_sequences(directory_data, files_data)

    # Grab IMDb IDs by parsing each title with Google.
    imdb_ids = parse_imdb_ids(title_sequences)

    # Resolve final imdb id if there are multiple and check its type.
    final_id = resolve_ids(imdb_ids)
    media_type = check_media_type(final_id)

    # Parse ID Through OMDb
    # Check if Movie or Series
    # If Movie, Construct Final Filename
    # If Seiries, Test if Beautifulsoup Can Extract Episode Names

    print()


if __name__ == "__main__":
    # Run Windows terminal commands.
    commands = [
        "title Plex File Organizer",
        "cls"
    ]

    for cmd in commands:
        os.system(cmd)

    # Run Script
    # while True:
    main()
