import pathlib
import re
import logging

from globals import ROOT_DIR
from youtube_cc import archive_youtube
from web_clipper import archive_web


def setup():
    """Ensures that all necessary folders exist."""
    archive_path = pathlib.Path(ROOT_DIR, "archive")
    paths = [
        pathlib.Path(ROOT_DIR, "logging"),
        pathlib.Path(archive_path, "web"),
        pathlib.Path(archive_path, "youtube"),
    ]
    for path in paths:
        path.mkdir(exist_ok=True)


def get_blacklist():
    """Provides a list of blacklisted URLs (that we don't want to archive)"""
    with open("blacklist.txt", mode="r") as f:
        # For each url in blacklist.txt,
        # create a regex pattern which checks for 0+ of any character
        # before and after the url
        blacklist = [line.rstrip("\n") for line in f]
    return blacklist


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
    # Check that the input URL is not a blacklisted URL
    blacklisted_urls = [re.compile(rf".*{url}.*") for url in get_blacklist()]

    for blacklisted_pattern in blacklisted_urls:
        if re.search(blacklisted_pattern, url):
            print(f"URL {url} is in the blacklist, not archiving")
            return
    # Archive YouTube videos with the custom YouTube archiver
    youtube_pattern = re.compile(r".*youtube.com.*")
    if re.search(pattern=youtube_pattern, string=url):
        archive_youtube(youtube_url=url)
        print(f"Archived subtitles of video at URL {url}")
    # Archive all other websites using the webpage archiver
    else:
        archive_web(url=url)
        print(f"Archived webpage at URL {url}")