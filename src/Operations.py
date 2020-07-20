import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import date
from math import e

def calc_rate(data1, data2):
    if(data2 == 0):
        return data1
    else:
        if(data1 < data2):
            return (data2 / data1) * -1
        else:
            return data1 / data2

def calc_mort_rate(data1, data2):
    if(data2 == 0):
        return 0
    else:
        return data1 / data2

def compute_data(parsed_data):
    days = np.array([])
    new_cases = np.array([])
    cases_growth_factor = np.array([])
    new_deaths = np.array([])
    deaths_growth_factor = np.array([])
    new_tests = np.array([])
    tests_growth_factor = np.array([])
    new_recovered = np.array([])
    recovered_growth_factor = np.array([])
    new_hospitalized = np.array([])
    hospitalized_growth_factor = np.array([])
    mortality_rate = np.array([])
    active_cases = np.array([])
    for i, entry in enumerate(parsed_data[0]):
        if(i == 0):
            new_cases = np.append(new_cases, parsed_data[1][i] - 0)
            cases_growth_factor = np.append(cases_growth_factor,  0)
            new_deaths = np.append(new_deaths, parsed_data[2][i] - 0)
            deaths_growth_factor = np.append(deaths_growth_factor, 0)
            new_tests = np.append(new_tests, parsed_data[3][i] - 0)
            tests_growth_factor = np.append(tests_growth_factor, 0)
            new_recovered = np.append(new_recovered, parsed_data[4][i] - 0)
            recovered_growth_factor = np.append(recovered_growth_factor, 0)
            new_hospitalized = np.append(new_hospitalized, parsed_data[5][i] - 0)
            hospitalized_growth_factor = np.append(hospitalized_growth_factor, 0)
            mortality_rate = np.append(mortality_rate, calc_mort_rate(parsed_data[2][i], parsed_data[1][i]))
            active_cases = np.append(active_cases, (parsed_data[1][i] - parsed_data[4][i] - parsed_data[2][i]))
            days = np.append(days, i)
            continue
        new_cases = np.append(new_cases, parsed_data[1][i] - parsed_data[1][i-1])
        cases_growth_factor = np.append(cases_growth_factor, calc_rate(parsed_data[1][i], parsed_data[1][i-1]))
        new_deaths = np.append(new_deaths, parsed_data[2][i] - parsed_data[2][i-1])
        deaths_growth_factor = np.append(deaths_growth_factor, calc_rate(parsed_data[2][i], parsed_data[2][i-1]))
        new_tests = np.append(new_tests, parsed_data[3][i] - parsed_data[3][i-1])
        tests_growth_factor = np.append(tests_growth_factor, calc_rate(parsed_data[3][i], parsed_data[3][i-1]))
        new_recovered = np.append(new_recovered, parsed_data[4][i] - parsed_data[4][i-1])
        recovered_growth_factor = np.append(recovered_growth_factor, calc_rate(parsed_data[4][i], parsed_data[4][i-1]))
        new_hospitalized = np.append(new_hospitalized, parsed_data[5][i] - parsed_data[5][i-1])
        hospitalized_growth_factor = np.append(hospitalized_growth_factor, calc_rate(parsed_data[5][i], parsed_data[5][i-1]))
        mortality_rate = np.append(mortality_rate, calc_mort_rate(parsed_data[2][i], parsed_data[1][i]))
        active_cases = np.append(active_cases, (parsed_data[1][i] - parsed_data[4][i] - parsed_data[2][i]))
        days = np.append(days, i)
    parsed_data.append(days)
    parsed_data.append(new_cases)
    parsed_data.append(cases_growth_factor)
    parsed_data.append(new_deaths)
    parsed_data.append(deaths_growth_factor)
    parsed_data.append(new_recovered)
    parsed_data.append(recovered_growth_factor)
    parsed_data.append(new_hospitalized)
    parsed_data.append(hospitalized_growth_factor)
    parsed_data.append(new_tests)
    parsed_data.append(tests_growth_factor)
    parsed_data.append(mortality_rate)
    parsed_data.append(active_cases)
    return parsed_data

