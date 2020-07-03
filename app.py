import pandas
import argparse
import datetime
import json

seconds_in_day = 24 * 60 * 60
date_format = '%b %d, %Y %I:%M:%S %p'
app_name = "Team2GoHoursPer"

class Data():

    def __init__(self, data={}):
        self.data = data
        self.total = 0

    def update_entry(self, in_date, out_date, key_fn):

        key = key_fn(in_date, in_date)

        point = self.data.get(key) if self.data.get(key) is not None else Point(groupByDate=in_date)

        period = Period(in_date, out_date)

        point.add_period(period)
        point.add_seconds(period.get_delta().seconds)
        self.total += period.get_delta().seconds

        self.data.update({key: point})

    def show(self):

        print(f'{app_name} ##################################################################')
        
        for key, point in self.data.items():

            delta = point.get_delta()

            st = None

            if (delta.days < 0 ):

              st = delta

            else :

              hours = delta.days * 24
              hours += delta.seconds//3600
              st = hours, (delta.seconds//60)%60

            print(f'{key} - {st[0]}h {st[1]}\'')

        print('------------------------------------------------')
        print(f'Total: {datetime.timedelta(seconds=self.total)}')

class Point:

    def __init__(self, groupByDate, periods=[], total_seconds=0):
        self.periods = periods
        self.total_seconds = total_seconds
        self.groupByDate = groupByDate

    def add_period(self, period):
        self.periods.append(period)

    def add_seconds(self, seconds):
        self.total_seconds += seconds

    def get_delta(self):
        return datetime.timedelta(seconds=self.total_seconds)

    def to_dict(self):
        return self.__dict__

class Period:

    def __init__(self, goin, goout):
        self.goin = goin
        self.goout = goout

    def get_delta(self):

        diff = self.goout - self.goin

        return datetime.timedelta(seconds=diff.seconds)

    def to_dict(self):
        return self.__dict__

parser = argparse.ArgumentParser(description=app_name)
parser.add_argument('path', type=str, help='path of the file to be processed')

args = parser.parse_args()

print("Processing: ", args.path)

df = pandas.read_excel(args.path)

reversed_df = df.iloc[::-1]

data_per_day = Data()
data_per_week = Data()

def key_per_day_fn(in_date, out_date):

  return f'{in_date.year}-{in_date.month}-{in_date.day}'

def key_per_week_fn(in_date, out_date):

  year = in_date.isocalendar()[:2][0]
  week = in_date.isocalendar()[:2][1]

  return f'{year}-{week}'

for index, row in reversed_df.iterrows():

    in_date = datetime.datetime.strptime(row["Entrada"], date_format)
    out_date = datetime.datetime.strptime(row["Salida"], date_format)

    data_per_day.update_entry(in_date, out_date, key_per_day_fn)
    # data_per_week.update_entry(in_date, out_date, key_per_week_fn)

data_per_day.show()
# data_per_week.show()
