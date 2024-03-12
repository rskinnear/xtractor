import os
import time

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import (
    NoSuchWindowException,
    StaleElementReferenceException,
    NoSuchElementException,
    TimeoutException,
)
from bs4 import BeautifulSoup

from ..base import SeleniumScraper
from ..constants.x_paths import POST_XPATH
from ..constants.urls import (
    X_PROFILE_URL,
    X_SEARCH_QUERY_URL,
    X_SEARCH_QUERY_URL_LATEST,
    X_PROFILE_URL_WITH_REPLIES,
)
from ..models import PostData
from ..utils.logger import logger
from .post import XPost


class Xtractor(SeleniumScraper):
    """
    A specialized web scraper using Selenium to interact with web pages dynamically, specifically designed to extract
    data and manage stale element references effectively.
    """

    LOG_PATH = os.path.join(os.getcwd(), "xtractor", "logs", "geckodriver.log")

    def __init__(self, wait_time: int = 7, headless: bool = False):
        """
        Initialize the Xtractor with specific settings.

        Args:
            wait_time (int): The maximum time to wait for elements to become available.
            headless (bool): Whether to run the browser in headless mode.
        """
        self.wait_time = wait_time
        self.headless = headless
        self._initialize_webdriver()

    def _initialize_webdriver(self):
        """
        Sets up the Selenium WebDriver with specified options and configurations.
        """
        options = webdriver.FirefoxOptions()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")

        service = webdriver.firefox.service.Service(log_path=self.LOG_PATH)
        self.driver = webdriver.Firefox(options=options, service=service)
        self.wait = WebDriverWait(self.driver, self.wait_time)

    def _handle_stale_element(
        self, by: str, value: str, retries: int = 3
    ) -> WebElement | None:
        """
        Attempts to locate an element, handling StaleElementReferenceException by retrying.

        Args:
            by (str): The Selenium By strategy to locate the element.
            value (str): The value to match with the given By strategy.
            retries (int): The number of retries to attempt if the element is stale.

        Returns:
            WebElement | None: The found web element or None if not found after retries.
        """
        for attempt in range(retries):
            try:
                element = self.wait.until(EC.presence_of_element_located((by, value)))
                element.tag_name  # Access an attribute to ensure the element is not stale.
                return element
            except StaleElementReferenceException:
                logger.warning(
                    "Encountered StaleElementReferenceException, retrying (%s/%s)...",
                    attempt + 1,
                    retries,
                )
                time.sleep(1)
            except (NoSuchElementException, TimeoutException):
                logger.warning("Element not found or loading timed out.")
                break
        return None

    def _scroll_to_page_bottom(self):
        """
        Scrolls the browser window to the bottom of the page, checking for new content load.
        """
        try:
            initial_scroll_height = self.driver.execute_script(
                "return document.body.scrollHeight;"
            )
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            self._wait_for_scroll(initial_scroll_height)
        except NoSuchWindowException:
            logger.info("Browser window is no longer available.")
        except Exception as e:
            logger.error("An error occurred while scrolling: %s", e)

    def _wait_for_scroll(self, initial_scroll_height):
        """
        Waits until new content loads after a scroll action, or exits if content does not load within a set time.

        Args:
            initial_scroll_height (int): The height of the page before initiating the scroll.
        """
        start_time = time.time()
        while time.time() - start_time < self.wait_time:
            new_scroll_height = self.driver.execute_script(
                "return document.body.scrollHeight;"
            )
            if new_scroll_height > initial_scroll_height:
                break

    def get(self, url: str):
        """
        Navigates the web driver to a specified URL.

        Args:
            url (str): The URL to navigate to.
        """
        self.driver.get(url)

    def get_element(
        self,
        by: str,
        value: str,
        element: WebElement | None = None,
        handle_stale: bool = True,
    ) -> WebElement | None:
        """
        Retrieves a single web element, with optional handling for stale elements.

        Args:
            by (str): The Selenium By strategy to locate the element.
            value (str): The value to match with the given By strategy.
            element (WebElement | None): The parent element to search within, if applicable.
            handle_stale (bool): Whether to handle stale element references.

        Returns:
            WebElement | None: The found web element, or None if not found.
        """
        if handle_stale:
            return self._handle_stale_element(by, value)
        return (
            self.wait.until(EC.presence_of_element_located((by, value)))
            if element is None
            else element.find_element(by, value)
        )

    def get_elements(
        self, by: str, value: str, element: WebElement | None = None
    ) -> list[WebElement]:
        """
        Retrieves a list of web elements based on the provided search parameters.

        Args:
            by (str): The Selenium By strategy to locate the elements.
            value (str): The value to match with the given By strategy.
            element (WebElement | None): The parent element to search within, if applicable.

        Returns:
            list[WebElement]: The list of found web elements.
        """
        if element is None:
            return self.wait.until(EC.presence_of_all_elements_located((by, value)))
        return element.find_elements(by, value)

    def get_element_text(self, element: WebElement) -> str:
        """
        Extracts and concatenates the text from various child elements and emojis within a parent element.

        Args:
            element (WebElement): The parent element from which to extract text.

        Returns:
            str: The concatenated text content of the element.
        """
        post_content = []
        for child in element.find_elements(By.XPATH, "./*"):
            if child.tag_name in ["span", "a", "div"]:
                post_content.append(child.text)
            elif child.tag_name == "img":
                post_content.append(child.get_attribute("alt"))
        return "".join(post_content)

    def _get_feed_element(self, x_path: str) -> WebElement | None:
        """
        Retrieves the main feed element based on the specified XPATH.

        Args:
            x_path (str): The XPATH to locate the feed element.

        Returns:
            WebElement | None: The feed element if found, otherwise None.
        """
        return self.wait.until(EC.presence_of_element_located((By.XPATH, x_path)))

    def _get_post_elements(self) -> list[WebElement]:
        """
        Retrieves all post elements from the current page.

        Returns:
            list[WebElement]: The list of post elements found on the page.
        """
        return self.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, POST_XPATH))
        )

    def _get_post_element(self) -> WebElement | None:
        """
        Retrieves the first post element from the current page.

        Returns:
            WebElement | None: The first post element if found, otherwise None.
        """
        return self.wait.until(EC.presence_of_element_located((By.XPATH, POST_XPATH)))

    def _scroll_and_scrape(self, limit: int) -> list[PostData]:
        """Scrolls the page and scrapes the post elements until the limit is reached

        Args:
            limit (int): The number of posts to scrape

        Returns:
            list[PostData]: X post data, including impression metrics.
        """
        user_posts = []
        post_ids = set()

        while len(user_posts) < limit:
            self._scroll_to_page_bottom()
            post_elements = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, POST_XPATH))
            )

            for index, post_element in enumerate(post_elements):
                try:
                    post_html = post_element.get_attribute("outerHTML")
                except StaleElementReferenceException:
                    # Attempt to re-acquire the stale element
                    post_elements = self.wait.until(
                        EC.presence_of_all_elements_located((By.XPATH, POST_XPATH))
                    )
                    post_element = post_elements[
                        index
                    ]  # Re-assign the post_element using index
                    post_html = post_element.get_attribute(
                        "outerHTML"
                    )  # Retry attribute fetch

                post_soup = BeautifulSoup(post_html, "html.parser")
                x_post = XPost(soup=post_soup)

                if x_post.id not in post_ids:
                    post_ids.add(x_post.id)
                    user_posts.append(x_post.get_attributes())
                    if len(user_posts) >= limit:
                        break

        return user_posts

    def get_post(self, url: str, reply: bool = False) -> PostData | None:
        """Returns a PostData object from an X post based on the specified url and post ID. A post ID should be specified when retrieving a post that is a reply.

        Args:
            url (str): The url of the X post
            post_id (str | None, optional): _description_. Defaults to None.

        Returns:
            PostData | None: X post data, including impression metrics.
        """
        logger.info("Scraping post: %s", url)

        self.get(url=url)
        if not reply:
            post_element = self.get_element(By.XPATH, POST_XPATH)
            post_html = post_element.get_attribute("outerHTML")
            post_soup = BeautifulSoup(post_html, "html.parser")
            post_data = XPost(soup=post_soup).get_attributes()
            return post_data
        else:
            post_elements = self.get_elements(By.XPATH, POST_XPATH)
            for element in post_elements:
                post_html = element.get_attribute("outerHTML")
                post_soup = BeautifulSoup(post_html, "html.parser")
                post_data = XPost(soup=post_soup).get_attributes()
                print(f"Post id: {post_data.url}: Looking for Id: {url}")
                if post_data.url == url:
                    return post_data
            return None

    def get_posts(self, query: str, limit: int, latest: bool = False) -> list[PostData]:
        """Scrapes posts given a search query

        Args:
            query (str): Search query
            limit (int): Number of posts to scrape
            latest (bool, optional): Scrape the latest posts containing the search query. When false, the top posts are scraped. Defaults to False.

        Returns:
            list[PostData]: X post data, including impression metrics.
        """
        logger.info("Scraping posts with the search query: %s", query)
        query_url = (
            X_SEARCH_QUERY_URL.format(query=query)
            if not latest
            else X_SEARCH_QUERY_URL_LATEST.format(query=query)
        )
        self.get(url=query_url)
        return self._scroll_and_scrape(limit)

    def get_user_posts(
        self, username: str, limit: int, with_replies: bool = False
    ) -> list[PostData]:
        """Fetches all users posts up to a limit

        Args:
            username (str): The X user whose feed is scraped
            limit (int): Number of posts (including replies) to scrape
            with_replies (bool, optional): Scrape the user's replies as well

        Returns:
            list[PostData]:  X post data, including impression metrics.
        """
        logger.info("Scraping posts from the user: %s", username)
        if with_replies:
            x_profile_url = X_PROFILE_URL_WITH_REPLIES.format(username=username)
        else:
            x_profile_url = X_PROFILE_URL.format(username=username)
        self.get(url=x_profile_url)
        return self._scroll_and_scrape(limit)

    def quit(self):
        self.driver.quit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):  # type: ignore
        self.driver.quit()
