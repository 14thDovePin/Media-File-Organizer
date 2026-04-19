from utils.data_sets import exit_list


EXIT_LIST = exit_list()


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
