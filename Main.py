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

'''
Structure of parsed_data list after computation
index   contents
0	    Dates
1	    Cases
2	    Deaths
3	    Tests
4   	Days
5   	New Cases
6	    % Cases
7   	New Deaths
8	    % Deaths
9	    New Tests
10	    % Tests
'''

def command_line():
    os.system("mode con cols=150")
    np.set_printoptions(suppress=True)
    header_fields = ['Date', 'Day', 'Cases', 'New Cases', '%\u0394 Cases', 'Deaths', 'New Deaths', '%\u0394 Deaths', 'Tests', 'New Tests', '%\u0394 Tests']
    parsed_data = 0
    instructions = ['load', 'show', 'show_all', 'delete', 'diff', 'projection', 'plot_cases', 'plot_cases_log', 'plot_cases_gf', 'plot_deaths', 'plot_deaths_log',
                   'plot_deaths_gf', 'plot_tests', 'plot_tests_log', 'plot_tests_gf', 'export_csv', 'clear', 'exit', 'help']
    file_name = ''
    while(True):
        input_cmd = input('>> ')
        parsed_input = input_cmd.split()
        if(len(parsed_input) == 0):
            continue

        if(parsed_input[0] not in instructions):
            print('Invalid command. Type "help" for instructions.')
            continue

        if(parsed_input[0] == 'exit'):
            if(len(parsed_input) != 1):
                print('Usage: exit')
                continue
            else:
                print('Exiting...')
                break

        if(parsed_input[0] == 'help'):
            if(len(parsed_input) != 1):
                print('Usage: help')
            else:
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

        if(parsed_input[0] == 'clear'):
            if(len(parsed_input) != 1):
                print('Usage: clear')
            elif(platform.system() == "Windows"):
                os.system("cls")
            elif(platform.system() == "Linux"):
                os.system("clear")
            continue

        if(parsed_input[0] == 'load'):
            if(len(parsed_input) != 2):
                print("Usage: load [FILE PATH]")
            else:
                try:
                    input_data = open(str(parsed_input[1]))
                except:
                    print(parsed_input[1], "is not accesible")
                    continue
                file_name = str(parsed_input[1])
                input_data = open(str(parsed_input[1]))
                parsed_data = parse_file(input_data)
                input_data.close()
                if(parsed_data != 0):
                    parsed_data = compute_data(parsed_data)
                    print("Loaded and computed data from", parsed_input[1])
            continue

        if(parsed_input[0] == 'delete'):
            parsed_data = 0
            file_name = ''
            continue

        if(parsed_data == 0):
            print('Data has not been loaded into memory')
            continue

        if(parsed_input[0] == 'show'):
            print_data(header_fields, parsed_data)
            continue

        if(parsed_input[0] == 'diff'):
            if(len(parsed_input) != 3):
                print("usage: diff [from_day] [to_day]")
            elif(not parsed_input[1].isdigit() or not parsed_input[2].isdigit()):
                print("Days must be integers. Ranging 0 -", parsed_data[0][len(parsed_data[0]) - 1])
            elif(int(parsed_input[1]) > parsed_data[4][len(parsed_data[0]) - 1] or \
                 int(parsed_input[2]) > parsed_data[4][len(parsed_data[0]) - 1]):
                print("Range of days is invalid, days must fall between the range: 0 -", parsed_data[0][len(parsed_data[0]) - 1])
            elif(int(parsed_input[1]) > int(parsed_input[2])):
                print("Range of days is invalid, starting day must be less than ending day")
            else:
                difference(parsed_data, int(parsed_input[1]), int(parsed_input[2]))
            continue

        if(parsed_input[0] == 'projection'):
            if(len(parsed_input) != 3):
                print("Usage: projection [next_days] [avg_previous_days]")
            elif(not parsed_input[1].isdigit() or not parsed_input[2]):
                print("[next_days] and [avg_previous_days] values must be integers.")
            else:
                projection(int(parsed_input[1]), int(parsed_input[2]), parsed_data)
            continue

        if(parsed_input[0] == 'csv_format'):
            print('Column 1: Date')
            print('Column 2: Cases')
            print('Column 2: Cases')

        if(parsed_input[0] == 'plot_cases'):
            if(len(parsed_input) != 3 and len(parsed_input) != 1):
                print("Usage: plot_cases")
                print("       plot_cases [from day] [to_day]")
            elif(len(parsed_input) == 1):
                plot_graph(parsed_data[4], parsed_data[1], 'b', "Days", "Cases", file_name + ": Cases as of " + parsed_data[0][len(parsed_data[0])-1])  
            elif(not parsed_input[1].isdigit() or not parsed_input[2].isdigit()):
                print("Days must be integers. Ranging 0 -", parsed_data[0][len(parsed_data[0]) - 1])
            elif(int(parsed_input[2]) > parsed_data[1][len(parsed_data[1]) - 1]):
                print("range of days is invalid, days must fall between the range: 0 -", parsed_data[0][len(parsed_data[0]) - 1])
            elif(int(parsed_input[1]) > int(parsed_input[2])):
                print("Range of days is invalid, starting day must be less than ending day")
            else:
                plot_graph(parsed_data[4][int(parsed_input[1]):int(parsed_input[2]) + 1], parsed_data[1][int(parsed_input[1]):int(parsed_input[2]) + 1], \
                   'b', "Days", "Cases", file_name + ":Cases from day " + parsed_data[0][int(parsed_input[1])] + " from " + parsed_data[0][int(parsed_input[2])])  
            continue

        if(parsed_input[0] == 'plot_cases_log'):
            if(len(parsed_input) != 1):
                print("Usage: plot_cases_log")
            else:
                plot_graph_log(parsed_data[4], parsed_data[1], 'b', "Days", "Cases", file_name + ": Cases as of " + parsed_data[0][len(parsed_data[0])-1])
            continue

        if(parsed_input[0] == 'plot_cases_gf'):
            if(len(parsed_input) != 3 and len(parsed_input) != 1):
                print("Usage: plot_cases_gf")
                print("       plot_cases_gf [from day] [to_day]")
            elif(len(parsed_input) == 1):
                plot_graph(parsed_data[4], parsed_data[6], 'b', "Days", "Cases Growth Ratio (%)", file_name + ": Cases Growth Ratio (%) as of " + parsed_data[0][len(parsed_data[0])-1])  
            elif(not parsed_input[1].isdigit() or not parsed_input[2].isdigit()):
                print("Days must be integers. Ranging 0 -", parsed_data[0][len(parsed_data[0]) - 1])
            elif(int(parsed_input[2]) > parsed_data[1][len(parsed_data[1]) - 1]):
                print("range of days is invalid, days must fall between the range: 0 -", parsed_data[0][len(parsed_data[0]) - 1])
            elif(int(parsed_input[1]) > int(parsed_input[2])):
                print("Range of days is invalid, starting day must be less than ending day")
            else:
                plot_graph(parsed_data[4][int(parsed_input[1]):int(parsed_input[2]) + 1], parsed_data[6][int(parsed_input[1]):int(parsed_input[2]) + 1], \
                   'b', "Days", "Cases Growth Ratio (%)", file_name + ":Cases Growth Ratio (%) from day " + parsed_data[0][int(parsed_input[1])] + " from " + parsed_data[0][int(parsed_input[2])])  
            continue

        if(parsed_input[0] == 'plot_deaths'):
            if(len(parsed_input) != 3 and len(parsed_input) != 1):
                print("Usage: plot_deaths")
                print("       plot_deaths [from day] [to_day]")
            elif(len(parsed_input) == 1):
                plot_graph(parsed_data[4], parsed_data[2], 'r', "Days", "Deaths", file_name + ": Deaths as of " + parsed_data[0][len(parsed_data[0])-1])  
            elif(not parsed_input[1].isdigit() or not parsed_input[2].isdigit()):
                print("Days must be integers. Ranging 0 -", parsed_data[0][len(parsed_data[0]) - 1])
            elif(int(parsed_input[2]) > parsed_data[1][len(parsed_data[1]) - 1]):
                print("range of days is invalid, days must fall between the range: 0 -", parsed_data[0][len(parsed_data[0]) - 1])
            elif(int(parsed_input[1]) > int(parsed_input[2])):
                print("Range of days is invalid, starting day must be less than ending day")
            else:
                plot_graph(parsed_data[4][int(parsed_input[1]):int(parsed_input[2]) + 1], parsed_data[2][int(parsed_input[1]):int(parsed_input[2]) + 1], \
                   'r', "Days", "Deaths", file_name + ":Deaths from day " + parsed_data[0][int(parsed_input[1])] + " from " + parsed_data[0][int(parsed_input[2])])  
            continue

        if(parsed_input[0] == 'plot_deaths_log'):
            if(len(parsed_input) != 1):
                print("Usage: plot_deaths_log")
            else:
                plot_graph_log(parsed_data[4], parsed_data[2], 'r', "Days", "Deaths", file_name + ": Deaths as of " + parsed_data[0][len(parsed_data[0])-1])
            continue

        if(parsed_input[0] == 'plot_deaths_gf'):
            if(len(parsed_input) != 3 and len(parsed_input) != 1):
                print("Usage: plot_deaths_gf")
                print("       plot_deaths_gf [from day] [to_day]")
            elif(len(parsed_input) == 1):
                plot_graph(parsed_data[4], parsed_data[8], 'r', "Days", "Deaths Growth Ratio (%)", file_name + ": Deaths Growth Ratio (%) as of " + parsed_data[0][len(parsed_data[0])-1])  
            elif(not parsed_input[1].isdigit() or not parsed_input[2].isdigit()):
                print("Days must be integers. Ranging 0 -", parsed_data[0][len(parsed_data[0]) - 1])
            elif(int(parsed_input[2]) > parsed_data[1][len(parsed_data[1]) - 1]):
                print("range of days is invalid, days must fall between the range: 0 -", parsed_data[0][len(parsed_data[0]) - 1])
            elif(int(parsed_input[1]) > int(parsed_input[2])):
                print("Range of days is invalid, starting day must be less than ending day")
            else:
                plot_graph(parsed_data[4][int(parsed_input[1]):int(parsed_input[2]) + 1], parsed_data[8][int(parsed_input[1]):int(parsed_input[2]) + 1], \
                   'r', "Days", "Deaths Growth Ratio (%)", file_name + ":Deaths Growth Ratio (%) from day " + parsed_data[0][int(parsed_input[1])] + " from " + parsed_data[0][int(parsed_input[2])])  
            continue

        if(parsed_input[0] == 'plot_tests'):
            if(len(parsed_input) != 3 and len(parsed_input) != 1):
                print("Usage: plot_tests")
                print("       plot_tests [from day] [to_day]")
            elif(len(parsed_input) == 1):
                plot_graph(parsed_data[4], parsed_data[3], 'g', "Days", "Tests", file_name + ": Tests as of " + parsed_data[0][len(parsed_data[0])-1])  
            elif(not parsed_input[1].isdigit() or not parsed_input[2].isdigit()):
                print("Days must be integers. Ranging 0 -", parsed_data[0][len(parsed_data[0]) - 1])
            elif(int(parsed_input[2]) > parsed_data[1][len(parsed_data[1]) - 1]):
                print("range of days is invalid, days must fall between the range: 0 -", parsed_data[0][len(parsed_data[0]) - 1])
            elif(int(parsed_input[1]) > int(parsed_input[2])):
                print("Range of days is invalid, starting day must be less than ending day")
            else:
                plot_graph(parsed_data[4][int(parsed_input[1]):int(parsed_input[2]) + 1], parsed_data[3][int(parsed_input[1]):int(parsed_input[2]) + 1], \
                   'g', "Days", "Tests", file_name + ":Tests from day " + parsed_data[0][int(parsed_input[1])] + " from " + parsed_data[0][int(parsed_input[2])])  
            continue

        if(parsed_input[0] == 'plot_tests_log'):
            if(len(parsed_input) != 1):
                print("Usage: plot_tests_log")
            else:
                plot_graph_log(parsed_data[4], parsed_data[3], 'g', "Days", "Tests", file_name + ": Tests as of " + parsed_data[0][len(parsed_data[0])-1])
            continue

        if(parsed_input[0] == 'plot_tests_gf'):
            if(len(parsed_input) != 3 and len(parsed_input) != 1):
                print("Usage: plot_tests_gf")
                print("       plot_tests_gf [from day] [to_day]")
            elif(len(parsed_input) == 1):
                plot_graph(parsed_data[4], parsed_data[10], 'g', "Days", "Tests Growth Ratio (%)", file_name + ": Tests Growth Ratio (%) as of " + parsed_data[0][len(parsed_data[0])-1])  
            elif(not parsed_input[1].isdigit() or not parsed_input[2].isdigit()):
                print("Days must be integers. Ranging 0 -", parsed_data[0][len(parsed_data[0]) - 1])
            elif(int(parsed_input[2]) > parsed_data[1][len(parsed_data[1]) - 1]):
                print("range of days is invalid, days must fall between the range: 0 -", parsed_data[0][len(parsed_data[0]) - 1])
            elif(int(parsed_input[1]) > int(parsed_input[2])):
                print("Range of days is invalid, starting day must be less than ending day")
            else:
                plot_graph(parsed_data[4][int(parsed_input[1]):int(parsed_input[2]) + 1], parsed_data[10][int(parsed_input[1]):int(parsed_input[2]) + 1], \
                   'g', "Days", "Tests Growth Ratio (%)", file_name + ":Tests Growth Ratio (%) from day " + parsed_data[0][int(parsed_input[1])] + " from " + parsed_data[0][int(parsed_input[2])])  
            continue

        print('Invalid input. For instructions  type "help".')
        
#################################################################################################################################

command_line()