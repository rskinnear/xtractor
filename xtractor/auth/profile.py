import os
import time

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from ..scraper.extractor import Xtractor
from ..models import Credentials
from ..constants.urls import X_LOGIN_URL
from ..utils.logger import logger
from .cookies import CookieManager


class ProfileManager:
    def __init__(
        self,
        scraper: Xtractor,
        credentials: Credentials | None = None,
        cookie_manager: CookieManager | None = None,
    ):
        if not credentials and not cookie_manager:
            raise ValueError("Either Credentials or CookieManager must be provided.")

        self.scraper = scraper
        self.credentials = credentials
        self.cookie_manager = cookie_manager

    def logout(self):
        pass

    def login(self):
        if self.cookie_manager:
            if os.path.exists(self.cookie_manager.cookies_path):
                logger.info("Logging in with cookies")
                self._login_with_cookies()

            elif self.credentials:
                logger.info("Logging in with credentials")
                self._login_with_credentials()
                self.cookie_manager.save_cookies(driver=self.scraper)
        else:
            self._login_with_credentials()

    def _login_with_cookies(self) -> None:
        if self.cookie_manager:
            self.scraper.get(X_LOGIN_URL)
            self.cookie_manager.load_cookies(driver=self.scraper)

    def _login_with_credentials(self):
        if self.credentials:
            self.scraper.get(X_LOGIN_URL)
            # fill in username
            self._wait_and_type(By.NAME, "text", self.credentials.username)
            # fill in password
            self._wait_and_type(By.NAME, "password", self.credentials.password)
            try:
                self._wait_and_type(By.NAME, "text", self.credentials.email)
            except (NoSuchElementException, TimeoutException):
                logger.info("Didn't request email verification.")

    def _wait_and_type(self, by: str, value: str, text: str) -> None:
        print(f"Sending: {text}")
        element: WebElement = WebDriverWait(self.scraper.driver, 7).until(
            EC.presence_of_element_located((by, value))
        )
        time.sleep(1)
        element.send_keys(text)
        element.send_keys(Keys.RETURN)
