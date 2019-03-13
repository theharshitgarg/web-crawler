import datetime
import os
import sys
from contextlib import closing

import requests
import validators
from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import ConnectionError, RequestException

try:
    from urllib.parse import urlparse, urljoin
except ImportError:
    from urlparse import urlparse, urljoin


class FileWriter():
    """FileWriter writes data to file."""

    def __init__(self, fname):
        self.name = fname
        try:
            os.mkdir("Data")
        except Exception as e:
            log_error(e)

    def write_links(self, links):
        """
        Writes links in a separated by newline by encoding in utf-8.
        """
        with open(os.path.join("Data", self.name), 'a') as file:
            for link in links:
                file.write(link.encode("utf-8") + "\n")


def get_base_url(url):
    """
    Returns the domain along with the scheme, if present.
    """
    path = urlparse(url)
    return path.geturl().replace(path.path, '')


def get_url_content(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


def validate_url(url):
    """Returns True if a url is valid else False"""
    return validators.url(url)


def get_soup_object(url):
    content = get_url_content(url)
    soup = BeautifulSoup(content, 'html.parser')

    return soup


def get_all_hyperlinks_soup(soup_obj):
    anchor_tags = soup_obj.select("a")

    hyper_links = []
    for key, link in enumerate(anchor_tags):
        path = get_valid_path(link["href"])
        if path:
            hyper_links.append(path)

    return hyper_links


def extract_images(soup_obj):
    EXTENSIONS = ['.jpg', '.gif', '.png']
    image_tags = soup_obj.select("img")

    images = []
    for key, img in enumerate(image_tags):
        images.append(get_valid_image_path(img['src']))

    return images


def get_difference_urls(old, new):
    return list(set(new).difference(set(old)))


def construct_url(url, path):
    if validators.url(path):
        return path

    path = urlparse(path)
    return get_base_url(url) + path.path
