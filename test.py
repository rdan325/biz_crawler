"""
Testing with https://babeswithblades.org/
Only testing crawl_biz() on a single buziness site
Expecting many emails including artistic@BabesWithBlades.org, business@babeswithblades.org, postal@babeswithblades.org
"""

from crawler import CocCrawler
import sys
import json

test_url = sys.argv[1]

if __name__ == '__main__':
    coc_crawler = CocCrawler()
    print('Testing site ', test_url)
    coc_crawler.biz_info = {test_url: {'links': set(), 'email': set(), 'phone': set()}}
    coc_crawler.crawl_biz(test_url)
    print(coc_crawler.biz_info)
    with open('biz_info.json', 'w') as file:
        file.write(json.dumps(coc_crawler.biz_info))