def logistic_fn(population):
    day_counter = 1
    days = np.array([])
    logistic = np.array([])
    current_cases = 1
    while (day_counter < 60):
        days = np.append(days, day_counter)
        log_fn = population / (1 + ((population / current_cases) - 1) * e ** (-0.38 * day_counter))
        print(log_fn)
        logistic = np.append(logistic, log_fn)
        day_counter += 1
    return (days, logistic)

def difference(parsed_data, day1, day2):
    print("Data difference between:", parsed_data[0][day1], 'and', parsed_data[0][day2])
    print("\u0394Days:\t", parsed_data[6][day2] - parsed_data[6][day1])
    print("\u0394Cases:\t", parsed_data[1][day2] - parsed_data[1][day1])
    print("\u0394Deaths: ", parsed_data[2][day2] - parsed_data[2][day1])
    print("\u0394Recov.: ", parsed_data[4][day2] - parsed_data[4][day1])
    print("\u0394Hospi.: ", parsed_data[5][day2] - parsed_data[5][day1])
    print("\u0394Tests:\t", parsed_data[3][day2] - parsed_data[3][day1])

def projection(next_days, days_passed, parsed_data):
    total_cases = float(parsed_data[1][len(parsed_data[1])-1])
    total_deaths = float(parsed_data[2][len(parsed_data[2])-1])
    counter = 0
    avg_cases_gf = 0.0
    avg_deaths_gf = 0.0
    while(counter < days_passed):
        avg_cases_gf += parsed_data[6][len(parsed_data[6]) - 1 - counter]
        avg_deaths_gf += parsed_data[8][len(parsed_data[8]) - 1 - counter]
        counter += 1
    avg_cases_gf /= days_passed
    avg_deaths_gf /= days_passed
    print('Avg Cases Growth Factor (past', days_passed ,'days):', round(avg_cases_gf, 5))
    print('Avg Deaths Growth Factor (past', days_passed ,'days):', round(avg_deaths_gf, 5))
    counter = 0
    while(counter < next_days):
        total_cases = total_cases * avg_cases_gf
        total_deaths = total_deaths * avg_deaths_gf
        counter += 1
    print("Prediction # of cases in the next", next_days, "days:", round(total_cases))
    print("Prediction # of deaths in the next", next_days, "days:", round(total_deaths))

def plot_graph(x, y, color, x_label, y_label, chart_title, file_name='', save=False, log_view=False):
    plt.figure(figsize=(14,10))
    plt.ticklabel_format(style='plain')
    plt.title(chart_title, fontdict={'fontsize' : 25})
    if(log_view):
        plt.yscale('log')
    plt.plot(x, y, 'ko', x, y, color)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid()
    plt.show()
    if(save):
        plt.plotplt.savefig('../res/graphs/' + file_name + '.png')
    else:
        plt.show()

def plot_graph_all(parsed_data, chart_title, from_day, to_day, file_name='', save=False):
    plt.figure(figsize=(14,10))
    plt.ticklabel_format(style='plain')
    plt.title(chart_title, fontdict={'fontsize' : 25})
    plt.plot(parsed_data[4][from_day:to_day], parsed_data[1][from_day:to_day], 'ko')
    plt.plot(parsed_data[4][from_day:to_day], parsed_data[1][from_day:to_day], 'b', label = "Cases")
    plt.plot(parsed_data[4][from_day:to_day], parsed_data[2][from_day:to_day], 'ko')
    plt.plot(parsed_data[4][from_day:to_day], parsed_data[2][from_day:to_day], 'r', label = "Deaths")
    plt.plot(parsed_data[4][from_day:to_day], parsed_data[4][from_day:to_day], 'ko')
    plt.plot(parsed_data[4][from_day:to_day], parsed_data[4][from_day:to_day], 'g', label = "Recovered")
    plt.plot(parsed_data[4][from_day:to_day], parsed_data[18][from_day:to_day], 'ko')
    plt.plot(parsed_data[4][from_day:to_day], parsed_data[18][from_day:to_day], 'k', label = "Active Cases")
    plt.legend(loc="upper left")
    plt.xlabel("Days")
    plt.grid()
    if(save):
        plt.plotplt.savefig('../res/graphs/' + file_name + '.png')
    else:
        plt.show()

