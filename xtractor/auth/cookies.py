import pickle

from ..scraper.extractor import Xtractor


class CookieManager:
    def __init__(self, cookies_path: str):
        self.cookies_path = cookies_path

    def save_cookies(self, driver: Xtractor) -> None:
        pickle.dump(driver.driver.get_cookies(), open(self.cookies_path, "wb"))

    def load_cookies(self, driver: Xtractor) -> None:
        cookies = pickle.load(open(self.cookies_path, "rb"))
        for cookie in cookies:
            driver.driver.add_cookie(cookie)
