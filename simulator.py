
import matplotlib
import sys
import matplotlib.pyplot as plt
import numpy as np
import csv
'''
if(len(sys.argv) != 2):
    print("usage: python3 simulator.py [INPUT_DATA.csv]")
    sys.exit(1)
'''
def parse_file(input_data):
    dates = np.asarray([])
    days = np.array([])
    cases = np.array([])
    growth_factor = np.array([0, 1])
    day_counter = 0
    for line in input_data:
        date = line.split(',')[0]
        num = line.split(',')[1][:line.split(',')[1].find('\n')]
        if(num is not ''):
            num = int(num)
        else:
            num = -1
        dates = np.append(dates, date)
        days = np.append(days, day_counter)
        cases = np.append(cases, num)
        if(day_counter > 1):
            growth_factor = np.append(growth_factor, (num / cases[day_counter - 1]))
        day_counter += 1        
    return (days, dates, cases, growth_factor)

def logistic_fn(population):
    day_counter = 1
    days = np.array([])
    logistic = np.array([])
    current_cases = 1
    logistic_f = 1 - ((1.2 * current_cases) / population)
    while (day_counter < 90):
        days = np.append(days, day_counter)
        logistic = np.append(logistic, current_cases)
        current_cases = current_cases * 1.5
        day_counter += 1
    return (days, logistic)

def projection(next_days, days_passed, cases, growth_factor):
    total_cases = cases[len(cases)-1]
    counter = 0
    index = len(parsed_data[3]) - 1
    counter = 0
    avg_growth_factor = 0.0
    while(counter < days_passed):
        avg_growth_factor += parsed_data[3][index - counter]
        counter += 1
    avg_growth_factor /= days_passed
    print('Avg Growth Factor (past', days_passed ,'days):', avg_growth_factor)
    counter = 0
    while(counter < next_days):
        total_cases = total_cases * avg_growth_factor
        counter += 1
    print("Prediction # of cases in the next", next_days, "days:", total_cases)

def plot_graph(x, y):
    plt.plot(x, y, 'bo', x, y, 'k')
    plt.show()

def print_data(days, dates, cases, growth_factor):
    print("Day # \t Date \t Cases \t Growth Ratio")
    for i in range(0, len(days)):
        print(days[i], '\t', dates[i], '\t', cases[i], '\t', growth_factor[i])

#################################################################################

np.set_printoptions(suppress=True)
#input_data = open(sys.argv[1])
input_data = open("peru_data.csv")    
parsed_data = parse_file(input_data)
#print_data(parsed_data[0], parsed_data[1], parsed_data[2], parsed_data[3])
projection(1, 3, parsed_data[2], parsed_data[3])
logistic_data = logistic_fn(32000000)
#plot_graph(parsed_data[0], parsed_data[2])
plot_graph(logistic_data[0],logistic_data[1])