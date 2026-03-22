""" July 4, 2025
DEV NOTE
This script is a special case script. It's not supposed to be
reused on other systems or for any other. This script can and will
break in the near future due to the nature of it relying on
selenium and the front end of a website entirely.
"""


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import json
import re

import website_ignore as website


TEST_MODE = False
TM_LIMIT = 5
FILENAME = "samples_ignore.json"
# Video Extensions
VE = ['webm', 'mkv', 'flv', 'vob', 'ogv', 'ogg', 'rrc', 'gifv', 'mng', 'mov',
      'avi', 'qt', 'wmv', 'yuv', 'rm', 'asf', 'amv', 'mp4', 'm4p', 'm4v',
      'mpg', 'mp2', 'mpeg', 'mpe', 'mpv', 'm4v', 'svi', '3gp', '3g2', 'mxf',
      'roq', 'nsv', 'flv', 'f4v', 'f4p', 'f4a', 'f4b', 'mod']


def grab_sample_filenames():
    """Return 50 samples each of movie & tv show file names."""
    sample_filenames = []
    driver = webdriver.Chrome()

    # Process movie file names.
    page_links = get_page_links(driver, website.movies())
    movie_links = grab_item_links(driver, page_links)
    sample_filenames += grab_filenames(driver, movie_links)

    # Process series file names.
    page_links = get_page_links(driver, website.tv_shows())
    show_links = grab_item_links(driver, page_links)
    sample_filenames += grab_filenames(driver, show_links)

    if TEST_MODE:
        print(f"\n\nSAMPLE FILENAMES: [{len(sample_filenames)}]")
        for filename in sample_filenames: print(f"\t{filename}")
        print("\n\n")

    # Store sample file names into a file.
    with open(FILENAME, 'w') as f:
        f.writelines(json.dumps(sample_filenames, indent=4))

    driver.quit()

    input("\n\nSUCCESS | PRESS ANY KEY TO CLOSE...\n\n")


def get_page_links(driver: webdriver, page: str) -> list:
    """Return the pages web links on a given link."""
    driver.get(page)

    # Grab the element containing the pages.
    page_list_elements = driver.find_elements(
        By.XPATH,
        "//div[@class='pagination']//ul//li//a"
    )

    # Extract the hrefs.
    page_links = [i.get_attribute('href') for i in page_list_elements][:-2]

    if TEST_MODE:
        page_links = page_links[:1]

    return page_links


def grab_item_links(driver: webdriver, page_links: list) -> list:
    """Return the list of the item's links from a given list of pages."""
    links = []

    # Loop through each pages.
    for page in page_links:
        if driver.current_url != page:
            driver.get(page)

        # Grab Each Item
        item_elements = driver.find_elements(
            By.XPATH,
            "//div[@class='featured-list']//div//table//tbody//tr//td//a[2]"
        )

        for item_element in item_elements:
            href = item_element.get_attribute('href')
            links.append(href)

    if TEST_MODE:
        links = links[:TM_LIMIT]

    return links


def grab_filenames(driver: webdriver, page_links: list) -> list:
    """Return a list of filenames based on a given list of pages."""
    filenames = []

    if TEST_MODE:
        limit = TM_LIMIT
    else:
        limit = 50

    for page in page_links:
        driver.get(page)

        # Limit filenames.
        if len(filenames) == limit:
            break

        # Navigate to the Files information.
        try:
            file_tab_element = driver.find_element(
                By.XPATH,
                "//div[@class='torrent-tabs']//ul//li[2]//a"
            )
        except:
            print("Failed to Grab Filename..")
            continue

        file_tab_element.click()

        try:
            file_information_element = driver.find_element(
                By.XPATH,
                "//div[@id='files']"
            )

            filename_elements = file_information_element.find_elements(
                By.TAG_NAME,
                'li'
            )
        except:
            print("Failed to Grab Filename..")
            continue

        # Pull Filename information.
        limit_pull = 0
        for filename in filename_elements:

            # Limit filenames.
            if len(filenames) == limit or limit_pull == 2:
                break

            # Filter filename.
            for extension in VE:
                if '.' + extension in filename.text:
                    limit_pull += 1
                    filenames.append(filename.text)

    return filenames


if __name__ == "__main__":
    grab_sample_filenames()
