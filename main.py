from argparse import ArgumentParser, Namespace
import os
from pathlib import Path
from shutil import copy, move
from typing import List

from torrentool.api import Torrent
from tqdm import tqdm


def rename(old_path: Path, new_path: Path, remove_file: bool):
    """Either move or file

    Args:
        old_path (Path): Old path to file
        new_path (Path): New path to file
        remove_file (bool): If set to True, move the file. Else, copy the file.
    """
    old_path = old_path.as_posix()
    new_path = new_path.as_posix()

    if remove_file:
        move(old_path, new_path)
    else:
        copy(old_path, new_path)


def main(args: Namespace):
    input_dir = Path(args.input)
    if args.dest is not None:
        dest_dir = Path(args.dest)

        # Create destination directory if not exists
        if not dest_dir.exists():
            os.makedirs(dest_dir)
    else:
        # Default to original directory if not set
        dest_dir = input_dir
    remove_file = args.remove
    print(dest_dir)

    files: List[Path] = [file for file in input_dir.iterdir()]

    for file in tqdm(files):
        # Ignore folders
        # TODO: implement recursive renaming
        if not file.is_file():
            continue

        # Ignore non ".torrent" files
        if not file.suffix.lower() == ".torrent":
            continue

        try:
            torrent = Torrent.from_file(file)
        except Exception:
            print(f"Encountered an error with {file.as_posix()}. Skipping.")
            continue

        torrent_name = torrent.name

        # Initial rename
        new_path: Path = dest_dir / f"{torrent_name}.torrent"
        if not new_path.exists():
            rename(file, new_path, remove_file)
            continue  # Move to next file

        # In case destination file already exists (due to duplicate torrent name),
        # add extra number
        success = False
        idx = 2
        while not success:
            new_path: Path = dest_dir / f"{torrent_name} {idx}.torrent"
            if new_path.exists():
                idx += 1
                continue

            rename(file, new_path, remove_file)
            success = True

if __name__ == "__main__":
    parser = ArgumentParser(description="Rename torrent hash file to its original name.")
    parser.add_argument("input", type=str, help="Path to input folder")
    parser.add_argument("-d",
                        "--dest",
                        type=str,
                        help="Path to destination folder",
                        required=False,
                        default=None)
    parser.add_argument("-r",
                        "--remove",
                        action="store_true",
                        help="Remove original file",
                        required=False,
                        default=False)

    main(parser.parse_args())
