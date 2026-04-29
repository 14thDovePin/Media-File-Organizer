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
import file_manager
import request_manager


ROOT_DIR = str()
DIR_NAME = str()

EXIT_LIST = ['exit', 'quit']


def main():
    # Prompt the root directory of the media.
    ROOT_DIR = prompts.root_directory()

    # Extract directory name, & filenames.
    walk = os.walk(ROOT_DIR)
    path, _, filenames = next(walk)
    DIR_NAME = path.split('\\').pop()

    print("\nFILE INFORMATION")
    print("================")
    print(f'Path: {path}')
    print(f'Directory Name: {DIR_NAME}')
    print('Files Detected :')
    for i in filenames: print(' - '+i)
    print(f'[{len(filenames)}] Total Files Detected...')
    print("================")

    input("Press Enter/Return to proceed...")

    print("Processing Media...")

    # Parse the media title for searching.
    media_data = file_manager.parse_filename(DIR_NAME)

    while True:

        # Lookup title through OMDb search.
        search_results = request_manager.search_omdb(
            media_data["title"],
            media_data["year"]
        )

        # Update media details if search results comes out empty.
        if search_results is None:
            print('\nError! Media Not Found...')
            print('Current Title Details:')
            print(f' - Title > {media_data["title"]}')
            print(f' - Year -> {media_data["year"]}')
            print('\nPrompting user for the media\'s proper title and year...')
            print("Enter 'exit' or 'quit' to end script.\n")

            prompts.update_title(media_data)
            prompts.update_year(media_data)
        else:
            break

    # If multiple search results, prompt user to select.
    if int(search_results['totalResults']) > 1:
        print("Multiple search results found! Prompting user for the correct one...")
        choice = prompts.select_result(search_results, media_data['title'])
    else:
        choice = search_results['Search'][0]

    # Grab detailed omdb media information.
    media_info = request_manager.detailed_omdb_search(
        choice['imdbID'],
    )

    print(f"\nMedia Type is {media_info['Type'].title()}")
    print("Begin Processing Media Files...")
    print("===============================")

    # Work on media type accordingly.
    if media_info['Type'] == 'movie':
        file_manager.process_movie_media(filenames, media_info, ROOT_DIR, path)
    elif media_info['Type'] == 'series':
        file_manager.process_series_media(filenames, media_info, ROOT_DIR, path)


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