def print_cases(header, data):
    np.set_printoptions(precision=3)
    print('%10s'%(header[0]), end = '')
    print('%9s'%(header[1]), end = '')
    print('%13s'%(header[2]), end = '')
    print('%13s'%(header[3]), end = '')
    print('%13s'%(header[4]), end = '')
    print('%13s'%(header[18]))
    for i in range(len(data[0])):
        print('%10s'%(data[0][i]), '%8s'%(data[6][i]), '%12s'%(data[1][i]), '%12s'%(data[7][i]), '%12s'%(str(data[8][i])[:8]), '%12s'%(data[18][i]))

def print_deaths(header, data):
    np.set_printoptions(precision=3)
    print('%10s'%(header[0]), end = '')
    print('%9s'%(header[1]), end = '')
    print('%13s'%(header[5]), end = '')
    print('%13s'%(header[6]), end = '')
    print('%13s'%(header[7]), end = '')
    print('%13s'%(header[5]))
    for i in range(len(data[0])):
        print('%10s'%(data[0][i]), '%8s'%(data[6][i]), '%12s'%(data[2][i]), '%12s'%(data[9][i]), '%12s'%(data[10][i]), '%12s'%(data[17][i]))
    
def print_tests(header, data):
    np.set_printoptions(precision=3)
    print('%10s'%(header[0]), end = '')
    print('%9s'%(header[1]), end = '')
    print('%13s'%(header[14]), end = '')
    print('%13s'%(header[15]), end = '')
    print('%13s'%(header[16]))
    for i in range(len(data[0])):
        print('%10s'%(data[0][i]), '%8s'%(data[6][i]), '%12s'%(data[3][i]), '%12s'%(data[15][i]), '%12s'%(data[16][i]))

def print_recovered(header, data):
    np.set_printoptions(precision=3)
    print('%10s'%(header[0]), end = '')
    print('%9s'%(header[1]), end = '')
    print('%13s'%(header[8]), end = '')
    print('%13s'%(header[9]), end = '')
    print('%13s'%(header[10]))
    for i in range(len(data[0])):
        print('%10s'%(data[0][i]), '%8s'%(data[6][i]), '%12s'%(data[4][i]), '%12s'%(data[11][i]), '%12s'%(data[12][i]))

def print_hospitalized(header, data):
    np.set_printoptions(precision=3)
    print('%10s'%(header[0]), end = '')
    print('%9s'%(header[1]), end = '')
    print('%13s'%(header[11]), end = '')
    print('%13s'%(header[12]), end = '')
    print('%13s'%(header[13]))
    for i in range(len(data[0])):
        print('%10s'%(data[0][i]), '%8s'%(data[6][i]), '%12s'%(data[5][i]), '%12s'%(data[13][i]), '%12s'%(data[14][i]))

def print_diff_data(header, data):
    np.set_printoptions(precision=3)
    '''
    Header index    Data Index      Title
    0               0               Date
    1               6               Day
    2               1               Cases
    3               7               New Cases
    18              18              Active Cases
    5               2               Deaths
    6               9               New Deaths
    17              17              Mortality Rate
    8               4               Recovered
    9               11              New Recovered
    11              5               Hospitalized
    12              13              New Hospitalized
    14              3               Tests
    15              15              New Tests
    '''
    print('%10s'%(header[0]), end = '')
    print('%9s'%(header[1]), end = '')
    print('%13s'%(header[2]), end = '')
    print('%13s'%(header[3]), end = '')
    print('%13s'%(header[18]), end = '')
    print('%13s'%(header[5]), end = '')
    print('%13s'%(header[6]), end = '')
    print('%13s'%(header[8]), end = '')
    print('%13s'%(header[9]), end = '')
    print('%13s'%(header[11]), end = '')
    print('%13s'%(header[12]), end = '')
    print('%13s'%(header[14]), end = '')
    print('%13s'%(header[15]))
    for i in range(len(data[0])):
        print('%10s'%(data[0][i]), '%8s'%(data[6][i]), 
            '%12s'%(data[1][i]), '%12s'%(data[7][i]), '%12s'%(data[18][i]), 
            '%12s'%(data[2][i]), '%12s'%(data[9][i]), 
            '%12s'%(data[4][i]), '%12s'%(data[11][i]),
            '%12s'%(data[5][i]), '%12s'%(data[13][i]),
            '%12s'%(data[3][i]), '%12s'%(data[15][i]))
            
