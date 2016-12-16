"""
Python script to deploy article to Zendesk.
"""

import os
import sys

from zdesk import Zendesk

from colorama import init
from colorama import Fore

from scripts import renderer
from scripts import cloudfront_images
from scripts import compare_repos

from scripts import file_constants

init()

def _deploy(article_id, zendesk_url, cloudfront_url, username, password):
    path = "site/" + article_id + "/index.html"
    locale = "en-us"

    # Check if the article_id is valid.
    if not os.path.exists("posts/" + article_id):
        print (Fore.RED + "The article_id you entered is invalid." + Fore.RESET)
        sys.exit(1)

    title = open("posts/" + article_id + "/title.html").readline()

    if not title:
        print (Fore.RED + "Add a title to posts/" + article_id + "/title.html before deploying the article." + Fore.RESET)
        sys.exit(1)

    # Prepare files for being pushed to Zendesk.
    renderer.render_zendesk_deployment(cloudfront_url, article_id)

    # Push the images to CloudFront.
    cloudfront_images.push_to_cloudfront(article_id)

    # Delete extra images on CloudFront.
    cloudfront_images.delete_from_cloudfront(article_id)

    # Build connection to Zendesk.
    zendesk = Zendesk(zendesk_url, username, password)

    if not compare_repos.compare_article_contents(article_id, zendesk):
        return

    # Packages the data in a dictionary matching the expected JSON.
    update_article = {"translation": {"title": title, "body": open(path, mode = 'rb').read()}}

    response = zendesk.help_center_article_translation_update(article_id, locale, update_article)

    # Check if article is in Draft mode.
    check_draft = response["translation"]["draft"]
    if check_draft:
        print (Fore.YELLOW + "Reminder that article " + article_id + " is still in draft mode." + Fore.RESET)

    print "Article " + article_id + " has been updated at: " + zendesk_url + "/" + article_id


def main():
    # Get subdomain.
    try:
        cloudfront_url = os.environ["ZENDESK_CLOUDFRONT_URL"]
    except KeyError:
        print(Fore.RED + "Please set the environment variable ZENDESK_CLOUDFRONT_URL" + Fore.RESET)
        sys.exit(1)

    # Get subdomain.
    try:
        subdomain = os.environ["ZENDESK_SUBDOMAIN"]
        zendesk_url = file_constants.get_url_from_subdomain(subdomain)
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

    # Check for articles that were posted directly on Zendesk instead of locally.

    compare_repos.compare_article_ids(zendesk_url, username, password)

    if len(sys.argv) == 2:
        print (Fore.MAGENTA + "Processing Article 1/1" + Fore.RESET)
        _deploy(sys.argv[1], zendesk_url, cloudfront_url, username, password)
    else:
        article_ids = next(os.walk("posts"))[1]
        i = 1
        for article_id in article_ids:
            print (Fore.MAGENTA + "Processing Article %s/%s %s" % (str(i), len(article_ids), article_id) + Fore.RESET)
            _deploy(article_id, zendesk_url, cloudfront_url, username, password)
            i += 1

    print "="*40
    print(Fore.GREEN + "SUCCESSFULLY FINISHED DEPLOYMENT" + Fore.RESET)
