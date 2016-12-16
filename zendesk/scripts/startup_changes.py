"""
Ensures that any changes made to "posts" while track-changes.py
wasn't running are fixed.
"""

import os
import shutil

import renderer

import file_constants

from filecmp import dircmp

FILE_FORMATS = file_constants.FILE_FORMATS

def sync_offline_changes(first, second):
    # Delete files/dirs that are no longer in the posts folder.
    content_not_in_posts(dircmp(first, second))
    # Add/modify files/dirs that aren't up to date in the out folder.
    content_not_in_out(dircmp(first, second))
    # Recursively search all dirs in posts and out.
    dirs = next(os.walk(first))[1]
    for index in range(0, len(dirs)):
        post = first + "/" + dirs[index]
        out = second + "/" + dirs[index]
        postmtime = os.path.getmtime(post)
        outmtime = os.path.getmtime(out)
        # Check if a directory in post has been modified.
        if postmtime != outmtime:
            # Recursively fix the folders
            sync_offline_changes(post, out)
            # Make the mtimes equal since the folders are the same now.
            os.utime(out, (os.path.getatime(post), postmtime))

        # Process all posts that have been modified.
        updates = dircmp(post, out).diff_files
        for item in updates:
            path = post.replace(post.split("/")[0] + "/", '') + "/" + item
            renderer.render_local_viewing(path)


def content_not_in_posts(comp):
    in_out = comp.right_only
    for item in in_out:
        shutil.rmtree(comp.right + "/" + item, ignore_errors=True)


# The function updates the "out" folder with files that were changed in "posts"
# while track-changes wasn't running.
def content_not_in_out(comp):
    # Left is stuff in posts.
    left = comp.left
    # Right is stuff in out.
    right = comp.right
    in_posts = comp.left_only
    for item in in_posts:
        # The items are folder names (aka article ids).
        if (item.endswith(FILE_FORMATS)) and (item[-10:] != "title.html"):
            # For the case that there are files not in the article folders.
            path = right.replace(right.split("/")[0] + "/", '') + "/" + item
            open(right + "/" + item, 'a').close()
            renderer.render_local_viewing(path)
        elif (item != ".DS_Store") and (item[-10:] != "title.html"):
            # For the case that there are new folders and files within them.
            os.makedirs(right + "/" + item)
            # Process all files within new directories.
            files_in_folder = next(os.walk(left + "/" + item))[2]
            for files in files_in_folder:
                if files != '.DS_Store' and files != 'title.html':
                    path = item + "/" + files
                    open(right + "/" + path, 'a').close()
                    renderer.render_local_viewing(path)
            # Append directories within a directory to ensure they are processed.
            dirs_in_folder = next(os.walk(left + "/" + item))[1]
            for dirs in dirs_in_folder:
                in_posts.append(item + "/" + dirs)
