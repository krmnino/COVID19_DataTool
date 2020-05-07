from FetchData import fetch_data
from FetchData import backup_prev_data
from Parser import compartimentalize


def get_ISO_codes(path):
    input_data = open(path)
    iso_codes = []
    for i, line in enumerate(input_data):
        if(i == 0):
            continue
        if((line.split(',')[0], line.split(',')[1]) not in iso_codes):
            iso_codes.append((line.split(',')[0], line.split(',')[1]))
    print(iso_codes)

#get_ISO_codes('data.csv')

compartimentalize('data.csv')

#backup_prev_data()

#fetch_data()