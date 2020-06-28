import numpy as np

def parse_file(input_data):
    dates = np.asarray([])
    cases = np.array([])
    deaths = np.array([])
    tests = np.array([])
    recovered = np.array([])
    hospitalized = np.array([])
    for i, line in enumerate(input_data):
        if(i == 0):
            continue
        if(line == '\n'):
            break
        parsed_line = line.split(',')
        try: 
            int(parsed_line[1])
            int(parsed_line[2])
            int(parsed_line[3])
            int(parsed_line[4])
            int(parsed_line[5])
        except:
            print('Data contains invalid data. Cannot convert string to integer.')
            return 0
        dates = np.append(dates, parsed_line[0])
        cases = np.append(cases, int(parsed_line[1]))
        deaths = np.append(deaths, int(parsed_line[2]))
        tests = np.append(tests, int(parsed_line[3]))
        recovered = np.append(recovered, int(parsed_line[4]))
        hospitalized = np.append(hospitalized, int(parsed_line[5]))
    return [dates, cases, deaths, tests, recovered, hospitalized]