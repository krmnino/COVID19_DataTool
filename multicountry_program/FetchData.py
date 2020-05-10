import os
import requests
from datetime import date


def get_ISO_codes(raw_data_path, iso_path):
    input_data = open(raw_data_path)
    iso_codes = open(iso_path)
    for i, line in enumerate(input_data):
        if(i == 0):
            continue
        if((line.split(',')[0], line.split(',')[1]) not in iso_codes):
            iso_codes.append((line.split(',')[0], line.split(',')[1]))
    print(iso_codes)

def fetch_data():
    src_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
    try:
        req_data = requests.get(src_url).text
    except:
        print('Could not rearch source repository.')
    req_data = requests.get(src_url).text
    out = open('fetch/data.csv', 'w')
    out.write(req_data)
    out.close()

def backup_prev_data(raw_data_path):
    today = date.today().strftime('_%Y-%m-%d_%H-%M-%S')
    backup_data = open('backups/backup' + today + '.csv', 'w')
    raw_data = open(raw_data_path)
    for line in raw_data:
        backup_data.write(line)
    raw_data.close()
    backup_data.close()
