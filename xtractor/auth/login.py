import os
import random

from ..scraper.extractor import Xtractor
from ..models import Credentials
from .cookies import CookieManager
from .profile import ProfileManager
from ..utils.logger import logger


def get_random_account() -> Credentials | None:
    with open("accounts.txt", "r", encoding="utf-8") as f:
        accounts = f.readlines()

    try:
        random_index = random.randint(0, len(accounts) - 1)
    except IndexError:
        logger.exception("No accounts provided in accounts.txt")
        return None

    random_account = accounts[random_index].split(":")
    return Credentials(
        email=random_account[0], username=random_account[1], password=random_account[2]
    )


def login_to_x(scraper: Xtractor) -> None:
    random_account = get_random_account()
    if not random_account:
        logger.exception(
            "No accounts found in accounts.txt. Be sure to load this file in the root directory with valid account credentials."
        )
        return

    cookies_path = os.path.join(
        os.path.dirname(__file__), "cookies", f"{random_account.username}.pkl"
    )
    cookies_manager = CookieManager(cookies_path=cookies_path)
    profile_manager = ProfileManager(
        scraper=scraper, credentials=random_account, cookie_manager=cookies_manager
    )
    profile_manager.login()
