"""
Crawler classes for going through CoC homepage and business site
"""


class CocCrawler:
    def __init__(self, coc_url='http://business.andersonville.org/list'):
        self.coc_url = coc_url