import re
import time
import json
import logging
from .errors import InvalidURL
from .downloader import FileDownloader

log = logging.getLogger(__name__)

base_url = 'https://api.mangadex.org'
uploads_url = 'https://uploads.mangadex.org'

def validate_url(url):
    """Validate mangadex url and return the uuid"""
    re_url = re.compile(r'https:\/\/mangadex\.org\/title\/([a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})')
    match = re_url.match(url)
    if match is None:
        raise InvalidURL('Invalid MangaDex URL')
    return match.group(1)

def download(url, file, progress_bar=True, replace=False, **headers):
    """Shortcut for :class:`FileDownloader`"""
    downloader = FileDownloader(
        url,
        file,
        progress_bar,
        replace,
        **headers
    )
    downloader.download()
    downloader.cleanup()

def write_details(manga, path):
    data = {}
    data['title'] = manga.title
    data['author'] = manga.author
    data['artist'] = manga.artist
    data['description'] = manga.description
    data['genre'] = manga.genres
    data['status'] = manga.status
    with open(path, 'w') as writer:
        writer.write(json.dumps(data))