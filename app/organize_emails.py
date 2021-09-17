import pandas as pd
import os
import re

DATA_PATH = os.environ.get('DATA_PATH', 'C:/biz_crawl_data')


def real_url(url):
    site_mapping = [(site, re.sub(r'[^A-Za-z0-9 ]+', '', site)) for site in biz_sites]
    print()
    for sm in site_mapping:
        if url == sm[1]:
            return sm[0]

    # did not find a match
    print('Did not find matching url for ', url)


def process_email(email):
    email = email.replace('mailto:', '')
    email = email.split('?subject')[0]
    if '@' in email:
        return email
    else:
        return ''


if __name__ == '__main__':
    with open(os.path.join(DATA_PATH, 'all_emails.txt'), 'r') as file:
        text = file.read()
    with open(os.path.join(DATA_PATH, 'biz_sites.json'), 'r') as j:
        jtext = j.read()

    data = eval(text)
    data_lists = {k: list(data[k]) for k in data.keys()}
    biz_sites = eval(jtext)
    print(len(biz_sites))
    site_mapping = [(site, re.sub(r'[^A-Za-z0-9 ]+', '', site)) for site in biz_sites]

    data_pre_pandas = []

    for site in data_lists.keys():
        site_data = {'site': site}
        if len(data_lists[site]) > 0:
            email1 = data_lists[site][0]
            site_data.update({'email1': email1})
            if len(data_lists[site]) > 1:
                email2 = data_lists[site][1]
                site_data.update({'email2': email2})
                if len(data_lists[site]) > 2:
                    email3 = data_lists[site][2]
                    site_data.update({'email3': email3})
            data_pre_pandas.append(site_data)

    df = pd.DataFrame(data_pre_pandas)
    df['url'] = df['site'].apply(real_url)
    df['email1'] = df['email1'].astype(str)
    df['email2'] = df['email2'].astype(str)
    df['email3'] = df['email3'].astype(str)
    # df['email1'] = df['email1'].apply(lambda x: x.replace('mailto:', '').replace('?', ''))
    df['email1'] = df['email1'].apply(process_email)
    df['email2'] = df['email2'].apply(process_email)
    df['email3'] = df['email3'].apply(process_email)
    df = df.drop('site', axis=1)
    print(df.head())
    # df.to_csv(os.path.join(DATA_PATH, 'top_emails.csv'), index=False)
