"""
Python script to process image URLs and file references.
"""

import re
import sys
import os

from colorama import init
from colorama import Fore

init()

def render_zendesk_deployment(cloudfront_url, article_id):
    article = article_id + "/index.html"
    # If the article has never been deployed, create a folder.
    if not(os.path.exists("site/" + article_id)):
        os.makedirs("site/" + article_id)
    original = open("posts/" + article)
    # If the article doesn't exist, return an error.
    if not original:
        sys.exit(1)
    if os.path.exists("site/" + article):
        os.remove("site/" + article)
    fixed_file = open("site/" + article, 'a')
    # Process images to add cloudfront url.
    for line in original.readlines():
        fix_lines(line, fixed_file, article_id, cloudfront_url)
    original.close()
    fixed_file.close()

def render_local_viewing(article):
    original = open("posts/" + article)
    os.remove("out/" + article)
    fixed_file = open("out/" + article, 'a')
    title_path = "posts/" + article.split("/")[0] + "/title.html"
    
    if os.path.isfile(title_path) and article.endswith('html'):
        title = open(title_path)
        # Add title to the local file.
        fixed_file.write("<h2>" + title.readline() + "</h2>")

    # Give local references to all images and article references.
    for line in original.readlines():
        fix_lines(line, fixed_file, "local_viewing", None)

    original.close()
    fixed_file.close()

def fix_lines(line, fixed_file, article_id, cloudfront_url):
    while True:
        image = re.search('src="([A-Z,a-z,1-9,\-,_,/,\.]*)">', line)

        # If there aren't any images there is nothing to be done.
        if not image:
            break
        # Format of replace_image is src="image-name">
        replace_image = image.group(0)
        img_name = image.group(1)

        if article_id == "local_viewing":
            # Prepare the image references for local viewing.
            line = line.replace(replace_image, "src=\"" + img_name + "\" style=\"max-width:50%\">")
        else:
            # Prepare the image references for Zendesk viewing.
            line = line.replace(replace_image, "src=\"" + cloudfront_url + "/" + article_id + "/" + img_name + "\">")
            if not img_name in os.listdir("posts/" + article_id):
                print(Fore.RED + "Warning: %s is not in your local folder and won't show up on the website." % img_name + Fore.RESET)

    while True:
        match = re.search('href=\"([0-9]*)\"', line)

        # If there aren't any references to other articles, break.
        if not match:
            break

        referenced_article_id = match.group(1)

        if article_id == "local_viewing":
            line = line.replace(referenced_article_id,"../" + referenced_article_id + "/index.html")
        else:
            line = line.replace(referenced_article_id,"./" + referenced_article_id)

    # Writes the lines to the fixed_file.
    fixed_file.write(line)
