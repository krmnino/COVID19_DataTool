from math import e
import matplotlib
import sys
import matplotlib.pyplot as plt
import numpy as np
import csv

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
    while (day_counter < 60):
        days = np.append(days, day_counter)
        log_fn = population / (1 + ((population / current_cases) - 1) * e ** (-0.38 * day_counter))
        print(log_fn)
        logistic = np.append(logistic, log_fn)
        day_counter += 1
    return (days, logistic)

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

def plot_graph(x, y, color):
    plt.plot(x, y, 'ko', x, y, color)
    plt.show()

def print_data(days, dates, cases, growth_factor):
    print("Day # \t Date \t\t Cases \t\t Growth Ratio")
    for i in range(0, len(days)):
        print(days[i], '\t', dates[i], '\t', cases[i], '\t\t', growth_factor[i])

def command_line():
    parsed_data = 0
    while(True):
        input_cmd = input(">> ")
        parsed_input = input_cmd.split()
        if(parsed_input[0] == 'exit'):
            print("Exiting...")
            break
        if(parsed_input[0] == 'help'):
            print('usage manual:')
            print('load [FILE]                                      load data set in memory')
            print('show                                             displays loaded data set')
            print('delete                                           erase data set loaded in memory')
            print('projection [next_days] [avg_previous_days]       show projection for the next x days using avg growth factor from y previous days')
            print('plot_cases                                       display cases graph')
            print('plot_growth                                      display cases graph')
            continue

        if(parsed_input[0] == "load" and len(parsed_input) != 2):
            print("usage: load [FILE PATH]")
            continue
        elif(parsed_input[0] == "load" and len(parsed_input) == 2):
            try:
                input_data = open(str(parsed_input[1]))
                parsed_data = parse_file(input_data)
                input_data.close()
                print("Loaded data from", parsed_input[1])
            except:
                print(parsed_input[1], "is not accesible")
            continue
                
        if(parsed_input[0] == "show" and parsed_data == 0):
            print("data has not been loaded into memory")
            continue
        elif(parsed_input[0] == "show" and parsed_data != 0):
            print_data(parsed_data[0], parsed_data[1], parsed_data[2], parsed_data[3])
            continue

        if(parsed_input[0] == "show_all" and parsed_data == 0):
            print("data has not been loaded into memory")
            continue
        elif(parsed_input[0] == "show_all" and len(parsed_input) != 3):
            print("usage: show_all [next_days] [avg_previous_days]")
            continue
        elif(parsed_input[0] == "show_all" and parsed_data != 0):
            print_data(parsed_data[0], parsed_data[1], parsed_data[2], parsed_data[3])
            projection(int(parsed_input[1]), int(parsed_input[2]), parsed_data[2], parsed_data[3])
            continue
        
        if(parsed_input[0] == "delete"):
            parsed_data = 0
            continue

        if(parsed_input[0] == "projection" and parsed_data == 0):
            print("data has not been loaded into memory")
            continue
        elif(parsed_input[0] == "projection" and len(parsed_input) != 3):
            print("usage: projection [next_days] [avg_previous_days]")
            continue
        elif(parsed_input[0] == "projection" and len(parsed_input) == 3 and parsed_data != 0):
            projection(int(parsed_input[1]), int(parsed_input[2]), parsed_data[2], parsed_data[3])
            continue

        if(parsed_input[0] == "plot_cases" and parsed_data == 0):
            print("data has not been loaded into memory")
            continue
        elif(parsed_input[0] == "plot_cases" and parsed_data != 0):
            plot_graph(parsed_data[0], parsed_data[2], 'b')
            continue

        if(parsed_input[0] == "plot_growth" and parsed_data == 0):
            print("data has not been loaded into memory")
            continue
        elif(parsed_input[0] == "plot_growth" and parsed_data != 0):
            plot_graph(parsed_data[0], parsed_data[3], 'k')  
            continue
        if(parsed_input[0] == "clear"):
            continue
        else:
            print('Invalid input. For instructions type "help".')
        
    
#################################################################################

np.set_printoptions(suppress=True)
command_line()