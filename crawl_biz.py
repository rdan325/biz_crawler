"""
Crawl biz sites from a json file
"""

from crawler import CocCrawler
import os
import re
import json

DATA_PATH = os.environ.get('DATA_PATH', '/var/opt')
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
    # Compare with what has already been crawled
    crawled_sites = os.listdir(DATA_PATH)
    crawled_sites = [site.strip('biz_').strip('.json') for site in crawled_sites]

    coc_crawler = CocCrawler()
    coc_crawler.biz_info = biz_data

    for url in coc_crawler.biz_info.keys():
        url_strip = re.sub(r'[^A-Za-z0-9 ]+', '', url)
        if url_strip in crawled_sites:
            print('Already crawled ', url, 'skipping...')
        else:
            print('Testing site ', url)
            coc_crawler.crawl_biz(url)

            # Write data for single url
            print(coc_crawler.biz_info[url])
            biz_path = os.path.join(DATA_PATH, 'biz_{}.json'.format(url_strip))
            with open(biz_path, 'w') as file:
                file.write(json.dumps(str(coc_crawler.biz_info[url])))
