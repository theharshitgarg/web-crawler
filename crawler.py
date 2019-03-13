import datetime
import sys
from contextlib import closing

import requests
import validators
from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import ConnectionError, RequestException

from data import Data
from utils import is_good_response, log_error

try:
    from urllib.parse import urlparse, urljoin
except ImportError:
    from urlparse import urlparse, urljoin


class Crawler:
    """
    This class extracts the content and 
    stores the data in appropriate data structure.
    """

    def __init__(self, url, depth=2):
        self.url = url
        self.depth = depth
        self.response = None
        self.soup_obj = None
        self.data = Data()

    def get_base_url(self):
        """
        Returns the domain along with the scheme, if present.
        """
        path = urlparse(self.url)
        return path.geturl().replace(path.path, '')

    def get_response_content(self):
        """Returns html content of a web page. Empty string on no response."""
        return self.response.content if self.response else ''

    def set_soup_obj(self, resp_content):
        """Sets soup object representation property of the web page"""
        if self.get_response_content:
            self.soup_obj = BeautifulSoup(resp_content, 'html.parser')

    def get_url_content(self):
        """
        Attempts to get the content at `url` by making an HTTP GET request.
        If the content-type of response is some kind of HTML/XML, return the
        text content, otherwise return None.
        """
        try:
            with closing(get(self.url, stream=True)) as resp:
                if is_good_response(resp):
                    self.response = resp
                    self.set_soup_obj(self.get_response_content())

                    return self.get_response_content()
                else:
                    return None

        except RequestException as e:
            log_error(
                'Error during requests to {0} : {1}'.format(
                    self.url, str(e)))
            return None

    def get_valid_path(self, url):
        """Returns valid url."""
        REJECTED_ONES = ['#', '/', '']
        parsed_url = urlparse(url)
        path = parsed_url.path

        if not parsed_url.hostname:
            url = urljoin(self.get_base_url(), url)
            parsed_url = urlparse(url)

        return None if path in REJECTED_ONES else url

    def get_valid_image_path(self, path):
        """Returns valid url for images."""
        parsed_url = urlparse(path)
        if parsed_url.hostname:
            return path

        return urljoin(self.get_base_url(), path)

    def get_hyperlinks(self):
        """Returns all the hyperlinks. Checks for its validity also."""
        hyper_links = []
        try:
            anchor_tags = self.soup_obj.select("a")
            for key, link in enumerate(anchor_tags):
                path = self.get_valid_path(link.get("href"))
                if path:
                    hyper_links.append(path)
        except AttributeError as e:
            log_error(e)

        return hyper_links

    def get_images(self):
        """Returns all the images links. Checks for its validity also."""
        EXTENSIONS = ['.jpg', '.gif', '.png']
        images = []
        try:
            image_tags = self.soup_obj.select("img")
            for key, img in enumerate(image_tags):
                images.append(self.get_valid_image_path(img['src']))
        except AttributeError as e:
            log_error(e)

        return images

    def construct_url(self, path):
        """Returns valid complete url with hostname. Checks for its correctness also."""
        if validators.url(path):
            return path

        path = urlparse(path)
        return urljoin(self.get_base_url(), path.path)

    def crawl(self):
        """Performs the actual crawling. Should result in update of the fields."""
        self.get_url_content()
