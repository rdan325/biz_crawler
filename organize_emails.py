import pandas as pd
import os

DATA_PATH = os.environ.get('DATA_PATH', 'C:/biz_crawl_data')

if __name__ == '__main__':
    with open(os.path.join(DATA_PATH, 'all_emails.txt'), 'r') as file:
        text = file.read()

    data = eval(text)
    data_lists = {k: list(data[k]) for k in data.keys()}

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
    print(df.head())
    df.to_csv(os.path.join(DATA_PATH, 'top_emails.csv'), index=False)
