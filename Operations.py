import numpy as np
import matplotlib.pyplot as plt

def calc_growth_factor(data1, data2):
    if(data2 == 0):
        return data1
    else:
        return data1 / data2

def compute_data(parsed_data):
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
            continue
        new_cases = np.append(new_cases, parsed_data[1][i] - parsed_data[1][i-1])
        cases_growth_factor = np.append(cases_growth_factor, calc_growth_factor(parsed_data[1][i], parsed_data[1][i-1]))
        new_deaths = np.append(new_deaths, parsed_data[2][i] - parsed_data[2][i-1])
        deaths_growth_factor = np.append(deaths_growth_factor, calc_growth_factor(parsed_data[2][i], parsed_data[2][i-1]))
        new_tests = np.append(new_tests, parsed_data[3][i] - parsed_data[3][i-1])
        tests_growth_factor = np.append(tests_growth_factor, calc_growth_factor(parsed_data[3][i], parsed_data[3][i-1]))
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
    print("\u0394Days:\t\t", parsed_data[0][day2] - parsed_data[0][day1])
    print("\u0394Cases:\t\t", parsed_data[2][day2] - parsed_data[2][day1])
    print("\u0394Growth Ratio:\t", parsed_data[3][day2] - parsed_data[3][day1])

def projection(next_days, days_passed, cases, growth_factor):
    total_cases = cases[len(cases)-1]
    counter = 0
    index = len(growth_factor) - 1
    counter = 0
    avg_growth_factor = 0.0
    while(counter < days_passed):
        avg_growth_factor += growth_factor[index - counter]
        counter += 1
    avg_growth_factor /= days_passed
    print('Avg Growth Factor (past', days_passed ,'days):', avg_growth_factor)
    counter = 0
    while(counter < next_days):
        total_cases = total_cases * avg_growth_factor
        counter += 1
    print("Prediction # of cases in the next", next_days, "days:", total_cases)

def plot_graph(x, y, color, x_label, y_label):
    plt.plot(x, y, 'ko', x, y, color)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid()
    plt.show()

def plot_graph_log(x, y, color, x_label, y_label):
    plt.plot(x, y, 'ko', x, y, color)
    plt.yscale('log')
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
    data[5] = np.round(data[5], decimals = 5)
    data[7] = np.round(data[7], decimals = 5)
    data[9] = np.round(data[9], decimals = 5)
    for i in range(len(data[0])):
        print(data[0][i], f'{i:8} {data[1][i]:12} {data[4][i]:12} {data[5][i]:12} {data[2][i]:12} {data[6][i]:12} {data[7][i]:12} {data[3][i]:12} {data[8][i]:12} {data[3][i]:12}')