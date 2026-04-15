'''
Create a simulation directory containing media files by
mirroring an actual directory full of it. Each file created
is an empty file containing no data. Its purpose is to
fullfill the testing needs of this project.
'''

import os


DIRECTORY = os.path.join(os.getcwd(), 'test', 'simulated_media_files.ignore')


def main():
    # Prompt the directory to be copied.
    while True:
        root_directory = input('Enter Root Directory: ')
        if os.path.exists(root_directory):
            break

    directory_scheme = []
    file_scheme = []

    # Build the directory and file scheme by walking the specified root directory.
    for path, directories, filenames in os.walk(root_directory):
        path = path.replace(root_directory, DIRECTORY)

        for i in directories:
            directory_scheme.append(os.path.join(path, i))

        for i in filenames:
            file_scheme.append(os.path.join(path, i))

    # Create and write the directories and files respectively.
    for directory in directory_scheme:
        os.makedirs(directory)

    print("Directories Created: ", len(directory_scheme))

    for file in file_scheme:
        with open(file, 'w') as f:
            pass

    print("Files Created: ", len(file_scheme))


if __name__ == "__main__":
    main()
