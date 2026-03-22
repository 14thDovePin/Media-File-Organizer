""" June 30, 2025
What is this script about?
This script formats any Movie or Series file names into their proper
titles that are readable by Plex's media file namescheming.

How does it work?
Below is the script's procedure. (may change as the script is developed)

1. Locate the files for the media.
2. Determine media type.
3. Obtain the title from the movies metadata from OMDb or IMDb.
4. Format title to Plex's media file namescheming.
5. Rename all media files.

External Libraries Used:
  colorama
  dotenv
  googlesearch-python

Developer Notes
I overengineered this a little bit. But that's part
of trying to implement new things I've learned!
"""
import os

from file_manager import prompt_media_info
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


TEST_MODE = False


def main():
    # Prompt the user for the information of the media to be used.
    media_directory, directory_name, filenames = prompt_media_info()

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
    while True:
        main()
