from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from ..base import Profile
from ..constants.x_paths import (
    FEED_XPATH,
    FOLLOWERS_XPATH,
    BIO_XPATH,
    JOIN_DATE_XPATH,
    PROFESSION_XPATH,
    LOCATION_XPATH,
    NAME_XPATH,
    FOLLOWING_XPATH,
    SUBSCRIPTIONS_XPATH,
)
from ..constants.urls import X_BASE_URL
from .utils import convert_string_to_int

from .extractor import Xtractor
from ..models import UserData


class XUser(Profile):
    """
    Represents a user profile on the X platform, providing attributes and methods
    to access various details of the user's profile.

    Attributes:
        scraper (Xtractor): An instance of the Xtractor used for web scraping.
        x_username (str | None): The X username of the profile.
        profile_element (WebElement | None): The web element representing the user's profile.
    """

    def __init__(
        self,
        scraper: Xtractor,
        x_username: str | None = None,
        profile_element: WebElement | None = None,
    ):
        """
        Initializes the XUser instance with a scraper object and optionally a username or profile element.

        Args:
            scraper (Xtractor): The Xtractor instance used for scraping.
            x_username (str | None): The username of the profile to be scraped.
            profile_element (WebElement | None): The WebElement corresponding to the profile.

        Raises:
            ValueError: If neither a username nor a profile element is provided.
        """
        if not x_username and not profile_element:
            raise ValueError(
                "Either an X username or profile element must be provided."
            )

        self.scraper = scraper
        self.x_username = x_username
        if self.x_username and not profile_element:
            self.scraper.get(f"{X_BASE_URL}/{self.x_username}")

        self.profile_element = (
            profile_element if profile_element else self._get_profile_element()
        )

        self._name: str | None = None
        self._username: str | None = None

    def _get_profile_element(self) -> WebElement | None:
        """
        Retrieves the main profile element from the page.

        Returns:
            WebElement | None: The main profile element if found, otherwise None.
        """
        try:
            return self.scraper.get_element(by=By.XPATH, value=FEED_XPATH)
        except NoSuchElementException:
            return None

    def _get_profile_property(self, by: str, value: str) -> str | None:
        """
        Retrieves a specific property from the profile element.

        Args:
            by (str): The locator strategy to use.
            value (str): The locator value.

        Returns:
            str | None: The text content of the property if found, otherwise None.
        """
        try:
            element = self.profile_element.find_element(by=by, value=value)  # type: ignore
            return self.scraper.get_element_text(element=element) if element else None
        except (TimeoutException, NoSuchElementException):
            return None

    @property
    def followers(self) -> int | None:
        """
        Retrieves the number of followers for the user.

        Returns:
            int | None: The number of followers if available, otherwise None.
        """
        followers_text = self._get_profile_property(
            by=By.XPATH, value=FOLLOWERS_XPATH.format(username=self.username)
        )
        return (
            convert_string_to_int(followers_text.replace("Followers", ""))
            if followers_text
            else None
        )

    @property
    def following(self) -> int | None:
        """
        Retrieves the number of profiles the user is following.

        Returns:
            int | None: The number of profiles the user is following if available, otherwise None.
        """
        following_text = self._get_profile_property(
            by=By.XPATH, value=FOLLOWING_XPATH.format(username=self.username)
        )
        return (
            convert_string_to_int(following_text.replace("Following", ""))
            if following_text
            else None
        )

    @property
    def subscriptions(self) -> int | None:
        """
        Retrieves the number of subscriptions for the user.

        Returns:
            int | None: The number of subscriptions if available, otherwise None.
        """
        subscription_text = self._get_profile_property(
            by=By.XPATH, value=SUBSCRIPTIONS_XPATH.format(username=self.username)
        )
        return (
            convert_string_to_int(subscription_text.replace("Subscriptions", ""))
            if subscription_text
            else None
        )

    @property
    def bio(self) -> str | None:
        """
        Retrieves the bio/description of the user.

        Returns:
            str | None: The bio of the user if available, otherwise None.
        """
        return self._get_profile_property(by=By.XPATH, value=BIO_XPATH)

    @property
    def name(self) -> str | None:
        """
        Retrieves the name of the user, fetching it if not already available.

        Returns:
            str | None: The name of the user if available, otherwise None.
        """
        if self._name is None:
            self._fetch_name_and_username()
        return self._name

    @property
    def username(self) -> str | None:
        """
        Retrieves the username of the user, fetching it if not already available.

        Returns:
            str | None: The username of the user if available, otherwise None.
        """
        if self._username is None:
            self._fetch_name_and_username()
        return self._username

    def _fetch_name_and_username(self) -> None:
        """
        Fetches and splits the name and username from the profile.

        This method is called internally to populate the _name and _username attributes.
        """
        name_username = self._get_profile_property(by=By.XPATH, value=NAME_XPATH)
        if name_username:
            self._name, self._username = name_username.splitlines()
            self._username = self._username.replace("@", "")

    @property
    def join_date(self) -> str | None:
        """
        Retrieves the join date of the user.

        Returns:
            str | None: The join date of the user if available, otherwise None.
        """
        date_string = self._get_profile_property(
            by=By.XPATH, value=JOIN_DATE_XPATH
        ).replace("Joined ", "")
        return datetime.strptime(date_string, "%B %Y")

    @property
    def profession(self) -> str | None:
        """
        Retrieves the profession/category of the user.

        Returns:
            str | None: The profession of the user if available, otherwise None.
        """
        return self._get_profile_property(by=By.XPATH, value=PROFESSION_XPATH)

    @property
    def location(self) -> str | None:
        """
        Retrieves the location of the user.

        Returns:
            str | None: The location of the user if available, otherwise None.
        """
        return self._get_profile_property(by=By.XPATH, value=LOCATION_XPATH)

    @property
    def url(self) -> str:
        """
        Constructs the URL to the user's profile.

        Returns:
            str: The URL to the user's X profile.
        """
        return f"{X_BASE_URL}/{self.username}/"

    def get_data(self) -> UserData:
        """Returns a UserData object for scraped data

        Returns:
            UserData: UserData model containing given user's profile data
        """
        return UserData(
            name=self.name,
            username=self.username,
            url=self.url,
            followers=self.followers,
            following=self.following,
            subscriptions=self.subscriptions,
            join_date=self.join_date,
            profession=self.profession,
            location=self.location,
        )

    def __str__(self):
        """
        Represents the XUser instance as a string, providing a summary of the user's profile information.

        Returns:
            str: A string representation of the user's profile information.
        """
        return (
            f"Name: {self.name}\n"
            f"Username: {self.username}\n"
            f"URL: {self.url}\n"
            f"Followers: {self.followers}\n"
            f"Following: {self.following}\n"
            f"Subscriptions: {self.subscriptions}\n"
            f"Bio: {self.bio}\n"
            f"Join date: {self.join_date}\n"
            f"Profession: {self.profession}\n"
            f"Location: {self.location}"
        )
