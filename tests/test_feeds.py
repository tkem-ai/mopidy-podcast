from io import StringIO
from pathlib import Path

import pytest
import uritools

from mopidy_podcast import feeds


@pytest.mark.parametrize(
    "filename,expected",
    [("directory.xml", feeds.OpmlFeed), ("rssfeed.xml", feeds.RssFeed)],
)
def test_parse(testpath: Path, filename: str, expected):
    path = testpath / filename
    feed = feeds.parse(path)
    assert isinstance(feed, expected)
    assert feed.uri == uritools.uricompose("podcast+file", "", str(path))


class StringSource(StringIO):
    def geturl(self):
        return "http://example.com/feed.xml"


def test_parse_unknown_feed():
    with pytest.raises(TypeError) as excinfo:
        feeds.parse(StringSource("<html/>"))
    assert str(excinfo.value) == (
        "Not a recognized podcast feed: http://example.com/feed.xml"
    )


def test_parse_rss_without_channel():
    with pytest.raises(ValueError, match=r"feed\.xml.*<channel>"):
        feeds.parse(StringSource('<rss version="2.0"/>'))
