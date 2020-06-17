import os
import requests
import time
from datetime import date
from DataPoint import DataPoint


def fetch_data_peru():
    src_url = ''
    try:
        req_data = requests.get(src_url).text
    except:
        print('Could not rearch PER data source.')
    req_data = requests.get(src_url).text
    out = open('fetch/raw_PER.csv', 'w')
    out.write(req_data)
    out.close()

def diff_raw_PER_data():
    try:
        open('fetch/raw_PER.csv')
    except:
        print('Could not access USA raw data file.')
    else:
        country_file = open('data/PER_data.csv')
        raw_data_file = open('fetch/raw_PER.csv', 'r')
        last_line = ''
        for line in country_file:
            last_line = line
        last_date = last_line[:last_line.find(',')]
        new_data = []
        for i, line in enumerate(raw_data_file):
            if(i == 0):
                continue
            parsed_line = line.split(',')
            curr_date = str(parsed_line[0][:4]) + '-' + str(parsed_line[0][4:6]) + '-' + str(parsed_line[0][6:])
            print(date)
            if(time.strptime(last_date, '%Y-%m-%d') < time.strptime(curr_date, '%Y-%m-%d')):
                #TODO: find data source....
                break
        return new_data