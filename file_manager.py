import json
import os
import re

from colorama import Fore

from utils.colors import Colors
from utils.data_sets import file_extensions, video_qualities, VIDEO_EXTENSIONS, SUBTITLE_EXTENSIONS


FE = file_extensions()
VQ = video_qualities()


def process_movie_media(filenames:list, media_info:dict, root_dir:str, path:str) -> None:
    """Process a movie type media directory."""
    files_information = []
    media_file : dict = None
    subtitle_file : dict = None

    # Process directory files.
    for file in filenames:
        files_information.append(parse_filename(file))

    # Scan media and subtitle files.
    for file in files_information:
        title_check = media_info['Title'].lower() in file['title'].lower()
        media_extension_check = file['file_extension'] in VIDEO_EXTENSIONS
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
    media_file_path = os.path.join(root_dir, media_file['file_name'])

    if not os.path.exists(media_file_path):
        raise Exception("Media File Path Error!")

    # Construct new name.
    new_media_file_path = os.path.join(root_dir, base_filename +'.'+ media_file['file_extension'])

    # Rename files.
    os.rename(media_file_path, new_media_file_path)

    #
    # Process Subtitle File
    #

    if subtitle_file:
        # Precheck file existence.
        subtitle_file_path = os.path.join(root_dir, subtitle_file['file_name'])

        if not os.path.exists(subtitle_file_path):
            raise Exception("Subtitle File Path Error!")

        # Construct new name.
        new_subtitle_file_path = os.path.join(root_dir, base_filename +'.'+ subtitle_file['file_extension'])

        # Rename files.
        os.rename(subtitle_file_path, new_subtitle_file_path)

    root_path = path.split('\\')
    root_path = '\\'.join(root_path[:-1])
    new_root_directory = os.path.join(root_path, base_filename)

    os.rename(root_dir, new_root_directory)


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


def parse_filename(filename:str) -> dict:
    """Parse a given filename or directory name for its media related information.

    Parameters
    ----------
    **dir_name** : str

    Returns
    -------
    dict
        title : str
        year : int
        type : str
            "movie" or "series"
        imdb_id: str
        season_number : int
        episode_number : int
        dir_name : str
            The directory name given to this function.
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


def check_video(filename: str) -> bool:
    """Check if filename is a video by its extension."""
    for ext in FE:
        if ext in filename:
            return True

    return False


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