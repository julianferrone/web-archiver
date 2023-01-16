"""Provides functions for archiving a YouTube video from URL by downloading
the subtitles.
"""
import yt_dlp
import re
import pathlib
import shutil
from datetime import datetime as dt

from globals import ROOT_DIR
from custom_logger import create_logger

LOGGER = create_logger(name="youtube_clipper")


def download_subtitles(youtube_url):
    """Downloads subtitles for a given YouTube URL.

    Args:
        youtube_url (str): A URL pointed to a YouTube video to download the
            subtitles for.
    """    
    ydl_opts = {
        "skip_download": True,
        "subtitleslangs": ["en"],
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitlesformat": "ttml",
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])


def move_subtitles():
    """Moves all subtitle files to ./archive/youtube
    """
    today = dt.today().strftime("%Y-%m-%d")
    subtitle_pattern = re.compile(pattern=r".*\.en\.ttml")
    subtitle_paths = [
        path
        for path in ROOT_DIR.iterdir()
        if re.search(pattern=subtitle_pattern, string=str(path))
    ]
    for path in subtitle_paths:
        filename = path.name
        # Remove the .en and .ttml suffixes
        while filename.suffix in {".en", ".ttml"}:
            filename = filename.with_suffix("")
        # Then add the date and readd the suffixes
        filename += f"_{today}_.en.ttml"
        
        newpath = pathlib.Path(ROOT_DIR, "archive", "youtube", filename)
        shutil.move(src=path, dst=newpath)

def archive_youtube(youtube_url):
    """Automatically downloads the subtitles for a given YouTube video
        to the archive.

    Args:
        youtube_url (str): A URL pointed to a YouTube video to download the
            subtitles for.
    """
    pattern = re.compile(r"https:\/\/www\.youtube\.com\/watch\?v=.*")
    if not re.search(pattern=pattern, string=youtube_url):
        # We only want to archive YouTube watch videos, not the homepage
        # or search results
        return
    download_subtitles(youtube_url=youtube_url)
    move_subtitles()
    LOGGER.info(f"Archived subtitles of video at URL {youtube_url}")