"""
Testing with https://babeswithblades.org/
Only testing crawl_biz() on a single buziness site
Expecting many emails including artistic@BabesWithBlades.org, business@babeswithblades.org, postal@babeswithblades.org
"""

from crawler import CocCrawler
import json

homepage = 'http://business.andersonville.org/list'

if __name__ == '__main__':
    coc_crawler = CocCrawler()
    print('Getting all biz_sites')
    coc_crawler.crawl_main()
    print(coc_crawler.biz_info)
    # upload them all to a json file at the end
    with open('biz_info.json', 'w') as file:
        file.write(json.dumps(coc_crawler.biz_info))  # TODO write as list instead of json
