
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
    growth_factor = np.array([])
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
        if(day_counter > 1 and num != -1):
            growth_factor = np.append(growth_factor, (num / cases[day_counter - 1]))
            print((num / cases[day_counter - 1]))
        day_counter += 1        
    return (days, dates, cases, growth_factor)

def logistic_fn():
    day_counter = 0
    days = np.array([])
    logistic = np.array([])
    while (day_counter < 90):
        days = np.append(days, day_counter)
        day_counter += 1

def projection(next_days, days_passed, cases, growth_factor):
    total_cases = 0
    counter = 0
    while (True):
        if(counter >= len(cases)):
            break
        if(cases[counter] == -1):
            total_cases = cases[counter - 1]
            break
        counter += 1
        pass
    index = len(parsed_data[3]) - 1
    counter = 0
    avg_growth_factor = 0.0
    while(counter < days_passed):
        avg_growth_factor += parsed_data[3][index - counter]
        counter += 1
    avg_growth_factor /= days_passed
    print('GF: ', avg_growth_factor)
    counter = 0
    while(counter < next_days):
        total_cases += total_cases * avg_growth_factor
        counter += 1
    print(total_cases)

def plot_graph(days, cases):
    plt.plot(days, cases, 'bo', days, cases, 'k')
    plt.show()

#################################################################################

np.set_printoptions(suppress=True)
#input_data = open(sys.argv[1])
input_data = open("peru_data.csv")    
parsed_data = parse_file(input_data)
projection(13, 5, parsed_data[2], parsed_data[3])
#plot_graph(parsed_data[0], parsed_data[2])
