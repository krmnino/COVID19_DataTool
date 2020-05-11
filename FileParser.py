import numpy as np

def parse_file(input_data):
    dates = np.asarray([])
    days = np.array([])
    cases = np.array([])
    growth_factor = np.array([0, 1])
    day_counter = 0
    for i, line in enumerate(input_data):
        if(i == 0):
            header = line.split(',')
            continue
        if(line == '\n'):
            break
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