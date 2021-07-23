import os

DATA_PATH = os.environ.get('DATA_PATH', '/var/opt')


def all_emails():
    crawled_sites = os.listdir(DATA_PATH)
    crawled_sites = [site.strip('biz_').strip('.json') for site in crawled_sites]
    emails = {}
    for site in crawled_sites:
        if site != 'sites':
            with open(site, 'r') as file:
                text = file.read()
            data = eval(text)
            emails.update({site: data['email']})
    return emails


if __name__ == '__main__':
    emails = all_emails()
    print(emails)
