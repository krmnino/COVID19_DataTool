from FileParser import parse_file
from Operations import difference
from Operations import print_data
from Operations import plot_graph
from Operations import projection
from Operations import compute_data
from Operations import plot_graph_log

import os
import platform
import sys
import numpy as np
from datetime import date
import csv


def command_line():
    os.system("mode con cols=150")
    np.set_printoptions(suppress=True)
    header_fields = ['Date', 'Day', 'Cases', 'New Cases', '%\u0394 Cases', 'Deaths', 'New Deaths', '%\u0394 Deaths', 'Tests', 'New Tests', '%\u0394 Tests']
    parsed_data = 0
    instructions = ['load', 'show', 'show_all', 'delete', 'diff', 'projection', 'plot_cases', 'plot_cases_log', 'plot_growth', 'clear', 'exit', 'help', 'csv_format']
    while(True):
        input_cmd = input('>> ')
        parsed_input = input_cmd.split()
        if(len(parsed_input) == 0):
            continue
        if(parsed_input[0] not in instructions):
            print('Invalid command. Type "help" for instructions.')
            continue
        if(parsed_input[0] == 'exit'):
            print('Exiting...')
            break
        if(parsed_input[0] == 'help'):
            print('usage manual:')
            print('load [FILE]                                      Load data set in memory')
            print('show                                             Displays loaded data set')
            print('show_all [next_days] [avg_previous_days]         Displays loaded data set and projection')
            print('delete                                           Erase data set loaded in memory')
            print('diff                                             Shows difference of values between 2 days')
            print('projection [next_days] [avg_previous_days]       Show projection for the next x days using avg growth factor from y previous days')
            print('plot_cases                                       Display cases graph')
            print('plot_cases_log                                   Display cases in a logarithmic graph')
            print('plot_growth                                      Display growth rate graph')
            print('plot_growth [from_day][to_day]                   Display growth rate graph from a range of days')
            print('clear                                            Clears the console')
            print('csv_format                                       Display .csv file format per columns')
            print('help                                             Display program manual')
            print('exit                                             Exit the program')
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
                print("Usage: load [FILE PATH]")
                continue
            else:
                try:
                    input_data = open(str(parsed_input[1]))
                except:
                    print(parsed_input[1], "is not accesible")
                    continue
                input_data = open(str(parsed_input[1]))
                parsed_data = parse_file(input_data)
                input_data.close()
                if(parsed_data != 0):
                    parsed_data = compute_data(parsed_data)
                    print("Loaded and computed data from", parsed_input[1])
                continue

        if(parsed_input[0] == 'delete'):
            parsed_data = 0
            continue

        if(parsed_data == 0):
            print('Data has not been loaded into memory')
            continue

        if(parsed_input[0] == 'show'):
            print_data(header_fields, parsed_data)
            continue

        if(parsed_input[0] == 'show_all'):
            if(len(parsed_input) != 3):
                print("Usage: show_all [next_days] [avg_previous_days]")
                continue
            else:
                print_data(parsed_data[0], parsed_data[1], parsed_data[2], parsed_data[3])
                projection(int(parsed_input[1]), int(parsed_input[2]), parsed_data[2], parsed_data[3])
                continue

        if(parsed_input[0] == 'diff'):
            if(len(parsed_input) != 3):
                print("usage: diff [from_day] [to_day]")
                continue
            elif(not parsed_input[1].isdigit() or not parsed_input[2].isdigit()):
                print("Days must be integers. Ranging 0 -", parsed_data[0][len(parsed_data[0]) - 1])
                continue
            elif(int(parsed_input[1]) > parsed_data[0][len(parsed_data[0]) - 1] or \
                 int(parsed_input[2]) > parsed_data[0][len(parsed_data[0]) - 1]):
                print("Range of days is invalid, days must fall between the range: 0 -", parsed_data[0][len(parsed_data[0]) - 1])
                continue
            elif(int(parsed_input[1]) > int(parsed_input[2])):
                print("Range of days is invalid, starting day must be less than ending day")
                continue
            else:
                difference(parsed_data, int(parsed_input[1]), int(parsed_input[2]))
                continue

        if(parsed_input[0] == 'projection'):
            if(len(parsed_input) != 3):
                print("Usage: projection [next_days] [avg_previous_days]")
                continue
            else:
                projection(int(parsed_input[1]), int(parsed_input[2]), parsed_data[2], parsed_data[3])
                continue

        if(parsed_input[0] == 'csv_format'):
            print('Column 1: Date')
            print('Column 2: Cases')
            print('Column 2: Cases')

        if(parsed_input[0] == 'plot_cases'):
            plot_graph(parsed_data[0], parsed_data[2], 'b', "Days", "Cases", "Cases as of: " + parsed_data[0][len(parsed_data[0])-1])
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
                print("Usage: plot_growth")
                print("       plot_growth [from day] [to_day]")
                continue
            elif(not parsed_input[1].isdigit() or not parsed_input[2].isdigit()):
                print("Days must be integers. Ranging 0 -", parsed_data[0][len(parsed_data[0]) - 1])
                continue
            elif(int(parsed_input[2]) > parsed_data[0][len(parsed_data[0]) - 1]):
                print("range of days is invalid, days must fall between the range: 0 -", parsed_data[0][len(parsed_data[0]) - 1])
                continue
            elif(int(parsed_input[1]) > int(parsed_input[2])):
                print("Range of days is invalid, starting day must be less than ending day")
                continue
            else:
                plot_graph(parsed_data[0][int(parsed_input[1]):int(parsed_input[2]) + 1], \
                    parsed_data[3][int(parsed_input[1]):int(parsed_input[2]) + 1], 'k', "Days", "Growth Ratio (%)")  
                continue
        print('Invalid input. For instructions  type "help".')
        
#################################################################################################################################


command_line()