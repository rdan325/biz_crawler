"""
Crawl biz sites from a json file
"""

from crawler import CocCrawler
import json
import os
import re

DATA_PATH = '../biz_crawl_data'
JSON_FILE = os.environ['JSON_FILE']

if __name__ == '__main__':
    json_path = os.path.join(DATA_PATH, JSON_FILE)
    with open(JSON_FILE, 'r') as jfile:
        data = json.load(jfile)
    coc_crawler = CocCrawler()
    coc_crawler.biz_info = data
    print('All links: {}'.format(coc_crawler.biz_info.keys()))

    for url in coc_crawler.biz_info.keys():
        print('Testing site ', url)
        coc_crawler.crawl_biz(url)

        # Write data for single url
        print(coc_crawler.biz_info[url])
        url_strip = re.sub(r'[^A-Za-z0-9 ]+', '', url)
        with open('biz_{}.json'.format(url_strip), 'w') as file:
            file.write(json.dumps(str(coc_crawler.biz_info[url])))
