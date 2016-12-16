"""
Python script to create a new article in a given section id.
"""

import os
import sys

from zdesk import Zendesk

from scripts import file_constants

from colorama import init
from colorama import Fore

init()

def _create_shell(section_id):

    # Get subdomain.
    try:
        subdomain = os.environ["ZENDESK_SUBDOMAIN"]
        url = file_constants.get_url_from_subdomain(subdomain)
    except KeyError:
        print(Fore.RED + "Please set the environment variable ZENDESK_SUBDOMAIN" + Fore.RESET)
        sys.exit(1)

    # Get username.
    try:
        username = os.environ["ZENDESK_USR"]
    except KeyError:
        print(Fore.RED + "Please set the environment variable ZENDESK_USR" + Fore.RESET)
        sys.exit(1)

    # Get password.
    try:
        password = os.environ["ZENDESK_PWD"]
    except KeyError:
        print(Fore.RED + "Please set the environment variable ZENDESK_PWD" + Fore.RESET)
        sys.exit(1)

    zendesk = Zendesk(url, username, password)

    # Add a temporary title and leave it in draft mode.
    new_article = {"article": {"title": "Temporary Title", "draft": True}}

    response = zendesk.help_center_section_article_create(id = section_id, data = new_article)

    # Report success.
    print('Successfully created the article.')

    # Create the article shell locally.
    article_id = response['article']['id']
    _empty_article(str(article_id))


def _empty_article(article_id):
    article = "posts/" + article_id + "/index.html"
    title = "posts/" + article_id + "/title.html"
 
    if article_id.isdigit() and not os.path.isfile(article):
        # Makes the folder for the article and pictures to be placed in.
        os.makedirs('posts/' + article_id)
        # Create the article and title shell.
        open(article, 'a').close()
        open(title, 'a').close()
        # Provides the user with the location of the html file that was created.
        print "The article is located at " + article
        print "Enter the article's title at " + title
    elif os.path.isfile(article):
        print (Fore.RED + "Error: This article ID already exists: " + article_id + Fore.RESET)
        sys.exit(1)
    else:
        print (Fore.RED + "Error: This article ID is invalid: " + article_id + Fore.RESET)
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print('Usage: python %s <section_id>' % sys.argv[0])
    else:
        _create_shell(sys.argv[1])
