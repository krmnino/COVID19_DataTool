import os

def compartimentalize(raw_data_path, data_path):
    input_data = open(raw_data_path, 'r')
    all_countries = []
    single_country = []
    country_iso = ''
    for i, line in enumerate(input_data):
        if(i == 0):
            continue
        parsed_line = line.split(',')
        if(parsed_line[0] == ''):
            continue
        if(parsed_line[0] != country_iso):
            country_iso = parsed_line[0]
            single_country = []
            all_countries.append(single_country)
        else:
            single_country.append([parsed_line[0], parsed_line[2], parsed_line[3], parsed_line[5], parsed_line[11]])
    input_data.close()
    for country in all_countries:
        country_data = open(data_path + '/' + country[0][0] + '.csv', 'w')
        for line in country:
            country_data.write(line[1] + ',' + line[2] + ',' + line[3] + ',' + line[4] + ',\n')
        country_data.close()
        
def update_all(raw_data_path, data_path):
    input_data = open(raw_data_path, 'r')
    all_countries = []
    single_country = []
    country_iso = ''
    for i, line in enumerate(input_data):
        if(i == 0):
            continue
        parsed_line = line.split(',')
        if(parsed_line[0] == ''):
            continue
        if(parsed_line[0] != country_iso):
            country_iso = parsed_line[0]
            single_country = []
            all_countries.append(single_country)
        else:
            single_country.append([parsed_line[0], parsed_line[2], parsed_line[3], parsed_line[5], parsed_line[11]])
    data_directory_names = os.listdir(data_path)
    new_countries = []
    for i, name in enumerate(data_directory_names):
        if(all_countries[i][0][0] != data_directory_names[i][:data_directory_names[i].find('.')]):
            new_countries.append(all_countries[i])
        else:
            print(data_path + '/' + data_directory_names[i])
            country_src = open(data_path + '/' + data_directory_names[i], 'r+')
            country_data = []
            if(name == 'COL.csv'):
                print('COLOMBIA')
            for j, line in enumerate(country_src):
                if(line.split(',')[0] != '\n'):
                    country_data.append(line.split(','))
            if(len(country_data) < len(all_countries[i])):
                index = len(country_data)
                while(index < len(all_countries[i])):
                    country_data.append(all_countries[i][index])
                    index += 1
            country_src.seek(0)
            country_src.truncate()
            for line in country_data:
                country_src.write(line[0] + ',' + line[1] + ',' + line[2] + ',' + line[3] + ',\n')
            country_src.close()
    if(len(new_countries) != 0):
        for country in new_countries:
            out_new_country = open(country[0][0] + '.csv')
            country_src.seek(0)
            country_src.truncate()
            for line in country:
                out_new_country.write(line[0] + ',' + line[1] + ',' + line[2] + ',' + line[3] + ',\n')
            out_new_country.close()



