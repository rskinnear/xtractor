from abc import ABC, abstractmethod
from datetime import datetime

from selenium.webdriver.remote.webelement import WebElement


class Profile(ABC):
    @property
    @abstractmethod
    def name(self) -> str | None:
        pass

    @property
    @abstractmethod
    def username(self) -> str | None:
        pass

    @property
    @abstractmethod
    def bio(self) -> str | None:
        pass

    @property
    @abstractmethod
    def url(self) -> str | None:
        pass


class Post(ABC):
    @property
    @abstractmethod
    def text(self) -> str | None:
        pass

    @property
    @abstractmethod
    def url(self) -> str | None:
        pass

    @property
    @abstractmethod
    def date(self) -> datetime | None:
        pass


class WebDriverInterface(ABC):
    @abstractmethod
    def get(self, url: str) -> None:
        pass

    @abstractmethod
    def get_element(self, by: str, value: str) -> WebElement:
        pass

    @abstractmethod
    def get_elements(self, by: str, value: str) -> list[WebElement]:
        pass

    @abstractmethod
    def get_element_text(self, element: WebElement) -> str:
        pass

    @abstractmethod
    def quit(self) -> None:
        pass


class SeleniumScraper(ABC):
    """Abstract base webscraper class designed to be used by Selenium."""

    @abstractmethod
    def get(self, url: str) -> None: ...

    @abstractmethod
    def get_element(self, by: str, value: str) -> WebElement: ...

    @abstractmethod
    def get_elements(self, by: str, value: str) -> list[WebElement]: ...

    @abstractmethod
    def get_element_text(self, element: WebElement) -> str: ...

    @abstractmethod
    def quit(self) -> None: ...
