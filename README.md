# Rename torrent from hash

If your torrent client renamed your torrent's filename to its hash and you want to rename it back to torrent's name, this Python 3 script will help you do that.

## Dependency

* [torrentool](https://github.com/idlesign/torrentool)
* [pathvalidate](https://github.com/thombashi/pathvalidate)

To install, run this command:
```
pip install --upgrade -r requirements.txt
```

## Usage

Run the script with this command:

```
python rename-from-hash.py
```

and then enter path to folder that contain the torrent filename you want to fix. It will automatically rename all the torrent files to their corresponding name.

Note: If torrent name already exist, it will add a number before the ``.torrent`` extension.