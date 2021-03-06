"""
Crawler classes for going through CoC homepage and business site
"""
import requests
from bs4 import BeautifulSoup
import time
try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse
import random
import signal
import os
import json

DATA_PATH = os.environ.get('DATA_PATH', '/var/opt')
JSON_FILE = os.environ.get('JSON_FILE', 'biz_sites.json')


def handler(signum, frame):
    print('Signal handler called with signal', signum)
    raise OSError('Site took too long')


class CocCrawler:
    def __init__(self, coc_url='http://business.andersonville.org/list'):
        """
        Records of links stored in self.biz_info
        {'biz1_url': {
            'links': {'biz1_url/path1', 'biz1_url/path2', 'biz1_url/path3'},
            'email': {'info@biz.com', 'info2@biz.com'},
            'phone': {'1234567', '9000000'}
        }}
        :param coc_url: str
        """
        self.coc_url = coc_url
        self.json_path = os.path.join(DATA_PATH, JSON_FILE)
        self.biz_info = {}

        # create file for json data
        open(self.json_path, 'a').close()

    def get_domain_links(self, url):
        """
        Get all links from a page
        :return links: list
        """
        parsed_url = urlparse(url)
        links = self.get_links(url)
        # if link starts with a "/", it is a path and should be considered a domain link
        path_only = [parsed_url.scheme + '://' + parsed_url.netloc + link for link in links if link[0] == '/']
        d_links = [link for link in links if parsed_url.netloc in link]
        d_links += path_only
        return d_links

    def get_links(self, url):
        """
        Get
        :param url: str
        :return links: list
        """
        sleep_time = random.randint(10, 15)
        print('Sleeping %i seconds...' % sleep_time)
        time.sleep(sleep_time)

        print('Getting link {}'.format(url))
        # Set timeout for 30 seconds
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(30)
        try:
            session = requests.get(url)  # TODO handle SSLError, other Exceptions
        except OSError:
            print('30 second Timeout! Skipping page')
            return None
        except Exception as e:
            print('Exception in getting page: {}'.format(str(e)))
            print('Skipping...')
            return None
        signal.alarm(0)
        print('SESSION RESPONSE: {}'.format(session.status_code))
        soup = BeautifulSoup(session.text, features='lxml')
        # get non-null href links
        links = [link.get('href') for link in soup.find_all('a')]
        links = [link for link in links if link]
        return links

    def filter_domain(self, links, parsed_url):
        """
        From a list of links, only get domain links and filter out bad possible links
        :param links: str
        :param domain: str
        :return d_links: str
        """

        # if link starts with a "/", it is a path and should be considered a domain link
        path_only = {parsed_url.scheme + '://' + parsed_url.netloc + link for link in links if link[0] == '/'}
        d_links = {link for link in links if parsed_url.netloc in link}
        d_links.update(path_only)
        link_list = list(d_links)
        blacklist = ['.png', '.jpg', '.jpeg', '.pdf', 'mailto:', 'tel:']

        for d in link_list:
            for bl in blacklist:
                if bl in d:
                    d_links.remove(d)
                    print('Blacklisted: ', d)
                    continue
        return d_links

    def crawl_main(self):
        """
        Crawl main page of Chamber of Commerce
        """
        links = self.get_links(self.coc_url)
        link_set = {link for link in links if 'ql' in link}
        while link_set:
            print('Sleeping')
            time.sleep(10)
            sub_link = link_set.pop()
            print('Getting sub-site from {}'.format(sub_link))
            self.crawl_sub(sub_link)
        print('Found all sub_links')

    def crawl_sub(self, sub_link):
        """
        Crawl sub page of Chamber of Commerce site that points to business pages
        """
        links = self.get_links(sub_link)
        sb_links = {link for link in links if 'member' in link}
        while sb_links:
            sleep_time = random.randint(10, 15)
            print('Sleeping %i seconds...' % sleep_time)
            time.sleep(sleep_time)
            b_link = sb_links.pop()
            print('Getting sub biz link from {}'.format(b_link))
            r_biz = requests.get(b_link)
            biz_soup = BeautifulSoup(r_biz.text, features='lxml')
            for l in biz_soup.find_all('a'):
                if l.get_text() == 'Visit Website':
                    biz_link = l.get('href')
                    print('Found biz_link {}'.format(biz_link))
                    # save to object and also to file
                    self.biz_info[biz_link] = {'links': set(), 'email': set(), 'phone': set()}
                    with open(self.json_path, 'w') as file:
                        json.dump(self.biz_info, file)
                    break

    def crawl_biz(self, biz_url, limit=20):
        """
        crawl single business page to get all contact info
        """
        to_crawl = {biz_url}
        crawled = set()
        counter = 0
        # check if difference of crawled and sites to crawl is nothing
        print('Crawling business site ', biz_url)
        while to_crawl - crawled and counter < limit:
            biz_link = to_crawl.pop()
            links = self.get_links(biz_link)
            print('Links from page {}'.format(links))
            if links:
                parsed_url = urlparse(biz_url)
                d_links = self.filter_domain(links, parsed_url)
                print('Found domain links: {}'.format(d_links))
                to_crawl.update(d_links)
                emails = {link for link in links if 'mailto:' in link}
                print('Found emails: {}'.format(emails))
                phones = {link for link in links if 'tel:' in link}
                print('Found phone numbers: {}'.format(phones))

                self.biz_info[biz_url]['email'].update(emails)
                self.biz_info[biz_url]['phone'].update(phones)
                self.biz_info[biz_url]['links'].update(d_links)
            else:
                print('No links found')

            crawled.add(biz_link)
            print('Finished crawling url %i' % counter)
            counter += 1

    def run_all(self):
        self.crawl_main()
        for biz_link in self.biz_info.keys():
            self.crawl_biz(biz_link)


if __name__ == '__main__':
    crawler = CocCrawler()
    crawler.run_all()
