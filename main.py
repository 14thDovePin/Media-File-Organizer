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

Developer Notes (Aprile 08, 2026)
I really did over engineered this. With a fresh new mindset as well
as software development approach. Let's see how I handle this!

TODO List
- Integrate Tests
"""

import os

from file_manager import (
    prompt_root_directory,
    parse_filename
)
from data_processor import (
    parse_imdb_ids,
    process_directory_data,
    process_filenames_data,
    resolve_ids,
    unify_title_sequences
)
from request_manager import check_media_type
from utils.colors import Colors
from utils.debug import print_debug
from utils.templates import GenerateTemplate


DEBUG = True

ROOT_DIR = str()
DIR_NAME = str()


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




    # # Process media data.
    # directory_data = process_directory_data(media_directory, directory_name)
    # files_data = process_filenames_data(media_directory, filenames)

    return

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
    # Setup terminal.
    commands = [
        "title Media File Organizer",
        "cls"
    ]

    for cmd in commands:
        os.system(cmd)

    print('Media File Organizer')
    print('====================')
    print('[Type "exit" or "quit" to end script...]')

    # Run Script
    while True:
        main()
