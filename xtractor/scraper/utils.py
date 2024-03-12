from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from bs4 import BeautifulSoup


def convert_string_to_int(string: str) -> int:
    """Converts string representations of numbers that include K and M to integers."""
    string = string.replace(",", "")  # Remove commas from the string
    try:
        if "K" in string:
            return int(float(string.replace("K", "")) * 1e3)
        elif "M" in string:
            return int(float(string.replace("M", "")) * 1e6)
        else:
            return int(float(string))
    except ValueError:
        return 0


def get_soup_element_text(soup: BeautifulSoup) -> str:
    """Iterates through span, a, div and img html tags to scrape text and emojis and joins the elements together."""
    post_content: list[str] = []

    for child in soup.find_all(["span", "a", "div", "img"]):
        if child.name in ["span", "a", "div"]:
            text = child.text
            if text:
                post_content.append(text.strip())
        elif child.name == "img":
            emoji = child.get("alt")  # Using get to access attributes in BeautifulSoup
            if emoji:
                post_content.append(emoji)

    return " ".join(post_content)


def get_x_element_text(post_element: WebElement) -> str:
    """Iterates through span and image html tags to scrape text and emojis and joins the elements together."""
    post_content: list[str] = []

    for child in post_element.find_elements(By.XPATH, "./*"):  # type: ignore
        if child.tag_name in ["span", "a", "div"]:
            text = child.text
            if text:
                post_content.append(text)
        elif child.tag_name == "img":
            emoji = child.get_attribute("alt")  # type: ignore
            if emoji:
                post_content.append(emoji)

    return "".join(post_content)
