from pick import pick

from utils.data_sets import exit_list


EXIT_LIST = exit_list()


def select_result(search_result:dict, media_title) -> dict:
    """Return the chosen search result by the user."""
    # Construct title and choices.
    title = f'Search Results From [{media_title}]'
    titles = search_result['Search']
    title_list = [f"[{i['imdbID']}] {i['Title']}" for i in titles]

    # Prompt user to pick.
    option, index = pick(title_list, title)

    # Detail pick to user.
    # Final Confirmation.

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
