import os
import requests
import time
from datetime import date
from DataPoint import DataPoint


def fetch_data_usa():
    src_url = 'https://covidtracking.com/api/v1/us/daily.csv'
    try:
        req_data = requests.get(src_url).text
    except:
        print('Could not rearch USA data source.')
        return
    else:
        req_data = requests.get(src_url).text
        out = open('fetch/raw_USA.csv', 'w')
        out.write(req_data)
        out.close()

def diff_raw_USA_data():
    try:
        open('fetch/raw_USA.csv', 'r')
        open('data/USA_data.csv')
    except:
        print('Could not access USA raw/parsed data file.')
        return
    else:
        country_file = open('data/USA_data.csv')
        raw_data_file = open('fetch/raw_USA.csv', 'r')
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
            if(time.strptime(last_date, '%Y-%m-%d') < time.strptime(curr_date, '%Y-%m-%d')):
                #Index  Data
                #   0   Date
                #   2   Cases
                #   13  Deaths
                #   17  Tests
                #   11    Recovered
                #   6   Hospitalized
                new_data.insert(0, DataPoint(curr_date, int(parsed_line[2]), int(parsed_line[13]),
                int(parsed_line[17]), int(parsed_line[11]), int(parsed_line[6])))
        return new_data

def fetch_data_peru():
    src_url = 'https://raw.githubusercontent.com/krmnino/Peru_COVID19_Stats/master/PER_data.csv'
    try:
        req_data = requests.get(src_url).text
    except:
        print('Could not rearch PER data source.')
        return
    else:
        req_data = requests.get(src_url).text
        out = open('fetch/raw_PER.csv', 'w')
        out.write(req_data)
        out.close()

def diff_raw_PER_data():
    try:
        open('fetch/raw_PER.csv', 'r')
        open('data/PER_data.csv')
    except:
        print('Could not access PER raw/parsed data file.')  
        return      
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
            if(time.strptime(last_date, '%Y-%m-%d') < time.strptime(str(parsed_line[0]), '%Y-%m-%d')):
                #Index  Data
                #   0   Date
                #   1   Cases
                #   2   Deaths
                #   3   Tests   
                #   4   Recovered
                #   5   Hospitalized
                new_data.append(DataPoint(parsed_line[0], int(parsed_line[1]), int(parsed_line[2]),
                int(parsed_line[3]), int(parsed_line[4]),int(parsed_line[5])))
        return new_data