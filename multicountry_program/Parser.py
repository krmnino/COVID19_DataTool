def compartimentalize(path):
    input_data = open(path, 'r')
    all_countries = []
    single_country = []
    country_iso = ''
    for i, line in enumerate(input_data):
        if(i == 0):
            continue
        parsed_line = line.split(',')
        if(parsed_line[1] == 'International'):
            continue
        if(parsed_line[0] != country_iso):
            country_iso = parsed_line[0]
            single_country = []
            all_countries.append(single_country)
        else:
            single_country.append(parsed_line)
    all_countries.remove(0)
    print(all_countries)
            