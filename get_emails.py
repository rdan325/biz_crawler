import os

DATA_PATH = os.environ.get('DATA_PATH', '/var/opt')


def all_emails():
    crawled_sites = os.listdir(DATA_PATH)
    emails = {}
    for site in crawled_sites:
        if site != 'biz_sites.json':
            with open(os.path.join(DATA_PATH, site), 'r') as file:
                text = file.read()
            data = eval(text)
            strip_site = site.strip('biz_').strip('.json')
            emails.update({strip_site: data['email']})
    return emails


if __name__ == '__main__':
    emails = all_emails()
    print(emails)
