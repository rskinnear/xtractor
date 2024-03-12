from unittest.mock import patch, mock_open, MagicMock

from xtractor.auth.login import get_random_account, login_to_x
from xtractor.utils.logger import logger


def test_get_random_account():
    mock_data = "email1:username1:password1\nemail2:username2:password2"
    with patch("builtins.open", mock_open(read_data=mock_data)) as mock_file:
        account = get_random_account()
        assert account is not None
        assert account.username.startswith("username")
        assert account.email.startswith("email")


def test_login_to_x_no_accounts():
    mock_data = ""
    with patch(
        get_random_account(), mock_open(read_data=mock_data), return_value=None
    ), patch(logger) as mock_logger:
        scraper = MagicMock()
        login_to_x(scraper)
        mock_logger.exception.assert_called_once_with(
            "No accounts found in accounts.txt. Be sure to load this file in the root directory with valid account credentials."
        )
