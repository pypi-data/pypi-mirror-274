import os
import requests
import pandas as pd

# https://markets.newyorkfed.org/static/docs/markets-api.html

def download_records_after(date):

    response = requests.get(f'https://markets.newyorkfed.org/api/rp/reverserepo/propositions/search.json?startDate={date}')

    if response.status_code != 200:
        print(f'status_code: {response.status_code}.')
    else:
        data = response.json()

        df = pd.DataFrame(data['repo']['operations'])

        print(f'Downloaded {len(df)} records.')

        return df

# ----------------------------------------------------------------------
# update_records is deprecated.
# Use load_records instead.
# ----------------------------------------------------------------------
def update_records(start_date):
    
    path = 'rrp.pkl'

    if os.path.isfile(path):

        print(f'Found {path}. Importing.')

        df = pd.read_pickle(path)

        recent_date = df['operationDate'].iloc[1]

        print(f'Second most recent date: {recent_date}.')

        new_records = download_records_after(recent_date)

        existing_records = df[df['operationDate'] < recent_date]

        # new_df = pd.concat([existing_records, new_records], ignore_index=True)

        new_df = pd.concat([new_records, existing_records], ignore_index=True)

        new_df.to_pickle(path)

        return new_df
    
    else:

        print(f'No {path} found. Downloading all records after {start_date}.')

        df = download_records_after(start_date)

        df.to_pickle(path)

        return df
# ----------------------------------------------------------------------
def load_records(start_date, update=False):
    
    path = 'rrp.pkl'

    if os.path.isfile(path):

        print(f'Found {path}. Importing.')

        df = pd.read_pickle(path)

        if update == False:
            return df

        recent_date = df['operationDate'].iloc[1]

        print(f'Second most recent date: {recent_date}.')

        new_records = download_records_after(recent_date)

        existing_records = df[df['operationDate'] < recent_date]

        # new_df = pd.concat([existing_records, new_records], ignore_index=True)

        new_df = pd.concat([new_records, existing_records], ignore_index=True)

        new_df.to_pickle(path)

        return new_df
    
    else:

        print(f'No {path} found. Downloading all records after {start_date}.')

        df = download_records_after(start_date)

        df.to_pickle(path)

        return df

# ----------------------------------------------------------------------

if __name__ == '__main__':
    load_records('1900-01-01', update=True)