def print_gf_data(header, data):
    np.set_printoptions(precision=3)
    '''
    Header index    Data Index      Title
    0               0               Date
    1               6               Day
    2               1               Cases
    4               8               % Cases
    5               2               Deaths
    7               10              % Deaths
    8               4               Recovered
    10              12              % Recovered
    11              5               Hospitalized
    13              14              % Hospitalized
    14              3               Tests
    16              16              % Tests
    '''
    print('%10s'%(header[0]), end = '')
    print('%9s'%(header[1]), end = '')
    print('%13s'%(header[2]), end = '')
    print('%13s'%(header[4]), end = '')
    print('%13s'%(header[5]), end = '')
    print('%13s'%(header[7]), end = '')
    print('%13s'%(header[17]), end = '')
    print('%13s'%(header[8]), end = '')
    print('%13s'%(header[10]), end = '')
    print('%13s'%(header[11]), end = '')
    print('%13s'%(header[13]), end = '')
    print('%13s'%(header[14]), end = '')
    print('%13s'%(header[16]))
    for i in range(len(data[0])):
        print('%10s'%(data[0][i]), '%8s'%(data[6][i]), 
            '%12s'%(data[1][i]), '%12s'%(str(data[8][i])[:8]), 
            '%12s'%(data[2][i]), '%12s'%(str(data[10][i])[:8]), '%12s'%(str(data[17][i])[:5]),
            '%12s'%(data[4][i]), '%12s'%(str(data[12][i])[:8]),
            '%12s'%(data[5][i]), '%12s'%(str(data[14][i])[:8]),
            '%12s'%(data[3][i]), '%12s'%(str(data[16][i])[:8]))

def print_new_data(new_data):
    print('INDEX', '%14s'%('DATE'), '%11s'%('CASES'), '%11s'%('DEATHS'), '%11s'%('TESTS'), '%11s'%('RECOVERED'), '%11s'%('HOSPITAL'))
    for i, entry in enumerate(new_data):
        print('%5s'%(str(i)), end = '')
        entry.show()

def list_to_csv(parsed_data):
    file_name = 'out_data_' + date.today().strftime('%Y-%m-%d') + '.csv'
    try:
        open(os.path.dirname(os.path.abspath(__file__)) + '/../export/' + file_name, 'w')
    except:
        print('Could not export processed data.')
        return 
    out_file = open(os.path.dirname(os.path.abspath(__file__)) + '/../export/' + file_name, 'w')
    out_file.write('Date,Day,Cases,NewCases,D%Cases,ActiveCases,Deaths,NewDeaths,D%Deaths,MortalityRate,Tests,\
        NewTests,D%Tests,Recovered,NewRecovered,D%Recovered,Hospitalized,NewHospitalized,D%Hospitalized\n')
    for i in range(0, len(parsed_data[0])-1):
        line = str(parsed_data[0][i]) + "," + str(parsed_data[6][i]) + "," + \
            str(parsed_data[1][i]) + "," + str(parsed_data[7][i]) + "," + str(parsed_data[8][i]) + "," + str(parsed_data[18][i]) + "," + \
            str(parsed_data[2][i]) + "," + str(parsed_data[9][i]) + "," + str(parsed_data[10][i]) + "," + str(parsed_data[17][i]) + "," + \
            str(parsed_data[3][i]) + "," + str(parsed_data[15][i]) + "," + str(parsed_data[16][i]) + "," + \
            str(parsed_data[4][i]) + "," + str(parsed_data[11][i]) + "," + str(parsed_data[12][i]) + "," + \
            str(parsed_data[5][i]) + "," + str(parsed_data[13][i]) + "," + str(parsed_data[14][i]) + "\n" 
        out_file.write(line)
    out_file.close()
    print('Data successfully exported to export/' + file_name)

def update_country_data(file_name, max_index, new_data):
    try:
        open(os.path.dirname(os.path.abspath(__file__)) + '/../data/' + file_name, 'a')
    except:
        print('Could not access', file_name)
        return False
    else:
        with open(os.path.dirname(os.path.abspath(__file__)) + '/../data/' + file_name, 'a') as file:
            for i in range(0, max_index + 1):
                file.writelines(new_data[i].to_csv())
            return True
        file.close()