from pick import pick

from utils.data_sets import exit_list
from request_manager import detailed_omdb_search


EXIT_LIST = exit_list()


def final_confirmation(searchResult:dict, dir:str) -> bool:
    """Prompts user for media title final confirmation."""
    print("\nMedia Details...")
    print("================")
    print(f"Title -----> {searchResult['Title']}")
    print(f"IMDb ID ---> {searchResult['imdbID']}")
    print(f"Directory -> {dir}")
    print("================")

    input("Press any key to continue...")

    text = "Confirm Media to Rename"
    choices = ['Confirm', 'Deny & Go Back']

    _, index = pick(choices, text)

    if index == 0:
        return True
    else:
        return False


def select_result(search_result:dict, media_title) -> dict:
    """Return the chosen search result by the user."""
    while True:

        # Construct title and choices.
        title = f'Search Results From [{media_title}]'
        titles = search_result['Search']
        title_list = [f"[{i['imdbID']}] {i['Title']}" for i in titles]

        # Prompt user to pick.
        option, index = pick(title_list, title)

        # Detail pick to user for final confirmation.
        response = detailed_omdb_search(titles[index]['imdbID'])

        print("\nSelected Media Details...")
        print("=========================")
        print(f"Title --> {response['Title']}")
        print(f"Year ---> {response['Year']}")
        print(f"IMDd ID > {response['imdbID']}")
        print(f"Type ---> {response['Type'].title()}")
        print(f"Plot ---> {response['Plot']}")
        print("=========================")
        input("Press any key to continue...")

        text = f"Confirm Selected Media [{response['Title']} {response['Year']}]?"

        # Final Confirmation.
        _, final_confirmation_index = pick(['Confirm & Continue', 'Deny & Go Back'], text)

        if final_confirmation_index == 1:
            continue
        else:
            break

    return titles[index]


def update_title(media_data:dict):
    """Update the title of a given media_data."""
    while True:

        new_title = input("Enter New Title: ")

        # Exit if promted.
        if new_title in EXIT_LIST:
            exit()

        if not new_title:
            break
        else:
            media_data['title'] = new_title
            break


def update_year(media_data:dict):
    """Update the year of a given media_data."""
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
