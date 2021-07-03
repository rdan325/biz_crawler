"""
Crawler classes for going through CoC homepage and business site
"""
import requests
from bs4 import BeautifulSoup
import time


class CocCrawler:
    def __init__(self, coc_url='http://business.andersonville.org/list'):
        self.coc_url = coc_url
        # Main object that stores business site, links, and points of contact
        # ['biz1_url': {
        #     'links': ['biz1_url/path1', 'biz1_url/path2', 'biz1_url/path3'],
        #     'email': ['info@biz.com', 'info2@biz.com'],
        #     'phone': ['1234567', '9000000']
        # }]
        self.biz_info = []

    def crawl_main(self):
        """
        Crawl main page of Chamber of Commerce
        """
        session = requests.get(self.coc_url)
        soup = BeautifulSoup(session.text)
        links = [link.get('href') for link in soup.find_all('a')]
        link_set = {link for link in links if 'ql' in link}
        while link_set:
            print('Sleeping')
            time.sleep(10)
            sub_link = link_set.pop(0)
            print('Getting sub-site from {}'.format(sub_link))
            self.crawl_sub(sub_link)
        print('Found all sub_links')

    def crawl_sub(self, sub_link):
        """
        Crawl sub page of Chamber of Commerce site that points to business pages
        """
        r_sub = requests.get(self.coc_url)
        soup = BeautifulSoup(r_sub.text)
        links = [link.get('href') for link in soup.find_all('a')]
        sb_links = {link for link in links if 'member' in link}
        while sb_links:
            print('Sleeping')
            time.sleep(10)
            b_link = sb_links.pop(0)
            print('Getting sub biz link from {}'.format(b_link))
            r_biz = requests.get(b_link)
            biz_soup = BeautifulSoup(r_biz.text)
            for l in biz_soup.find_all('a'):
                if l.get_text() == 'Visit Website':
                    biz_link = l.get('href')
                    print('Found biz_link {}'.format(biz_link))
                    self.biz_info.append({biz_link: {'links': [], 'email': [], 'phone': []}})
                    break
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

    def run(self):
        self.crawl_main()
        for biz_link in self.biz_info:
            self.crawl_biz(biz_link)


if __name__ == '__main__':
    crawler = CocCrawler()
    crawler.run()


