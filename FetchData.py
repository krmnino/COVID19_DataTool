import os
import requests
import time
from datetime import date
from DataPoint import DataPoint


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

def diff_raw_country_data(file_name):
    file_names = os.listdir('data')
    if(not file_name in file_names):
        print(file_name + 'could not be accessed or does not exist.')
        return
    else:
        country_file = open('data/' + file_name)
        raw_data_file = open('fetch/data.csv', 'r')
        last_line = ''
        for line in country_file:
            last_line = line
        last_date = last_line[:last_line.find(',')]
        new_data = []
        for i, line in enumerate(raw_data_file):
            if(i == 0):
                continue
            parsed_line = line.split(',')
            if(file_name[:file_name.find('_')] == parsed_line[0] and time.strptime(last_date, '%Y-%m-%d') < time.strptime(parsed_line[2], '%Y-%m-%d')):
                if(parsed_line[11][:parsed_line[11].find('.')] == ''):
                    new_data.append(DataPoint(parsed_line[0], parsed_line[2], int(parsed_line[3]), int(parsed_line[5]), 0))
                else:
                    new_data.append(DataPoint(parsed_line[0], parsed_line[2], int(parsed_line[3]), int(parsed_line[5]), int(parsed_line[11][:parsed_line[11].find('.')])))
        return new_data