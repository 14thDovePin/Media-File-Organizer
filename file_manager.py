import json
import os
import re

from request_manager import extract_series_ids, detailed_omdb_search
from utils.data_sets import file_extensions, video_qualities, VIDEO_EXTENSIONS, SUBTITLE_EXTENSIONS
from utils import filter, format


FE = file_extensions()
VQ = video_qualities()
PROCESSED_DIRECTORY = '.Processed_Media'


def process_series_media(filenames:list, media_info:dict, root_dir:str, path:str) -> None:
    """Process a series type media directory."""

    # Create the destination directory.
    processed_directory = os.path.join('\\'.join(root_dir.split('\\')[:-1]), PROCESSED_DIRECTORY)
    destination_directory = os.path.join(processed_directory, filter.windows_file_namescheme(media_info['Title']))

    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    print("Parsing files & episode list...")

    # Parse files.
    parsed_files = [parse_filename(i) for i in filenames]

    # Extract & parse IMDb IDs of each episode of the given season.
    episode_ids = extract_series_ids(media_info['imdbID'])
    parsed_episodes = [detailed_omdb_search(id) for id in episode_ids]

    # Check for any bad data within the parsed episodes.
    for episode in parsed_episodes[:]:
        if episode['Season'] == 'N/A' or episode['Episode'] == 'N/A':
            print(f"### BAD DATA!!! ['{episode['imdbID']}']")
            parsed_episodes.remove(episode)

    # Work through each media file and rename them accrodingly.
    for file in parsed_files:
        for episode in parsed_episodes:
            # Check if file is media related.
            if file['season_number'] == None or file['episode_number'] == None:
                continue

            # Match file & episode.
            omdb_results_season = int(episode['Season'])
            omdb_results_episode = int(episode['Episode'])

            season_check = int(file['season_number']) == int(episode['Season'])
            episode_check = int(file['episode_number']) == int(episode['Episode'])

            if season_check and episode_check:
                # Setup and filter filename.
                sn = format.se_number(omdb_results_season)
                en = format.se_number(omdb_results_episode)

                episode_name = filter.windows_file_namescheme(episode['Title'])
                title = filter.windows_file_namescheme(media_info['Title'])
                filename = title + f" S{sn}E{en} {episode_name}.{file['file_extension']}"
                current_filename = os.path.join(root_dir, file['file_name'])
                final_filename = os.path.join(destination_directory, f'Season {sn}', filename)

                print(f"Processing [{current_filename.split('\\')[-1]}]")

                # Rename files and create the necessary directories.
                dir_structure = '\\'.join(final_filename.split('\\')[:-1])

                if not os.path.exists(dir_structure):
                    os.makedirs(dir_structure)

                os.rename(current_filename, final_filename)

    # Cleanup root directory if its empty.
    walk = os.walk(root_dir)
    _, directories, files = next(walk)

    if len(directories) == 0 and len(files) == 0:
        os.rmdir(root_dir)

    print(f'↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓')
    print(f"Finished Processing Series [{media_info['Title']}]")
    print(f'==========================')


def process_movie_media(filenames:list, media_info:dict, root_dir:str, path:str) -> None:
    """Process a movie type media directory."""
    # Create processed directory.
    base_filename = filter.windows_file_namescheme(f"{media_info['Title']} ({media_info['Year']})")
    processed_directory = os.path.join('\\'.join(root_dir.split('\\')[:-1]), PROCESSED_DIRECTORY, base_filename)

    if not os.path.exists(processed_directory):
        os.makedirs(processed_directory)

    # Process directory files.
    files_information = []

    for file in filenames:
        files_information.append(parse_filename(file))

    # Assume that only one movie file and an optional subtitle file is present.
    media_file : dict = None
    subtitle_file : dict = None

    # Scan files.
    for file in files_information:
        media_extension_check = file['file_extension'] in VIDEO_EXTENSIONS
        subtitle_extension_check = file['file_extension'] in SUBTITLE_EXTENSIONS

        if media_extension_check:
            media_file = file

        if subtitle_extension_check:
            subtitle_file = file

        if media_file and subtitle_file:
            break

    # Process media and subtitle files.
    if media_file:
        rename_file(root_dir, processed_directory, media_file, base_filename, media_file['file_extension'])

    if subtitle_file:
        rename_file(root_dir, processed_directory, subtitle_file, base_filename, subtitle_file['file_extension'])

    # Cleanup root directory if its empty.
    walk = os.walk(root_dir)
    _, directories, files = next(walk)

    if len(directories) == 0 and len(files) == 0:
        os.rmdir(root_dir)

    print(f'↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓')
    print(f"Finished Processing Movie [{media_info['Title']}]")
    print(f'=========================')


