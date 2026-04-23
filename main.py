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
from request_manager import search_omdb, detailed_omdb_search
from utils.colors import Colors
from utils.data_sets import VIDE_EXTENSIONS, SUBTITLE_EXTENSIONS
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
            print('\nError! Media Not Found...')
            print('Current Title Details:')
            print(f'\tTitle > {media_data["title"]}')
            print(f'\tYear -> {media_data["year"]}')

            print('\nPrompting user for the media\'s title and year...')
            print("Enter 'exit' or 'quit' to end script. Enter blank if either title or year doesn't need changes.\n")

            prompts.update_title(media_data)
            prompts.update_year(media_data)
        else:
            break

    # If multiple search results, prompt user to select.
    if int(search_results['totalResults']) > 1:
        choice = prompts.select_result(search_results, media_data['title'])
    else:
        choice = search_results['Search'][0]

    # Final title confirmation.
    confirm = prompts.final_confirmation(choice, ROOT_DIR)

    if not confirm:
        return

    # Grab detailed omdb media information.
    media_info = detailed_omdb_search(
        choice['imdbID'],
    )

    print(media_info)

    print(f"\nMedia Type is {media_info['Type'].title()}")
    print("Begin Processing Media Files...")
    print("===============================")

    # Work on media type accordingly.
    if media_info['Type'] == 'movie':
        files_information = []
        media_file : dict = None
        subtitle_file : dict = None

        # Process directory files.
        for file in filenames:
            files_information.append(parse_filename(file))

        # Scan through files.
        for file in files_information:
            title_check = media_info['Title'].lower() in file['title'].lower()
            media_extension_check = file['file_extension'] in VIDE_EXTENSIONS
            subtitle_extension_check = file['file_extension'] in SUBTITLE_EXTENSIONS

            if title_check and media_extension_check:
                media_file = file

            if title_check and subtitle_extension_check:
                subtitle_file = file

            if media_file and subtitle_file:
                break

        # Construct base filename.
        base_filename = f"{media_info['Title']} ({media_info['Year']})"

        #
        # Process Media File
        #

        # Precheck file existence.
        media_file_path = os.path.join(ROOT_DIR, media_file['file_name'])

        if not os.path.exists(media_file_path):
            raise Exception("Media File Path Error!")

        # Construct new name.
        new_media_file_path = os.path.join(ROOT_DIR, base_filename +'.'+ media_file['file_extension'])

        # Rename files.
        os.rename(media_file_path, new_media_file_path)

        #
        # Process Subtitle File
        #

        if subtitle_file:
            # Precheck file existence.
            subtitle_file_path = os.path.join(ROOT_DIR, subtitle_file['file_name'])

            if not os.path.exists(subtitle_file_path):
                raise Exception("Subtitle File Path Error!")

            # Construct new name.
            new_subtitle_file_path = os.path.join(ROOT_DIR, base_filename +'.'+ subtitle_file['file_extension'])

            # Rename files.
            os.rename(subtitle_file_path, new_subtitle_file_path)

        root_path = path.split('\\')
        root_path = '\\'.join(root_path[:-1])
        new_root_directory = os.path.join(root_path, base_filename)

        os.rename(ROOT_DIR, new_root_directory)

    elif media_info['Type'] == 'series':
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
