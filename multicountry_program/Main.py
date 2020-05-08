from FetchData import fetch_data
from FetchData import backup_prev_data
from RawParser import compartimentalize
from RawParser import update_all
from RawParser import update_single
from CountryParser import parse_country

#get_ISO_codes('fetch/data.csv', 'fetch/countries_iso_codes.csv')
#fetch_data()
#compartimentalize('fetch/data.csv', 'data')
#update_all('fetch/data.csv', 'data')
#update_single('fetch/data.csv', 'data/COL.csv')
parse_country('data/ABW.csv')
#backup_prev_data('fetch/data.csv')

