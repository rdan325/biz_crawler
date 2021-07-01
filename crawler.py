"""
Crawler classes for going through CoC homepage and business site
"""
import requests
from bs4 import BeautifulSoup


class CocCrawler:
    def __init__(self, coc_url='http://business.andersonville.org/list'):
        self.coc_url = coc_url
        # Main object that stores business site, links, and points of contact
        # {'biz1_url': {
        #     'links': ['biz1_url/path1', 'biz1_url/path2', 'biz1_url/path3'],
        #     'email': ['info@biz.com', 'info2@biz.com'],
        #     'phone': ['1234567', '9000000']
        # }}
        self.biz_info = None

    def crawl_main(self):
        """
        Crawl main page of Chamber of Commerce
        """
        session = requests.get(self.coc_url)
        soup = BeautifulSoup(session.text)
        # TODO get sub pages
        # TODO for loop through pages and call crawl_sub()

    def crawl_sub(self):
        """
        Crawl sub page of Chamber of Commerce site that points to business pages
        """
        # TODO get all links to businesses with specific tag and put in self.biz_info
        # TODO call crawl_biz()

    def crawl_biz(self, biz_url, crawled):
        """
        Recursively crawl business page to get contact info
        """
        # TODO while loop to check if still left to crawl
        # TODO get session for biz site
        # TODO look for all contact links and put in self.biz_info
        # TODO look for all domain links and put in self.biz_info
        # TODO track visited sites
        # TODO sleep
        # TODO recursively crawl
        ...


