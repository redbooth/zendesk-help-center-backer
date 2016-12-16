"""
Keeps track of the changes to the "posts" folder using the watchdog api.
"""

import os
import shutil
import time

from scripts import renderer
from scripts import startup_changes
from scripts import file_constants

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

"""
Extend FileSystemEventHandler to be able to write custom on_any_event method
"""

FILE_FORMATS = file_constants.FILE_FORMATS

class MyHandler(FileSystemEventHandler):
    """
    Overwrite the methods for creation, deletion, modification, and moving to get more information
    as to what is happening on output
    """

    def on_created(self, event):
        # When files/dirs are created in the posts folder, create them in the out folder.
        path = event.src_path
        if path[-10:] == 'title.html':
            return

        out_path = "out" + path[5:]

        if path.endswith(FILE_FORMATS):
            if not(os.path.exists('out/' + path.split('/')[-2])):
                os.makedirs('out/' + path.split('/')[-2])
            open(out_path, 'a').close()
            renderer.render_local_viewing(path[6:])
        elif os.path.isdir(path):
            if not(os.path.exists(out_path)):
                os.makedirs(out_path)
        else:
            # Not dir, article, or image (aka must be temp file).
            return

        print "Created " + out_path

    def on_deleted(self, event):
        # When files/dirs are deleted in the posts folder, delete them in the out folder.
        path = event.src_path
        if path[-10:] == 'title.html':
            return

        out_path = "out" + path[5:]

        if path.endswith(FILE_FORMATS):
            os.remove(out_path)
        elif os.path.isdir(path):
            os.rmdir(out_path)
        else:
            # Not dir, article, or image (aka must be temp file).
            return
        print "Deleted: " + out_path

    def on_modified(self, event):
        # When files/dirs are modified in the posts folder, re-process them for the out folder.

        path = event.src_path

        # If title is modified, it must be modified in out folder's index.
        if path[-10:] == 'title.html':
            renderer.render_local_viewing(path[6:-10] + "index.html")
            print "Prepared out/" + path[6:-10] + "index.html for local viewing."

        # If image or index is modified, it must be modified in out folder.
        elif path.endswith(FILE_FORMATS):
            renderer.render_local_viewing(path[6:])
            print "Prepared out/" + path[6:] + " for local viewing."

    def on_moved(self, event):
        # When files/dirs are moved in the posts folder, move them in the out folder as well.
        path = event.src_path
        if path[-10:] == 'title.html':
            return
        move = event.dest_path
        out_path = "out" + path[5:]
        move_path = "out" + move[5:]

        # Check if the folder has been renamed (nothing actually moved).
        if path.split("/")[-2] != move.split("/")[-2]:
            old_name = out_path.replace("/" + path.split("/")[-1], '')
            new_name = move_path.replace("/" + move.split("/")[-1], '')
            os.rename(old_name, new_name)
            print "Renamed " + old_name + " to " + new_name
            os.rename(old_name, new_name)
        # Check if file has been moved
        elif out_path != move_path and path.endswith(FILE_FORMATS):
            shutil.move(out_path, move_path)
            print "Moved " + out_path + " to " + move_path

def main():
    # Fill all changes that occurred when track-changes.py wasn't running.
    if os.path.isdir("out"):
        shutil.rmtree("out", True)

    if not os.path.isdir("out"):
        os.mkdir("out")
 
    startup_changes.sync_offline_changes("posts", "out")

    print "Watching posts directory for changes... CTRL+C to quit."
    watch_directory = "posts"

    event_handler = MyHandler()

    # Run the watchdog.
    observer = Observer()
    observer.schedule(event_handler, watch_directory, True)
    observer.start()

    """
    Keep the script running or else python closes without stopping the observer
    thread and this causes an error.
    """
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
