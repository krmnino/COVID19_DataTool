import numpy as np
import matplotlib.pyplot as plt

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

def print_data(days, dates, cases, growth_factor):
    print("Day # \t Date \t\t Cases \t\t Growth Ratio")
    for i in range(0, len(days)):
        print(days[i], '\t', dates[i], '\t', cases[i], '\t\t', growth_factor[i])
