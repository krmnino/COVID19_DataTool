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
        print("ISO:", self.iso_code)
        print("Date:", self.date)
        print("Cases:", self.cases)
        print("Deaths:", self.deaths)
        print("Tests:", self.tests)

    def show_comparison(self, dp):
        print('%12s'%('FIELDS'), '|', '%12s'%(self.date), '|' ,'%12s'%(dp.date))
        print('-------------+--------------+-------------')
        print('%12s'%('ISO'), '|', '%12s'%(self.iso_code), '|' ,'%12s'%(dp.iso_code))
        print('%12s'%('Cases'), '|', '%12s'%(self.cases), '|' ,'%12s'%(dp.cases))
        print('%12s'%('Deaths'), '|', '%12s'%(self.deaths), '|' ,'%12s'%(dp.deaths))
        print('%12s'%('Tests'), '|', '%12s'%(self.tests), '|' ,'%12s'%(dp.tests))