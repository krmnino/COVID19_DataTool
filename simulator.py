from math import e
import matplotlib
import os
import platform
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
        if(num != ''):
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

def difference(parsed_data, day1, day2):
    for col in parsed_data:
        print(col)

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

def command_line():
    parsed_data = 0
    instructions = ['load', 'show', 'delete', ]
    while(True):
        input_cmd = input('>> ')
        parsed_input = input_cmd.split()
        if(parsed_input[0] == 'exit'):
            print('Exiting...')
            break
        if(parsed_input[0] == 'help'):
            print('usage manual:')
            print('load [FILE]                                      load data set in memory')
            print('show                                             displays loaded data set')
            print('show_all [next_days] [avg_previous_days]         displays loaded data set and projection')
            print('delete                                           erase data set loaded in memory')
            print('diff                                             shows difference of values between 2 days')
            print('projection [next_days] [avg_previous_days]       show projection for the next x days using avg growth factor from y previous days')
            print('plot_cases                                       display cases graph')
            print('plot_cases_log                                   display cases in a logarithmic graph')
            print('plot_growth                                      display growth rate graph')
            print('plot_growth [from_day][to_day]                   display growth rate graph from a range of days')
            print('clear                                            clears the console')
            continue

        if(parsed_input[0] == "clear"):
            if(platform.system() == "Windows"):
                os.system("cls")
                continue
            elif(platform.system() == "Linux"):
                os.system("clear")
                continue
            continue

        if(parsed_input[0] == 'load'):
            if(len(parsed_input) != 2):
                print("usage: load [FILE PATH]")
                continue
            else:
                try:
                    input_data = open(str(parsed_input[1]))
                    parsed_data = parse_file(input_data)
                    input_data.close()
                    print("Loaded data from", parsed_input[1])
                except:
                    print(parsed_input[1], "is not accesible")
                continue

        if(parsed_input[0] == 'delete'):
            parsed_data = 0
            continue

        if(parsed_data == 0):
            print('data has not been loaded into memory')
            continue

        if(parsed_input[0] == 'show'):
            print_data(parsed_data[0], parsed_data[1], parsed_data[2], parsed_data[3])
            continue

        if(parsed_input[0] == 'show_all'):
            if(len(parsed_input) != 3):
                print("usage: show_all [next_days] [avg_previous_days]")
                continue
            else:
                print_data(parsed_data[0], parsed_data[1], parsed_data[2], parsed_data[3])
                projection(int(parsed_input[1]), int(parsed_input[2]), parsed_data[2], parsed_data[3])
                continue

        if(parsed_input[0] == 'diff'):
            if(len(parsed_input) != 3):
                print("usage: diff [from_day] [to_day]")
                continue
            else:
                difference(parsed_data, int(parsed_input[1]), int(parsed_input[2]))
                continue

        if(parsed_input[0] == 'projection'):
            if(len(parsed_input) != 3):
                print("usage: projection [next_days] [avg_previous_days]")
                continue
            else:
                projection(int(parsed_input[1]), int(parsed_input[2]), parsed_data[2], parsed_data[3])
                continue

        if(parsed_input[0] == 'plot_cases'):
            plot_graph(parsed_data[0], parsed_data[2], 'b', "Days", "Cases")
            continue

        if(parsed_input[0] == 'plot_cases_log'):
            plot_graph_log(parsed_data[0], parsed_data[2], 'b', "Days", "Cases")
            continue

        if(parsed_input[0] == 'plot_growth'):
            if(len(parsed_input) == 1):
                plot_graph(parsed_data[0], parsed_data[3], 'k', "Days", "Growth Ratio (%)")  
                continue
            elif(len(parsed_input) != 3):
                print(len(parsed_input))
                print("usage: plot_growth")
                print("       plot_growth [from day] [to_day]")
                continue
            elif(parsed_input[0] == "plot_growth" and int(parsed_input[2]) > parsed_data[0][len(parsed_data[0]) - 1]):
                print("range of days is invalid, starting day must be less than ending day")
                continue
            elif(parsed_input[0] == "plot_growth" and int(parsed_input[1]) > int(parsed_input[2])):
                print("range of days is invalid, starting day must be less than ending day")
                continue
            else:
                plot_graph(parsed_data[0][int(parsed_input[1]):int(parsed_input[2]) + 1], \
                    parsed_data[3][int(parsed_input[1]):int(parsed_input[2]) + 1], 'k', "Days", "Growth Ratio (%)")  
                continue
        print('Invalid input. For instructions type "help".')
        
    
#################################################################################

np.set_printoptions(suppress=True)
command_line()