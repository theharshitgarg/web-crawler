from crawler import Crawler
from cache import Cache
from data import Data
import sys
from utils import validate_url, FileWriter, log_error, get_base_url
import datetime
import validators


try:
    from urllib.parse import urlparse, urljoin
except ImportError:
    from urlparse import urlparse, urljoin


def is_valid_nagvigation_link(link, base_ref=None):
    """
    This function checks if the link is navigable or not.
    A link to resource like pdf, jpg should be avoided.
    Also an external link to the site is avoided here.
    """
    RESTRICTED = ['.jpg', '.pdf', '.gif', '.png']
    parsed_link = urlparse(link)

    if parsed_link.hostname and parsed_link.hostname != urlparse(
            base_ref).hostname:
        return False

    return validators.url(link) and not bool(
        [i for i in RESTRICTED if i in parsed_link.path])


def main(url, depth):
    cache = Cache() # TODO: Implement cache logic
    data = Data()
    date_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    links_file = FileWriter(date_time + '-links.txt')
    images_file = FileWriter(date_time + '-images.txt')

    crawler = Crawler(url)
    crawler.crawl()
    cache.append_links(crawler.get_hyperlinks())
    data.append_images(crawler.get_images())
    data.append_links(0, crawler.get_hyperlinks())
    links_file.write_links(crawler.get_hyperlinks())
    images_file.write_links(crawler.get_images())

    base = 1
    while base < depth:
        images = []
        hyperlinks = []

        for key, link in enumerate(data.hyperlinks[base - 1]):
            if is_valid_nagvigation_link(link, get_base_url(url)):
                crawler = Crawler(link)
                crawler.crawl()
                images = crawler.get_images()
                hyperlinks = crawler.get_hyperlinks()

                images = data.append_images(images)
                hyperlinks = data.append_links(base, images)
                links_file.write_links(hyperlinks)
                images_file.write_links(images)
            else:
                log_error("Invalid Link")

        base = base + 1


if __name__ == '__main__':
    print "stating scraping...."
    if len(sys.argv) < 2:
        print "Incorrect Usage"
        print "Please provide url and "

    url = sys.argv[1]
    if not validate_url(url):
        print "Incorrect url. Please give valid url"
        exit()

    try:
        depth = int(sys.argv[2])
    except BaseException:
        depth = 2

    main(url, depth)

    print "Scraping Done..... :-]). Look the files in data folder."
