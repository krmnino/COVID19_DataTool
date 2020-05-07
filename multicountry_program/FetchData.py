import os
import requests
from datetime import date


def fetch_data():
    src_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
    try:
        req_data = requests.get(src_url).text
    except:
        print('Could not rearch source repository.')
    req_data = requests.get(src_url).text
    out = open('data.csv', 'w')
    out.write(req_data)
    out.close()

def backup_prev_data():
    today = date.today().strftime('_%Y-%m-%d_%H-%M-%S')
    backup_data = open('data/backup' + today + '.csv', 'w')
    raw_data = open('data.csv')
    for line in raw_data:
        backup_data.write(line)
    raw_data.close()
    backup_data.close()

