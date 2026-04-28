import os

from pick import pick

from utils.data_sets import exit_list
from request_manager import detailed_omdb_search


EXIT_LIST = exit_list()


def select_result(search_result:dict, media_title) -> dict:
    """Return the chosen search result by the user."""
    index = 0

    while True:

        # Construct title and choices.
        title = f'Select the Correct Media from the Search Results of [{media_title}]'
        titles = search_result['Search']
        title_list = [f"[{i['imdbID']}] {i['Title']}" for i in titles]

        # Prompt user to pick.
        option, index = pick(title_list, title, default_index=index)

        # Detail pick to user for final confirmation.
        response = detailed_omdb_search(titles[index]['imdbID'])

        confirm = final_confirmation(response)

        if confirm:
            break

    return titles[index]


def final_confirmation(media_info:dict) -> bool:
    """Prompts user for media title final confirmation."""

    # Cut plot to proper length of 72 characters.
    words = [i+' ' for i in media_info['Plot'].split(' ')]
    column = 10  # Start out at 10 to include `Plot ---> `.
    max_line_length = 72
    list_length = -1

    for word in words[:]:
        column += len(word)
        list_length += 1

        # Move words into new line when column reaches max_line_length.
        if column >= max_line_length:
            words.insert(list_length, '\n\t')
            list_length += 1
            column = 8 + len(word)  # Start out at 8 to include tab.

    # Finalize and filter list, and combine plot into text.
    words.insert(0, '\nPlot ---> ')

    if words[-1] == '\n\t':
        words.pop()

    plot = ''.join(words)

    text = \
        "\nSelected Media Details..." \
        "\n=========================" \
        f"\nTitle --> {media_info['Title']}" \
        f"\nYear ---> {media_info['Year']}" \
        f"\nIMDd ID > {media_info['imdbID']}" \
        f"\nType ---> {media_info['Type'].title()}" \

    text += plot

    # Prompt user to pick again or proceed.
    choices = ['Deny & Pick Again', 'Confirm & Proceed to Processing']

    _, index = pick(choices, text)

    if index == 1:
        return True
    else:
        return False


def update_year(media_data:dict):
    """Update the year of a given media_data."""
    print('\nLeave blank if no changes are needed. Enter `none` if user wishes to remove the current year listed.\n')
    while True:

        new_year = input("Enter New Year: ")

        # Exit if promted.
        if new_year in EXIT_LIST:
            exit()

        if not new_year:
            break

        if new_year.lower() == 'none':
            media_data['year'] = None
            break

        try:
            new_year = int(new_year)
        except:
            print('Invalid Year!')
            continue

        media_data['year'] = new_year
        break


def update_title(media_data:dict):
    """Update the title of a given media_data."""
    while True:

        new_title = input("Enter New Title: ")

        # Exit if promted.
        if new_title in EXIT_LIST:
            exit()

        if not new_title:
            continue
        else:
            media_data['title'] = new_title
            break


def root_directory() -> str:
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
