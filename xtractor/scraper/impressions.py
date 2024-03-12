from bs4 import BeautifulSoup, Tag

from ..constants.maps import IMPRESSION_HTML_TO_NAME
from ..constants.css_selectors import METRICS_CSS_SELECTOR, VIEWS_CSS_SELECTOR
from .utils import convert_string_to_int


class ImpressionFinder:
    """
    A utility class designed to extract impression data such as likes, shares, comments, and views from a social media post.

    Attributes:
        soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML content of the post.
    """

    def __init__(self, soup: BeautifulSoup):
        """
        Initializes the ImpressionFinder with the BeautifulSoup object of a post.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML content of the post.
        """
        self.soup = soup

    def _get_element(self, css_selector: str) -> Tag | None:
        """
        Retrieves a single element based on the provided CSS selector.

        Args:
            css_selector (str): The CSS selector to locate the desired element.

        Returns:
            Tag | None: The BeautifulSoup Tag object found using the selector or None if no element is found.
        """
        return self.soup.select_one(css_selector)

    def _get_metric(self, metric: str) -> str:
        """
        Extracts the text content of a specified metric element within the post.

        Args:
            metric (str): The name of the metric to extract from the post.

        Returns:
            str: The extracted metric value as text or "0" if the metric element is not found or empty.
        """
        element = self._get_element(METRICS_CSS_SELECTOR.format(metric=metric.lower()))
        return (
            element.text.split()[0].strip()
            if element and element.text.strip() != ""
            else "0"
        )

    def get_metric_value(self, metric_html: str) -> int:
        """
        Converts a metric value extracted from HTML to an integer.

        Args:
            metric_html (str): The metric identifier used within the HTML content.

        Returns:
            int: The numeric value of the metric.
        """
        metric_value = self._get_metric(metric_html)
        return convert_string_to_int(metric_value)

    def get_views(self) -> int:
        """
        Extracts and returns the number of views for a post.

        Returns:
            int: The number of views for the post or 0 if the views data is not available.
        """
        views_element = self._get_element(VIEWS_CSS_SELECTOR)
        return convert_string_to_int(views_element.text) if views_element else 0

    def get_impressions(self) -> dict[str, int]:
        """
        Compiles and returns a dictionary of various impression metrics for the post.

        Returns:
            dict[str, int]: A dictionary where keys are metric names (e.g., 'likes', 'shares') and values are their respective counts.
        """
        metrics = {}
        for html_value in IMPRESSION_HTML_TO_NAME:
            metric_value = self.get_metric_value(metric_html=html_value)
            metric_name = IMPRESSION_HTML_TO_NAME.get(html_value)
            if metric_name:
                metrics[metric_name] = metric_value

        # Special case handling for 'views' which may need separate processing
        if metrics.get("views", 0) == 0:
            metrics["views"] = self.get_views()

        return metrics
