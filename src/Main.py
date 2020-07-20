from FileParser import parse_file
from Operations import difference
from Operations import print_diff_data
from Operations import print_cases
from Operations import print_deaths
from Operations import print_tests
from Operations import print_recovered
from Operations import print_hospitalized
from Operations import print_gf_data
from Operations import plot_graph
from Operations import projection
from Operations import compute_data
from Operations import list_to_csv
from Operations import plot_graph_all
from Operations import print_new_data
from Operations import update_country_data
from FetchUpdateData import fetch_data_usa
from FetchUpdateData import diff_raw_USA_data
from FetchUpdateData import fetch_data_peru
from FetchUpdateData import diff_raw_PER_data

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
4       Recovered
5       Hospitalized
6   	Days
7   	New Cases
8	    % Cases
9   	New Deaths
10	    % Deaths
11      New Recovered
12      % Recovered
13      New Hospitalized  
14      % Hospitalized
15	    New Tests
16	    % Tests
17      Mortality Rate
18      Active Cases
'''

def command_line():
    os.system('mode con cols=150')
    np.set_printoptions(suppress=True)
    iso_code_countries = {'USA':'USA_data.csv', 'PER':'PER_data.csv'}
    header_fields = ['Date', 'Day', 'Cases', 'New Cases', '%\u0394 Cases', 'Deaths', 'New Deaths', '%\u0394 Deaths', 'Recov.', 'New Recov.', '%\u0394 Recov.',
                    'Hospit.', 'New Hospit.', '%\u0394 Hospit.', 'Tests', 'New Tests', '%\u0394 Tests', 'Mort. %', 'Active']
    instructions = ['load', 'show_diff', 'show_gf', 'show_cases', 'show_deaths', 'show_tests', 'show_recovered', 'show_hospitalized', 'delete', 'diff', 'projection',
                    'plot_cases', 'plot_cases_log', 'plot_cases_gf', 'plot_deaths', 'plot_deaths_log', 'plot_deaths_gf', 'plot_tests', 'plot_tests_log', 'plot_tests_gf',
                    'plot_recovered', 'plot_recovered_log', 'plot_recovered_gf', 'plot_hospitalized', 'plot_hospitalized_log', 'plot_hospitalized_gf', 'plot_all',
                    'update', 'fetch', '', 'export_csv', 'clear', 'exit', 'help', 'save_plot_cases']
    new_data = []
    parsed_data = 0
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
                print('fetch [ISO_CODE]                                 Update raw data from external repo of selected country')
                print('update [ISO_CODE]                                Update parsed data of selected country')
                print('load [ISO_CODE]                                  Load data set in memory')
                print('show_gf                                          Display growth factor (percent change) in cases, deaths, recovered, hospitalized, and tests')
                print('show_cases                                       Display data related to number of cases')
                print('show_deaths                                      Display data related to number of deaths')
                print('show_tests                                       Display data related to number of tests')
                print('show_recovered                                   Display data related to number of recoveries')
                print('show_hospitalized                                Display data related to number of hospitalizations')
                print('delete                                           Erase data set loaded in memory')
                print('diff                                             Shows difference of values between 2 days')
                print('projection [next_days] [avg_previous_days]       Show projection for the next x days using avg growth factor from y previous days')
                print('plot_cases [from_day] [to_day]                   Display cases graph')
                print('plot_cases_log                                   Display cases in a logarithmic graph')
                print('plot_cases_gf [from_day] [to_day]                Display cases growth factor graph')
                print('plot_deaths [from_day] [to_day]                  Display deaths graph')
                print('plot_deaths_log                                  Display deaths in a logarithmic graph')
                print('plot_deaths_gf [from_day] [to_day]               Display deaths growth factor graph')
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
                    open(os.path.dirname(os.path.abspath(__file__)) + '/../data/' + iso_code_countries[str(parsed_input[1])])
                except:
                    print(iso_code_countries[str(parsed_input[1])], "is not accesible")
                    continue
                file_name = str(parsed_input[1])
                input_data = open(os.path.dirname(os.path.abspath(__file__)) + '/../data/' + iso_code_countries[str(parsed_input[1])])
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

        if(parsed_input[0] == 'fetch'):
            if(len(parsed_input) != 2):
                print('Usage: fetch [ISO_CODE]')
            elif(not parsed_input[1] in iso_code_countries):
                print('Invalid country ISO code')
            else:
                if(parsed_input[1] == 'PER'):
                    fetch_data_peru()
                    print('PER raw data was updated.')
                elif(parsed_input[1] == 'USA'):
                    fetch_data_usa()
                    print('USA raw data was updated.')
            continue

        if(parsed_input[0] == 'update'):
            if(len(parsed_input) != 2):
                print('Usage: update [ISO_CODE]')
            elif(not parsed_input[1] in iso_code_countries):
                print('Invalid country ISO code')
            else:
                if(parsed_input[1] == 'USA'):
                    new_data = diff_raw_USA_data()
                elif(parsed_input[1] == 'PER'):
                    new_data = diff_raw_PER_data()
                if(len(new_data) == 0):
                    print(iso_code_countries[parsed_input[1]], 'is up to date.')
                else:
                    print_new_data(new_data)
                    save_new = input('Save new data up to what index? (Type integer or N/n to abort): ')
                    if(save_new.isdigit() and int(save_new) >= 0  and int(save_new) < len(new_data)):
                        if(update_country_data(iso_code_countries[parsed_input[1]], int(save_new), new_data) == True):
                            print('Updated data in', iso_code_countries[parsed_input[1]])
                    elif(save_new == 'N' or save_new == 'n'):
                        new_data = []
                        print('Data discarted')
                    else:
                        print('Invalid input. Make sure the input is an integer between 0 and', len(new_data) - 1)
            continue

        if(parsed_data == 0):
            print('Data has not been loaded into memory')
            continue

        if(parsed_input[0] == 'show_diff'):
            print_diff_data(header_fields, parsed_data)
            continue

        if(parsed_input[0] == 'show_cases'):
            print_cases(header_fields, parsed_data)
            
        if(parsed_input[0] == 'show_deaths'):
            print_deaths(header_fields, parsed_data)
            continue
            
        if(parsed_input[0] == 'show_tests'):
            print_tests(header_fields, parsed_data)
            continue
        
        if(parsed_input[0] == 'show_recovered'):
            print_recovered(header_fields, parsed_data)
            continue

        if(parsed_input[0] == 'show_hospitalized'):
            print_hospitalized(header_fields, parsed_data)
            continue

        if(parsed_input[0] == 'show_gf'):
            print_gf_data(header_fields, parsed_data)
            continue      
        
        if(parsed_input[0] == 'export_csv'):
            list_to_csv(parsed_data)
            continue

        if(parsed_input[0] == 'diff'):
            if(len(parsed_input) != 3):
                print("usage: diff [from_day] [to_day]")
            elif(not parsed_input[1].isdigit() or not parsed_input[2].isdigit()):
                print("Days must be integers. Ranging 0 -", parsed_data[0][len(parsed_data[0]) - 1])
            elif(int(parsed_input[1]) > parsed_data[6][len(parsed_data[0]) - 1] or \
                 int(parsed_input[2]) > parsed_data[6][len(parsed_data[0]) - 1]):
                print("Range of days is invalid, days must fall between the range: 0 -", parsed_data[6][len(parsed_data[0]) - 1])
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

        if(parsed_input[0] == 'plot_cases'):
            if(len(parsed_input) != 3 and len(parsed_input) != 1):
                print("Usage: plot_cases")
                print("       plot_cases [from day] [to_day]")
            elif(len(parsed_input) == 1):
                plot_graph(parsed_data[6], parsed_data[1], 'b', "Days", "Cases", file_name + ": Cases as of " + parsed_data[0][len(parsed_data[0])-1])  
            elif(not parsed_input[1].isdigit() or not parsed_input[2].isdigit()):
                print("Days must be integers. Ranging 0 -", parsed_data[6][len(parsed_data[0]) - 1])
            elif(int(parsed_input[2]) > parsed_data[6][len(parsed_data[1]) - 1]):
                print("range of days is invalid, days must fall between the range: 0 -", parsed_data[6][len(parsed_data[0]) - 1])
            elif(int(parsed_input[1]) > int(parsed_input[2])):
                print("Range of days is invalid, starting day must be less than ending day")
            else:
                plot_graph(parsed_data[6][int(parsed_input[1]):int(parsed_input[2]) + 1], parsed_data[1][int(parsed_input[1]):int(parsed_input[2]) + 1], \
                   'b', "Days", "Cases", file_name + ": Cases from day " + parsed_data[0][int(parsed_input[1])] + " to " + parsed_data[0][int(parsed_input[2])])  
            continue

        if(parsed_input[0] == 'plot_cases_log'):
            if(len(parsed_input) != 1):
                print("Usage: plot_cases_log")
            else:
                plot_graph(parsed_data[6], parsed_data[1], 'b', "Days", "Cases", file_name + ": Cases as of " + parsed_data[0][len(parsed_data[0])-1], log_view=True)
            continue

        if(parsed_input[0] == 'plot_cases_gf'):
            if(len(parsed_input) != 3 and len(parsed_input) != 1):
                print("Usage: plot_cases_gf")
                print("       plot_cases_gf [from day] [to_day]")
            elif(len(parsed_input) == 1):
                plot_graph(parsed_data[6], parsed_data[8], 'b', "Days", "Cases Growth Rate (%)", file_name + ": Cases Growth Rate (%) as of " + parsed_data[0][len(parsed_data[0])-1])  
            elif(not parsed_input[1].isdigit() or not parsed_input[2].isdigit()):
                print("Days must be integers. Ranging 0 -", parsed_data[6][len(parsed_data[0]) - 1])
            elif(int(parsed_input[2]) > parsed_data[6][len(parsed_data[1]) - 1]):
                print("range of days is invalid, days must fall between the range: 0 -", parsed_data[6][len(parsed_data[0]) - 1])
            elif(int(parsed_input[1]) > int(parsed_input[2])):
                print("Range of days is invalid, starting day must be less than ending day")
            else:
                plot_graph(parsed_data[6][int(parsed_input[1]):int(parsed_input[2]) + 1], parsed_data[8][int(parsed_input[1]):int(parsed_input[2]) + 1], \
                   'b', "Days", "Cases Growth Rate (%)", file_name + ": Cases Growth Rate (%) from day " + parsed_data[0][int(parsed_input[1])] + " to " + parsed_data[0][int(parsed_input[2])])  
            continue

        if(parsed_input[0] == 'plot_deaths'):
            if(len(parsed_input) != 3 and len(parsed_input) != 1):
                print("Usage: plot_deaths")
                print("       plot_deaths [from day] [to_day]")
            elif(len(parsed_input) == 1):
                plot_graph(parsed_data[6], parsed_data[2], 'r', "Days", "Deaths", file_name + ": Deaths as of " + parsed_data[0][len(parsed_data[0])-1])  
            elif(not parsed_input[1].isdigit() or not parsed_input[2].isdigit()):
                print("Days must be integers. Ranging 0 -", parsed_data[6][len(parsed_data[0]) - 1])
            elif(int(parsed_input[2]) > parsed_data[6][len(parsed_data[1]) - 1]):
                print("range of days is invalid, days must fall between the range: 0 -", parsed_data[6][len(parsed_data[0]) - 1])
            elif(int(parsed_input[1]) > int(parsed_input[2])):
                print("Range of days is invalid, starting day must be less than ending day")
            else:
                plot_graph(parsed_data[6][int(parsed_input[1]):int(parsed_input[2]) + 1], parsed_data[2][int(parsed_input[1]):int(parsed_input[2]) + 1], \
                   'r', "Days", "Deaths", file_name + ": Deaths from day " + parsed_data[0][int(parsed_input[1])] + " to " + parsed_data[0][int(parsed_input[2])])  
            continue

        if(parsed_input[0] == 'plot_deaths_log'):
            if(len(parsed_input) != 1):
                print("Usage: plot_deaths_log")
            else:
                plot_graph(parsed_data[6], parsed_data[2], 'r', "Days", "Deaths", file_name + ": Deaths as of " + parsed_data[0][len(parsed_data[0])-1], log_view=True)
            continue

        if(parsed_input[0] == 'plot_deaths_gf'):
            if(len(parsed_input) != 3 and len(parsed_input) != 1):
                print("Usage: plot_deaths_gf")
                print("       plot_deaths_gf [from day] [to_day]")
            elif(len(parsed_input) == 1):
                plot_graph(parsed_data[6], parsed_data[10], 'r', "Days", "Deaths Growth Rate (%)", file_name + ": Deaths Growth Rate (%) as of " + parsed_data[0][len(parsed_data[0])-1])  
            elif(not parsed_input[1].isdigit() or not parsed_input[2].isdigit()):
                print("Days must be integers. Ranging 0 -", parsed_data[6][len(parsed_data[0]) - 1])
            elif(int(parsed_input[2]) > parsed_data[6][len(parsed_data[1]) - 1]):
                print("range of days is invalid, days must fall between the range: 0 -", parsed_data[6][len(parsed_data[0]) - 1])
            elif(int(parsed_input[1]) > int(parsed_input[2])):
                print("Range of days is invalid, starting day must be less than ending day")
            else:
                plot_graph(parsed_data[6][int(parsed_input[1]):int(parsed_input[2]) + 1], parsed_data[10][int(parsed_input[1]):int(parsed_input[2]) + 1], \
                   'r', "Days", "Deaths Growth Rate (%)", file_name + ": Deaths Growth Rate (%) from day " + parsed_data[0][int(parsed_input[1])] + " to " + parsed_data[0][int(parsed_input[2])])  
            continue

        if(parsed_input[0] == 'plot_tests'):
            if(len(parsed_input) != 3 and len(parsed_input) != 1):
                print("Usage: plot_tests")
                print("       plot_tests [from day] [to_day]")
            elif(len(parsed_input) == 1):
                plot_graph(parsed_data[6], parsed_data[3], 'c', "Days", "Tests", file_name + ": Tests as of " + parsed_data[0][len(parsed_data[0])-1])  
            elif(not parsed_input[1].isdigit() or not parsed_input[2].isdigit()):
                print("Days must be integers. Ranging 0 -", parsed_data[6][len(parsed_data[0]) - 1])
            elif(int(parsed_input[2]) > parsed_data[6][len(parsed_data[1]) - 1]):
                print("range of days is invalid, days must fall between the range: 0 -", parsed_data[6][len(parsed_data[0]) - 1])
            elif(int(parsed_input[1]) > int(parsed_input[2])):
                print("Range of days is invalid, starting day must be less than ending day")
            else:
                plot_graph(parsed_data[6][int(parsed_input[1]):int(parsed_input[2]) + 1], parsed_data[3][int(parsed_input[1]):int(parsed_input[2]) + 1], \
                   'c', "Days", "Tests", file_name + ": Tests from day " + parsed_data[0][int(parsed_input[1])] + " to " + parsed_data[0][int(parsed_input[2])])  
            continue

        if(parsed_input[0] == 'plot_tests_log'):
            if(len(parsed_input) != 1):
                print("Usage: plot_tests_log")
            else:
                plot_graph(parsed_data[6], parsed_data[3], 'c', "Days", "Tests", file_name + ": Tests as of " + parsed_data[0][len(parsed_data[0])-1], log_view=True)
            continue

        if(parsed_input[0] == 'plot_tests_gf'):
            if(len(parsed_input) != 3 and len(parsed_input) != 1):
                print("Usage: plot_tests_gf")
                print("       plot_tests_gf [from day] [to_day]")
            elif(len(parsed_input) == 1):
                plot_graph(parsed_data[6], parsed_data[16], 'c', "Days", "Tests Growth Rate (%)", file_name + ": Tests Growth Rate (%) as of " + parsed_data[0][len(parsed_data[0])-1])  
            elif(not parsed_input[1].isdigit() or not parsed_input[2].isdigit()):
                print("Days must be integers. Ranging 0 -", parsed_data[6][len(parsed_data[0]) - 1])
            elif(int(parsed_input[2]) > parsed_data[6][len(parsed_data[1]) - 1]):
                print("range of days is invalid, days must fall between the range: 0 -", parsed_data[6][len(parsed_data[0]) - 1])
            elif(int(parsed_input[1]) > int(parsed_input[2])):
                print("Range of days is invalid, starting day must be less than ending day")
            else:
                plot_graph(parsed_data[6][int(parsed_input[1]):int(parsed_input[2]) + 1], parsed_data[16][int(parsed_input[1]):int(parsed_input[2]) + 1], \
                   'c', "Days", "Tests Growth Rate (%)", file_name + ": Tests Growth Rate (%) from day " + parsed_data[0][int(parsed_input[1])] + " to " + parsed_data[0][int(parsed_input[2])])  
            continue

        if(parsed_input[0] == 'plot_recovered'):
            if(len(parsed_input) != 3 and len(parsed_input) != 1):
                print("Usage: plot_recovered")
                print("       plot_recovered [from day] [to_day]")
            elif(len(parsed_input) == 1):
                plot_graph(parsed_data[6], parsed_data[4], 'g', "Days", "Recovered", file_name + ": Recovered as of " + parsed_data[0][len(parsed_data[0])-1])  
            elif(not parsed_input[1].isdigit() or not parsed_input[2].isdigit()):
                print("Days must be integers. Ranging 0 -", parsed_data[6][len(parsed_data[0]) - 1])
            elif(int(parsed_input[2]) > parsed_data[6][len(parsed_data[1]) - 1]):
                print("range of days is invalid, days must fall between the range: 0 -", parsed_data[4][len(parsed_data[0]) - 1])
            elif(int(parsed_input[1]) > int(parsed_input[2])):
                print("Range of days is invalid, starting day must be less than ending day")
            else:
                plot_graph(parsed_data[6][int(parsed_input[1]):int(parsed_input[2]) + 1], parsed_data[4][int(parsed_input[1]):int(parsed_input[2]) + 1], \
                   'g', "Days", "Recovered", file_name + ": Recovered from day " + parsed_data[0][int(parsed_input[1])] + " to " + parsed_data[0][int(parsed_input[2])])  
            continue

        if(parsed_input[0] == 'plot_recovered_log'):
            if(len(parsed_input) != 1):
                print("Usage: plot_recovered_log")
            else:
                plot_graph(parsed_data[6], parsed_data[4], 'g', "Days", "Recovered", file_name + ": Recovered as of " + parsed_data[0][len(parsed_data[0])-1], log_view=True)
            continue

        if(parsed_input[0] == 'plot_recovered_gf'):
            if(len(parsed_input) != 3 and len(parsed_input) != 1):
                print("Usage: plot_recovered_gf")
                print("       plot_recovered_gf [from day] [to_day]")
            elif(len(parsed_input) == 1):
                plot_graph(parsed_data[6], parsed_data[12], 'g', "Days", "Recovered Growth Rate (%)", file_name + ": Recovered Growth Rate (%) as of " + parsed_data[0][len(parsed_data[0])-1])  
            elif(not parsed_input[1].isdigit() or not parsed_input[2].isdigit()):
                print("Days must be integers. Ranging 0 -", parsed_data[6][len(parsed_data[0]) - 1])
            elif(int(parsed_input[2]) > parsed_data[6][len(parsed_data[1]) - 1]):
                print("range of days is invalid, days must fall between the range: 0 -", parsed_data[6][len(parsed_data[0]) - 1])
            elif(int(parsed_input[1]) > int(parsed_input[2])):
                print("Range of days is invalid, starting day must be less than ending day")
            else:
                plot_graph(parsed_data[6][int(parsed_input[1]):int(parsed_input[2]) + 1], parsed_data[12][int(parsed_input[1]):int(parsed_input[2]) + 1], \
                   'g', "Days", "Recovered Growth Rate (%)", file_name + ": Recovered Growth Rate (%) from day " + parsed_data[0][int(parsed_input[1])] + " to " + parsed_data[0][int(parsed_input[2])])  
            continue

        if(parsed_input[0] == 'plot_hospitalized'):
            if(len(parsed_input) != 3 and len(parsed_input) != 1):
                print("Usage: plot_hospitalized")
                print("       plot_hospitalized [from day] [to_day]")
            elif(len(parsed_input) == 1):
                plot_graph(parsed_data[6], parsed_data[5], 'm', "Days", "Hospitalized", file_name + ": Hospitalized as of " + parsed_data[0][len(parsed_data[0])-1])  
            elif(not parsed_input[1].isdigit() or not parsed_input[2].isdigit()):
                print("Days must be integers. Ranging 0 -", parsed_data[6][len(parsed_data[0]) - 1])
            elif(int(parsed_input[2]) > parsed_data[6][len(parsed_data[1]) - 1]):
                print("range of days is invalid, days must fall between the range: 0 -", parsed_data[6][len(parsed_data[0]) - 1])
            elif(int(parsed_input[1]) > int(parsed_input[2])):
                print("Range of days is invalid, starting day must be less than ending day")
            else:
                plot_graph(parsed_data[6][int(parsed_input[1]):int(parsed_input[2]) + 1], parsed_data[5][int(parsed_input[1]):int(parsed_input[2]) + 1], \
                   'm', "Days", "Hospitalized", file_name + ": Hospitalized from day " + parsed_data[0][int(parsed_input[1])] + " to " + parsed_data[0][int(parsed_input[2])])  
            continue

        if(parsed_input[0] == 'plot_hospitalized_log'):
            if(len(parsed_input) != 1):
                print("Usage: plot_hospitalized_log")
            else:
                plot_graph(parsed_data[6], parsed_data[3], 'm', "Days", "Hospitalized", file_name + ": Hospitalized as of " + parsed_data[0][len(parsed_data[0])-1], log_view=True)
            continue

        if(parsed_input[0] == 'plot_hospitalized_gf'):
            if(len(parsed_input) != 3 and len(parsed_input) != 1):
                print("Usage: plot_hospitalized_gf")
                print("       plot_hospitalized_gf [from day] [to_day]")
            elif(len(parsed_input) == 1):
                plot_graph(parsed_data[6], parsed_data[14], 'm', "Days", "Hospitalized Growth Rate (%)", file_name + ": Hospitalized Growth Rate (%) as of " + parsed_data[0][len(parsed_data[0])-1])  
            elif(not parsed_input[1].isdigit() or not parsed_input[2].isdigit()):
                print("Days must be integers. Ranging 0 -", parsed_data[6][len(parsed_data[0]) - 1])
            elif(int(parsed_input[2]) > parsed_data[6][len(parsed_data[1]) - 1]):
                print("range of days is invalid, days must fall between the range: 0 -", parsed_data[6][len(parsed_data[0]) - 1])
            elif(int(parsed_input[1]) > int(parsed_input[2])):
                print("Range of days is invalid, starting day must be less than ending day")
            else:
                plot_graph(parsed_data[6][int(parsed_input[1]):int(parsed_input[2]) + 1], parsed_data[14][int(parsed_input[1]):int(parsed_input[2]) + 1], \
                   'm', "Days", "Hospitalized Growth Rate (%)", file_name + ": Hospitalized Growth Rate (%) from day " + parsed_data[0][int(parsed_input[1])] + " to " + parsed_data[0][int(parsed_input[2])])  
            continue

        if(parsed_input[0] == 'plot_all'):
            if(len(parsed_input) != 3 and len(parsed_input) != 1):
                print("Usage: plot_all")
                print("       plot_all [from day] [to_day]")
            elif(len(parsed_input) == 1):
                plot_graph_all(parsed_data, file_name + ": Cases, Deaths, Recovered, Active Cases as of " + parsed_data[0][len(parsed_data[0])-1], 0, len(parsed_data[0])-1)  
            elif(not parsed_input[1].isdigit() or not parsed_input[2].isdigit()):
                print("Days must be integers. Ranging 0 -", parsed_data[6][len(parsed_data[0]) - 1])
            elif(int(parsed_input[2]) > parsed_data[6][len(parsed_data[1]) - 1]):
                print("range of days is invalid, days must fall between the range: 0 -", parsed_data[6][len(parsed_data[0]) - 1])
            elif(int(parsed_input[1]) > int(parsed_input[2])):
                print("Range of days is invalid, starting day must be less than ending day")
            else:
                plot_graph_all(parsed_data, file_name + ": Cases, Deaths, Recovered, Active Cases from " + parsed_data[0][int(parsed_input[1])] + " to " \
                    + parsed_data[0][int(parsed_input[2])], int(parsed_input[1]), int(parsed_input[2]))  
            continue
        
        if(parsed_input[0] == 'save_plot_cases'):
            if(len(parsed_input) != 3 and len(parsed_input) != 1):
                print("Usage: save_plot_cases")
                print("       save_plot_cases [from day] [to_day]")
            elif(len(parsed_input) == 1):
                plot_graph(parsed_data[6], parsed_data[1], 'b', "Days", "Cases", file_name + ": Cases as of " + parsed_data[0][len(parsed_data[0])-1], \
                file_name='cases', save=True)  
            elif(not parsed_input[1].isdigit() or not parsed_input[2].isdigit()):
                print("Days must be integers. Ranging 0 -", parsed_data[6][len(parsed_data[0]) - 1])
            elif(int(parsed_input[2]) > parsed_data[6][len(parsed_data[1]) - 1]):
                print("range of days is invalid, days must fall between the range: 0 -", parsed_data[6][len(parsed_data[0]) - 1])
            elif(int(parsed_input[1]) > int(parsed_input[2])):
                print("Range of days is invalid, starting day must be less than ending day")
            else:
                plot_graph(parsed_data[6][int(parsed_input[1]):int(parsed_input[2]) + 1], parsed_data[1][int(parsed_input[1]):int(parsed_input[2]) + 1], \
                   'b', "Days", "Cases", file_name + ": Cases from day " + parsed_data[0][int(parsed_input[1])] + " to " + parsed_data[0][int(parsed_input[2])], \
                    file_name='cases_from_' + parsed_data[0][int(parsed_input[1])] + '_to_' + parsed_data[0][int(parsed_input[2])], save=True)  
            continue

        print('Invalid input. For instructions  type "help".')
        
#################################################################################################################################

command_line()