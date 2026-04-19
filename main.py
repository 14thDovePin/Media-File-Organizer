""" June 30, 2025
What is this script about?
This script formats any Movie or Series file names into their proper titles
that "should" be readable by Plex's or Jellyfin's media file namescheming.

Script Procedure (Changes Through Development)

1. Prompt the media root directory.
2. Extract root directory name as well as all filenames within.
3. Parse title/s from root directory name as well as all filenames.
4. Get media data online.
    a. Attempt to grab data in the following order: OMDb > Google > IMDb > OMDb.
5. Format media names properly.
6. Prompt user for confirmation of file rename.
7. Rename all media files along with their external subtitles, and then finally the root directory.

External Libraries Used:
  colorama
  dotenv
  googlesearch-python
  pick

Developer Notes (Aprile 08, 2026)
I really did over engineered this. With a fresh new mindset as well
as software development approach. Let's see how I handle this!

TODO List
- Integrate Tests
"""

import os

import prompts

from data_processor import (
    parse_imdb_ids,
    process_directory_data,
    process_filenames_data,
    resolve_ids,
    unify_title_sequences
)
from file_manager import (
    prompt_root_directory,
    parse_filename
)
from request_manager import search_omdb
from utils.colors import Colors
from utils.debug import print_debug
from utils.templates import GenerateTemplate


DEBUG = True

ROOT_DIR = str()
DIR_NAME = str()

EXIT_LIST = ['exit', 'quit']


def main():
    # Prompt the root directory of the media.
    ROOT_DIR = prompt_root_directory()

    # Extract directory name, & filenames.
    walk = os.walk(ROOT_DIR)
    path, directories, filenames = next(walk)
    DIR_NAME = path.split('\\').pop()

    if DEBUG:
        print_debug()
        print_debug("FILE INFORMATION")
        print_debug(f'Path: {path}')
        print_debug(f'Directory Name: {DIR_NAME}')
        print_debug('Files:')
        for i in filenames: print_debug('\t'+i)

    # Initially parse the media title.
    media_data = parse_filename(DIR_NAME)

    # Process Media IMDb Title
    while True:

        # Lookup title through OMDb search.
        search_results = search_omdb(
            media_data["title"],
            media_data["year"]
        )

        if search_results is None:
            # Update media details.
            print('\nError! Movie Not Found...')
            print('Current Title Details:')
            print(f'\tTitle > {media_data["title"]}')
            print(f'\tYear -> {media_data["year"]}')
            print("Enter 'exit' or 'quit' to end script. Enter blank if either title or year doesn't need changes.")

            prompts.update_title(media_data)
            prompts.update_year(media_data)
        else:
            break

    # If multiple search results, prompt user to select.
    if int(search_results['totalResults']) > 1:
        pass


if __name__ == "__main__":
    # Setup terminal.
    commands = [
        "title Media File Organizer",
        "cls"
    ]

    for cmd in commands:
        os.system(cmd)

    print('Media File Organizer')
    print('====================')
    print('[Type "exit" or "quit" to end script or press `Ctrl` + `C`.]')

    # Run Script
    while True:
        main()
