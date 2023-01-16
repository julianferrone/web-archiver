from dataclasses import dataclass
import requests
import pathlib
import re
from markdownify import markdownify as md
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
from htmldate import find_date
from readability.readability import Document

from globals import ROOT_DIR
from custom_logger import create_logger

LOGGER = create_logger(name="web_clipper")

@dataclass
class WebpageClipping:
    author: str
    source: str
    clipped_date: str
    published_date: str
    tags: str
    title: str
    markdown: str


def clip_webpage(url):
    """Clips a webpage.

    Args:
        url (str): The URL of the webpage to archive.

    Returns:
        WebpageClipping: The contents (and some metadata)
            of the webpage.
    """
    response = requests.get(url)

    soup = bs(response.text, "html.parser")
    byline_soup = soup.find(class_="byline")
    today = dt.today().strftime("%Y-%m-%d")
    published = find_date(response.text)
    TAGS = "#clippings"

    readable = Document(response.text)
    title = readable.title()
    source = f"[{title}]({url})"
    markdowned = md(readable.summary())

    return WebpageClipping(
        author=byline_soup,
        source=source,
        clipped_date=today,
        published_date=published,
        tags=TAGS,
        title=title,
        markdown=markdowned,
    )


def format_clipping(clipping):
    """Formats a WebpageClipping into a Markdown string.

    Args:
        clipping (WebpageClipping): Clipping to format.

    Returns:
        str: Formatted string
    """
    document = "\n\n".join(
        [
            f"author:: {clipping.author}",
            f"source:: {clipping.source}",
            f"clipped:: {clipping.clipped_date}",
            f"published:: {clipping.published_date}",
            f"tags:: {clipping.tags}",
            f"# {clipping.title}",
            clipping.markdown,
        ]
    )
    # Remove all whitespace characters sandwiched between two new lines
    cleaned = re.sub(r"\n\s+\n", "\n\n", document)
    # Convert all instances of at least one new-line to 2 new-lines
    cleaned = re.sub(r"\n+", "\n\n", cleaned)
    return cleaned


# We want to replace all illegal filename characters in the title with a dash
# before writing to the file
def clean_filename(filename):
    """Replaces all illegal filename characters in the title of a filename
        with a dash, before writing to the file (i.e. `<>:/|?*`)

    Args:
        filename (str): The filename to clean

    Returns:
        str: Cleaned filename.
    """
    blacklist = r"[<>:/\|?*]"
    blacklist = re.compile(blacklist)
    replacement = " - "
    return re.sub(blacklist, replacement, filename)


def archive_web(url):
    """Archives a webpage as a Markdown file under
        /archive/web/

    Args:
        url (str): The URL of the webpage to archive.
    """
    webpage = clip_webpage(url)
    filename = clean_filename(webpage.title)
    path = pathlib.Path(ROOT_DIR, "archive", "web", f"{filename}_{webpage.clipped_date}.md")
    document = format_clipping(clipping=webpage)
    with path.open(mode="wb") as file:
        file.write(document.encode("UTF-8"))
    LOGGER.info(f"Archived webpage at URL {url}")
