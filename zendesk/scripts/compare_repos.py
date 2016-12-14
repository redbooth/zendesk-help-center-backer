"""
Python script to check if any articles were created on Zendesk instead of locally
or if any articles were deleted from Zendesk but not deleted locally.
"""

import requests
import os

from colorama import init
from colorama import Fore
init()

def compare_article_ids(url, username, password):
    zendesk_ids = []
    url += "/api/v2/help_center/articles.json"
    while url:
        response = requests.get(url, auth=(username, password))
        data = response.json()
        for article in data["articles"]:
            zendesk_ids.append(article["id"])
        url = data["next_page"]

    local_ids = next(os.walk("posts"))[1]
    local_ids.sort()
    zendesk_ids.sort()

    for ids in zendesk_ids:
        if str(ids) not in set(local_ids):
            print(Fore.RED + "WARNING: Article number %s was created directly in Zendesk and is not tracked by Git." %str(ids) + Fore.RESET)
    for ids in local_ids:
        if int(ids) not in set(zendesk_ids):
            print(Fore.RED + "WARNING: Article number %s was deleted in Zendesk but not deleted in Git." %str(ids) + Fore.RESET)

def compare_article_contents(article_id, zendesk):
    zendesk_article = zendesk.help_center_article_show(id=article_id)["article"]

    title = zendesk_article["title"]

    # If the title has changed, deploy the article.
    if title != open("posts/%s/title.html" % article_id).readline():
        return True

    # Read local body into a string to compare with zendesk body
    with open("site/%s/index.html" % article_id, "r") as myfile:
        local_body = myfile.read()

    # If the bodies are not the same, deploy the article
    if local_body != zendesk_article["body"]:
        return True

    return False


def line_count(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
