import os
from torrentool.api import Torrent
from pathvalidate import sanitize_filename

torrents_path = input("Enter torrent folder path:")  # Path to folder containing torrent files
if not torrents_path.endswith("\\"):
    torrents_path = torrents_path + "\\"

for subdir, dirs, files in os.walk(torrents_path):
    for filename in files:
        filepath = subdir + os.sep + filename
        # Only rename files ended with .torrent extension
        if filepath.endswith(".torrent"):
            torrent = Torrent.from_file(filepath)
            # Sanitize file name to prevent invalid characters
            torrent_name = sanitize_filename(torrent.name)

            if not os.path.isfile(torrents_path + torrent_name + ".torrent"):
                os.rename(filepath, torrents_path + torrent_name + ".torrent")
            else:  # In case duplicate torrent file name
                # If ABC.torrent exists, rename to ABC 1.torrent, ABC 2.torrent, etc.
                counter = 1
                while os.path.isfile(torrents_path + torrent_name + " " + str(counter) + ".torrent"):
                    counter += 1
                os.rename(filepath, torrents_path + torrent_name + " " + str(counter) + ".torrent")

print("Rename complete")
