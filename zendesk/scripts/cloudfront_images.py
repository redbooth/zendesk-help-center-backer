"""
Push images to CloudFront.
"""

import os
import sys
import hashlib

import file_constants

import boto
import boto.s3
from boto.s3.key import Key

from colorama import init
from colorama import Fore
init()

IMAGE_FORMATS = file_constants.IMAGE_FORMATS

def push_to_cloudfront(article_id):
    # Get the environment variable keys to connect with CloudFront.
    bucket_name, access_key, secret_key = get_aws_keys()
    # Establish connection with S3.
    conn = boto.connect_s3(access_key, secret_key)
    # Access the files in the folder for this article_id.
    files_in_folder = next(os.walk("posts/" + article_id))[2]
    for files in files_in_folder:
        if files.endswith(IMAGE_FORMATS):
            # Push each image.
            push(article_id, files, conn, bucket_name)


def push(article_id, img_name, conn, bucket_name):
    img_path = article_id + "/" + img_name
    post_path = "posts/" + img_path

    if not conn.lookup(bucket_name):
        # Create the bucket and connect to it if it doesn't exist.
        bucket = conn.create_bucket(bucket_name, location=boto.s3.connection.Location.DEFAULT)
    else:
        # Connect to the bucket.
        bucket = conn.get_bucket(bucket_name)
    k = Key(bucket)

    # Give the key the same name as the image.
    k.key = img_path

    local_hash = hash_check(post_path)
    # If the image path exists, check if the image has been modified.
    if k.exists():
        # Find local md5.
        local_hash = hash_check(post_path)
        # Access cloudfront md5.
        cloudfront_hash = bucket.get_key(img_path).etag[1:-1]
        if local_hash != cloudfront_hash:
            print 'Updating ' + img_path + ' in Amazon S3 bucket ' + bucket_name
            k.set_contents_from_filename(post_path)
    else:
        # If the image doesn't exist, add it.
        print 'Uploading ' + img_path + ' to Amazon S3 bucket ' + bucket_name
        k.set_contents_from_filename(post_path)


def delete_from_cloudfront(article_id):
    bucket_name, access_key, secret_key = get_aws_keys()

    # Establish connection with S3.
    conn = boto.connect_s3(access_key, secret_key)
    if not conn.lookup(bucket_name):
        # If the bucket doesn't exist, there is nothing to delete.
        return
    else:
        # Connect to the bucket.
        bucket = conn.get_bucket(bucket_name)
    # Access the images in the S3 directory for this article_id.
    for image in bucket.list(prefix = article_id):
        if not os.path.exists("posts/" + image.name):
            # If the image doesn't exist locally, delete it on CloudFront.
            print("Deleting " + image.name + " from CloudFront")
            bucket.delete_key(image.name)


def hash_check(post_path):
    # Computes the local image's md5.
    hasher = hashlib.md5()
    image = open(post_path, 'rb').read()
    hasher.update(image)
    return hasher.hexdigest()


def get_aws_keys():
    # Get the AWS bucket name.
    try:
        bucket = os.environ["ZENDESK_BUCKET_NAME"]
    except KeyError:
        print(Fore.RED + "Please set the environment variable ZENDESK_BUCKET_NAME" + Fore.RESET)
        sys.exit(1)

    # Get the AWS access key.
    try:
        access = os.environ["AWS_ACCESS_KEY"]
    except KeyError:
        print(Fore.RED + "Please set the environment variable AWS_ACCESS_KEY" + Fore.RESET)
        sys.exit(1)

    # Get the AWS secret key.
    try:
        secret = os.environ["AWS_SECRET_KEY"]
    except KeyError:
        print(Fore.RED + "Please set the environment variable AWS_SECRET_KEY" + Fore.RESET)
        sys.exit(1)

    return [bucket, access, secret]