def rename_file(root_dir, processed_dir, media_file, base_filename, file_extension):
    """Rename a a file given its details and the file extension wanted."""
    # Precheck file existence.
    file_path = os.path.join(root_dir, media_file['file_name'])

    if not os.path.exists(file_path):
        raise Exception("Media File Path Error!")

    # Construct new name.
    new_file_path = os.path.join(processed_dir, base_filename +'.'+ file_extension)

    # Rename files.
    print(f"Processing [{file_path.split('\\')[-1]}]")
    os.rename(file_path, new_file_path)


def parse_filename(filename:str) -> dict:
    """Parse a given filename or directory name for its media related information.

    Parameters
    ----------
    **dir_name** : str

    Returns
    -------
    dict
    - title : str
    - year : int
    - type : str
        - "movie" or "series"
    - imdb_id: str
    - season_number : int
    - episode_number : int
    - file_extension : str
    - file_name : str
    - dir_name : str
        - The directory name given to this function.

    """
    ignore_case = re.IGNORECASE

    # Patterns
    year_pattern = r'19\d\d|20\d\d'
    season_pattern = r'[\d\s.]SEASON[\s.]?(\d+)|SEASON|[\d\s.]?S(\d+)'
    episode_pattern = r'[\d\s.]EPISODE[\s.]?(\d+)|EPISODE|[\d\s.]?EP?(\d+)'
    enclosed_pattern = r'[\s.]?\([^\)]+\)|[\s.]?\[[^\]]+\]'
    word_pattern = r'[^. \s]+'

    media_data = {
        "title": None,
        "year": None,
        "type": None,
        "imdb_id" : None,
        "season_number": None,
        "episode_number": None,
        "file_extension": None,
        "file_name": None,
        "directory_name" : None
    }

    # Parse data into dictionary.

    # Extract Year
    year = re.search(year_pattern, filename)

    if year:
        year = year.group(0)
        media_data["year"] = int(year)

    # Extract Season Number
    season = re.search(season_pattern, filename, ignore_case)

    if season:
        if season.group(1):
            media_data['season_number'] = season.group(1)
        else:
            media_data['season_number'] = season.group(2)

        if media_data['season_number'] != None:
            media_data['season_number'] = int(media_data['season_number'])

    # Extract Episode Number
    episode = re.search(episode_pattern, filename, ignore_case)

    if episode:
        if episode.group(1):
            media_data['episode_number'] = episode.group(1)
        else:
            media_data['episode_number'] = episode.group(2)

        if media_data['episode_number'] != None:
            media_data['episode_number'] = int(media_data['episode_number'])

    # Extract file extension if filename is a file.
    directory = True
    extension = None
    potential_extension = filename.split('.')[-1]

    if potential_extension in FE:
        directory = False
        extension = potential_extension

    if not directory:
        media_data['file_extension'] = extension
        media_data['file_name'] = filename
    else:
        media_data['directory_name'] = filename

    # Determine Title Type
    if media_data['season_number'] or media_data['episode_number']:
        media_data['type'] = 'series'

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
        if word in FE:
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

        # Dash
        if '-' == word:
            store_index = True

        # Store Index
        if store_index:
            indexes.append(word_sequence.index(word))

    if indexes:
        final_index = min(indexes)
        word_sequence = word_sequence[:final_index]

    media_data["title"] = " ".join(word_sequence)

    return media_data


if __name__ == "__main__":
    files_and_directories = []
    directories = []
    walk = os.walk("test\\simulated_media_files.ignore")

    for _, dirs, files in walk:
        for i in dirs:
            files_and_directories.append(i)
            directories.append(i)

        for i in files:
            files_and_directories.append(i)

    print(len(files_and_directories))

    test_results = list()

    for i in files_and_directories:
        test_results.append(parse_filename(i))

    # for i in test_results: print(i)
    # print(len(test_results))

    dir_test_results = []

    for i in files_and_directories:
        dir_test_results.append(parse_filename(i))

    # for i in dir_test_results: print(i)
    # print(len(dir_test_results))

    with open('media_information_parse_check.ignore.json', 'w') as f:
        import json
        data = json.dumps(dir_test_results, indent=2)
        f.writelines(data)