class DataPoint:
    iso_code = ''
    date = ''
    cases = 0
    deaths = 0
    tests = 0

    def __init__(self, iso_, date_, cases_, deaths_, tests_):
        self.iso_code = iso_
        self.date = date_
        self.cases = cases_
        self.deaths = deaths_
        self.tests = tests_
    
    def get_data(self):
        return [self.iso_code, self.date, self.cases, self.deaths, self.tests]

    def show(self):
        #print('%12s'%(str(self.iso_code)), '%12s'%(str(self.date)), '%12s'%(str(self.cases), '%12s'%(str(self.deaths), '%12s'%(str(self.tests)))))
        print('%12s'%(str(self.iso_code)), end = '')
        print('%15s'%(str(self.date)), end = '')
        print('%12s'%(str(self.cases)), end = '')
        print('%12s'%(str(self.deaths)), end = '')
        print('%12s'%(str(self.tests)))



