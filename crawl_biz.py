"""
Crawl biz sites from a json file
"""

from crawler import CocCrawler
import os
import re

DATA_PATH = 'C:/biz_crawl_data'
JSON_FILE = os.environ.get('JSON_FILE', 'biz_sites.json')

def list_to_dict(lst):
    d = {l: {'links': set(), 'email': set(), 'phone': set()} for l in lst}
    return d

if __name__ == '__main__':
    json_path = os.path.join(DATA_PATH, JSON_FILE)
    print('Path to links: ', json_path)
    with open(json_path, 'r') as file:
        data_string = file.read()
    data = eval(data_string)  # read string as list
    biz_data = list_to_dict(data)
    coc_crawler = CocCrawler()
    coc_crawler.biz_info = biz_data
    print('All links: {}'.format(coc_crawler.biz_info.keys()))

    for url in coc_crawler.biz_info.keys():
        print('Testing site ', url)
        coc_crawler.crawl_biz(url)

        # Write data for single url
        print(coc_crawler.biz_info[url])
        url_strip = re.sub(r'[^A-Za-z0-9 ]+', '', url)
        biz_path = os.path.join(DATA_PATH, 'biz_{}.json'.format(url_strip))
        with open(biz_path, 'w') as file:
            file.write(json.dumps(str(coc_crawler.biz_info[url])))
