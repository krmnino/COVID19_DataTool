import numpy as np
import matplotlib.pyplot as plt

def calc_growth_factor(data1, data2):
    if(data2 == 0):
        return data1
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
    for i, entry in enumerate(parsed_data[0]):
        if(i == 0):
            new_cases = np.append(new_cases, parsed_data[1][i] - 0)
            cases_growth_factor = np.append(cases_growth_factor,  0)
            new_deaths = np.append(new_deaths, parsed_data[2][i] - 0)
            deaths_growth_factor = np.append(deaths_growth_factor, 0)
            new_tests = np.append(new_tests, parsed_data[3][i] - 0)
            tests_growth_factor = np.append(tests_growth_factor, 0)
            days = np.append(days, i)
            continue
        new_cases = np.append(new_cases, parsed_data[1][i] - parsed_data[1][i-1])
        cases_growth_factor = np.append(cases_growth_factor, calc_growth_factor(parsed_data[1][i], parsed_data[1][i-1]))
        new_deaths = np.append(new_deaths, parsed_data[2][i] - parsed_data[2][i-1])
        deaths_growth_factor = np.append(deaths_growth_factor, calc_growth_factor(parsed_data[2][i], parsed_data[2][i-1]))
        new_tests = np.append(new_tests, parsed_data[3][i] - parsed_data[3][i-1])
        tests_growth_factor = np.append(tests_growth_factor, calc_growth_factor(parsed_data[3][i], parsed_data[3][i-1]))
        days = np.append(days, i)
    parsed_data.append(days)
    parsed_data.append(new_cases)
    parsed_data.append(cases_growth_factor)
    parsed_data.append(new_deaths)
    parsed_data.append(deaths_growth_factor)
    parsed_data.append(new_tests)
    parsed_data.append(tests_growth_factor)
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
    print("\u0394Days:\t", parsed_data[4][day2] - parsed_data[4][day1])
    print("\u0394Cases:\t", parsed_data[1][day2] - parsed_data[1][day1])
    print("\u0394Deaths: ", parsed_data[2][day2] - parsed_data[2][day1])
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

def plot_graph(x, y, color, x_label, y_label, chart_title):
    plt.plot(x, y, 'ko', x, y, color)
    plt.title(chart_title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid()
    plt.show()

def plot_graph_log(x, y, color, x_label, y_label, chart_title):
    plt.plot(x, y, 'ko', x, y, color)
    plt.yscale('log')
    plt.title(chart_title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid()
    plt.show()

def print_data(header, data):
    np.set_printoptions(precision=3)
    print('%10s'%(header[0]), end = '')
    print('%9s'%(header[1]), end = '')
    print('%13s'%(header[2]), end = '')
    print('%13s'%(header[3]), end = '')
    print('%13s'%(header[4]), end = '')
    print('%13s'%(header[5]), end = '')
    print('%13s'%(header[6]), end = '')
    print('%13s'%(header[7]), end = '')
    print('%13s'%(header[8]), end = '')
    print('%13s'%(header[9]), end = '')
    print('%13s'%(header[10]))
    for i in range(len(data[0])):
        print('%10s'%(data[0][i]), '%8s'%(data[4][i]), \
            '%12s'%(data[1][i]), '%12s'%(data[5][i]), '%12s'%(round(data[6][i], 5)), \
            '%12s'%(data[2][i]), '%12s'%(data[7][i]) , '%12s'%(round(data[2][i], 5)), \
            '%12s'%(data[3][i]), '%12s'%(data[9][i]) , '%12s'%(round(data[10][i], 5)))