from datetime import datetime, timezone

from bs4 import BeautifulSoup, Tag

from ..utils.logger import logger
from ..base import Post
from ..models import PostData
from ..constants.css_selectors import *
from .utils import get_soup_element_text
from .impressions import ImpressionFinder


class XPost(Post):
    """
    Represents a post on the X platform and provides methods to extract various attributes including text, date, url, etc.

    Attributes:
        soup (BeautifulSoup): The BeautifulSoup object representing the post's HTML content.
        _url (str | None): The URL of the post, if available.
    """

    def __init__(self, soup: BeautifulSoup, url: str | None = None):
        """
        Initializes an XPost instance.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object representing the post's HTML content.
            url (str | None): The URL of the post, if available.
        """
        self.soup = soup
        self._url = url

    def _get(self, tag: str, element: Tag) -> Tag | None:
        """
        Retrieves a specific attribute or content from a Tag element.

        Args:
            tag (str): The tag or attribute name to retrieve.
            element (Tag): The BeautifulSoup Tag element from which to retrieve the attribute.

        Returns:
            Tag | None: The retrieved content or None if not found.
        """
        attribute = element.get(tag)
        return attribute[0] if isinstance(attribute, list) else attribute

    def _get_element(self, attribute_xpath: str) -> Tag | None:
        """
        Selects the first matching element based on the provided XPath Selector.

        Args:
            attribute_xpath (str): The XPath Selector to identify the element.

        Returns:
            Tag | None: The first matching Tag or None if not found.
        """
        try:
            return self.soup.select_one(attribute_xpath)
        except Exception as error:
            logger.error("Error encountered: %s", error)

    def _get_elements(self, attribute_xpath: str) -> list[Tag]:
        """
        Selects all matching elements based on the provided XPath.

        Args:
            attribute_xpath (str): The XPath selector to identify the elements.

        Returns:
            list[Tag]: A list of all matching Tags.
        """
        try:
            return self.soup.select(attribute_xpath)
        except Exception as error:
            logger.error("Error encountered: %s", error)

    @property
    def text(self) -> str | None:
        """
        Extracts and returns the post's text content.

        Returns:
            str | None: The post's text content or None if not found.
        """
        text_element = self._get_element(TEXT_CSS_SELECTOR)
        if text_element is None:
            return None
        return get_soup_element_text(
            soup=BeautifulSoup(text_element.decode_contents(), "html.parser")
        )

    @property
    def url(self) -> str | None:
        """
        Retrieves the URL of the post.

        Returns:
            str | None: The post's URL or None if it cannot be determined.
        """
        if self._url:
            return self._url

    @property
    def date(self) -> datetime | None:
        """
        Extracts and returns the post's publication date.

        Returns:
            datetime | None: The datetime object representing the post's publication date or None if not found.
        """
        date_element = self._get_element(DATE_CSS_SELECTOR)
        if date_element is None:
            return None
        date = self._get(tag="datetime", element=date_element)
        return (
            datetime.fromisoformat(date[:-1]).replace(tzinfo=timezone.utc)
            if date
            else None
        )

    @property
    def author_username(self) -> str | None:
        """
        Retrieves the username of the post's author.

        Returns:
            str | None: The author's username or None if not found.
        """
        username_element = self._get_element(USERNAME_CSS_SELECTOR)
        if not username_element:
            return None
        return (
            username_element.get_text().split("@")[1].split("·")[0]
            if "·" in username_element.get_text()
            else username_element.get_text().split("@")[1]
        )

    @property
    def author_name(self) -> str | None:
        """
        Retrieves the display name of the post's author.

        Returns:
            str | None: The author's display name or None if not found.
        """
        username_element = self._get_element(USERNAME_CSS_SELECTOR)
        if not username_element:
            return None
        return username_element.get_text().split("@")[0]

    @property
    def id(self) -> str | None:
        """
        Retrieves the unique identifier of the post.

        Returns:
            str | None: The post's unique identifier or None if the URL is not available.
        """
        if self.url:
            return self.url.split("/")[-1]

    def get_post_media(self) -> set[str]:
        """
        Extracts media URLs (if any) associated with the post.

        Returns:
            set[str]: A set of media URLs found within the post.
        """
        media_elements = self._get_elements(MEDIA_CSS_SELECTOR)
        return {
            self._get(tag="src", element=element)
            for element in media_elements
            if self._get(tag="src", element=element)
        }

    def is_repost(self) -> bool:
        """
        Determines if the post is a repost.

        Returns:
            bool: True if the post is a repost, False otherwise.
        """
        return bool(self._get_element(REPOST_CSS_SELECTOR))

    def video_in_post(self) -> bool:
        """
        Checks if there is a video within the post.

        Returns:
            bool: True if a video is present, False otherwise.
        """
        return bool(self._get_element(VIDEO_CSS_SELECTOR))

    def show_more_link(self) -> bool:
        """
        Determines if the 'Show more' link is present in the post.

        Returns:
            bool: True if the 'Show more' link is present, False otherwise.
        """
        return bool(self._get_element(SHOW_MORE_CSS_SELECTOR))

    def get_impressions(self) -> dict[str, int]:
        """
        Retrieves various impression counts (like, retweet, etc.) for the post.

        Returns:
            dict[str, int]: A dictionary with impression types as keys and their respective counts as values.
        """
        impression_scraper = ImpressionFinder(soup=self.soup)
        return impression_scraper.get_impressions()

    def get_attributes(self) -> PostData:
        return PostData(
            post_id=self.id,
            text=self.text,
            url=self.url,
            date=self.date,
            author_username=self.author_username,
            author_name=self.author_name,
            is_repost=self.is_repost(),
            video_in_post=self.video_in_post(),
            impressions=self.get_impressions(),
            post_media=self.get_post_media(),
        )

    def __str__(self):
        attributes = [
            f"Text: {self.text}",
            f"URL: {self.url}",
            f"Date: {self.date}",
            f"Author Username: {self.author_username}",
            f"Author Name: {self.author_name}",
            f"ID: {self.id}",
            f"Is Repost: {self.is_repost()}",
            f"Video in Post: {self.video_in_post()}",
            f"Show More Link: {self.show_more_link()}",
        ]

        media_urls = self.get_post_media()
        if media_urls:
            attributes.append(f"Media URLs: {', '.join(media_urls)}")

        impressions = self.get_impressions()
        if impressions:
            attributes.append("Impressions:")
            for key, value in impressions.items():
                attributes.append(f"  {key}: {value}")

        return "\n".join(attributes)
