import pathlib
import re
import logging

from globals import ROOT_DIR
from youtube_cc import archive_youtube
from web_clipper import archive_web

def setup():
    """Ensures that all necessary folders exist.
    """
    archive_path = pathlib.Path(ROOT_DIR, "archive")
    paths = [
        pathlib.Path(ROOT_DIR, "logging"),
        pathlib.Path(archive_path, "web"),
        pathlib.Path(archive_path, "youtube")
    ]
    for path in paths:
        path.mkdir(exist_ok=True)

def archive_url(url):
    """Archives the provided URL in a lightweight form.

    Currently supported:
    - YouTube (subtitles saved as ttml files)
    - General websites (saved as Markdown files)

    Args:
        url (str): URL to archive
    """    
    # We want to make sure the archive folders exist
    setup()
    youtube_pattern = re.compile(r".*youtube.com.*")
    if re.search(pattern=youtube_pattern, string=url):
        archive_youtube(youtube_url=url)
        logging.info("Archived subtitles of video at URL %s", url)
    else:
        archive_web(url=url)
        logging.info("Archived webpage at URL %s", url)