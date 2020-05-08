from FetchData import fetch_data
from FetchData import backup_prev_data
from Parser import compartimentalize
from Parser import update_all

#get_ISO_codes('data.csv')



#fetch_data()

#compartimentalize('fetch/data.csv', 'data')

update_all('fetch/data.csv', 'data')

#backup_prev_data()

