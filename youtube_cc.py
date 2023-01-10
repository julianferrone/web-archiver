import yt_dlp
import re
import pathlib
import shutil

ROOT_DIR = pathlib.Path(__file__).parent


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
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])


def move_subtitles():
    """Moves all subtitle files to ./archive/youtube
    """    
    subtitle_pattern = re.compile(pattern=r".*\.en\.ttml")
    subtitle_paths = [
        path
        for path in ROOT_DIR.iterdir()
        if re.search(pattern=subtitle_pattern, string=str(path))
    ]
    for path in subtitle_paths:
        newpath = pathlib.Path(ROOT_DIR, "archive", "youtube", path.name)
        shutil.move(src=path, dst=newpath)
        print(f"Moved {path} to {newpath}")

def archive_youtube(youtube_url):
    """Automatically downloads the subtitles for a given YouTube video
        to the archive.

    Args:
        youtube_url (str): A URL pointed to a YouTube video to download the
            subtitles for.
    """    
    download_subtitles(youtube_url=youtube_url)
    move_subtitles()