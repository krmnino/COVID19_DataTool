import numpy as np

def parse_country(path):
    country_data = open(path)
    dates = np.asarray([])
    cases = np.array([])
    growth_factor = np.array([0, 1])
    for line in country_data:
        parsed_line = line.split(',')
        date = parsed_line[0]
        day_cases = parsed_line[1]
        day_deaths = parsed_line[2]
        day_tests = parsed_line[3]