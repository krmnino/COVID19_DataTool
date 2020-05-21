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
    out = open('fetch/data.csv', 'w')
    out.write(req_data)
    out.close()