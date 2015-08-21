"""
Python script to download all images from Zendesk.
"""

import re
import os
import urllib

def main():
    article_ids = next(os.walk("posts"))[1]
    for ids in article_ids:
        print "Processing article #" + str(ids)
        download_images("posts/" + ids)

def download_images(image_path):
    body = open(image_path + "/index.html", 'r+')
    for line in body:
        image = re.search('src="([A-Z,a-z,0-9,\-,:,_,/,\.]*)">', line)
        # Only download if there is an image
        if image:
            image_url = image.group(1)
            image_name = image_url.split("/")[-1]
            urllib.urlretrieve(image_url, image_path + "/" + image_name)
            print "Downloaded: " + image_name

if __name__ == '__main__':
    main()
