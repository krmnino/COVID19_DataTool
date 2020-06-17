class DataPoint:
    date = ''
    cases = 0
    deaths = 0
    tests = 0

    def __init__(self, date_, cases_, deaths_, tests_):
        self.date = date_
        self.cases = cases_
        self.deaths = deaths_
        self.tests = tests_
    
    def get_data(self):
        return [self.date, self.cases, self.deaths, self.tests]

    def show(self):
        #print('%12s'%(str(self.iso_code)), '%12s'%(str(self.date)), '%12s'%(str(self.cases), '%12s'%(str(self.deaths), '%12s'%(str(self.tests)))))
        print('%15s'%(str(self.date)), end = '')
        print('%12s'%(str(self.cases)), end = '')
        print('%12s'%(str(self.deaths)), end = '')
        print('%12s'%(str(self.tests)))



