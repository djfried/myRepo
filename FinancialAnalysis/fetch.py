import csv
import pprint
from datetime import datetime, timedelta
from yahoo_finance import Share


def getNDaysAgo(N):
    date_N_days_ago = datetime.now() - timedelta(days=N)

    return str(date_N_days_ago.date())


fname= 'C:\dump\companylist.csv'
with open(fname) as f:
    content = csv.reader(f,delimiter=',')
    twentDay = getNDaysAgo(1)
    today=str(datetime.now().date())
    for line in content:
        if any(x not in line[0] for x in ['^','$']):
            stock = Share(line[0])
            print line[0]
            print stock.get_name()
            print stock.get_50day_moving_avg()
            # print stock.get_200day_moving_avg()
            print stock.get_avg_daily_volume()
            pprint(stock.get_historical(twentDay, today))
        else:
            print line[0] + ' contains a special character******'



# yahoo = Share('WWW')
# print yahoo.get_name()
# print yahoo.get_open();
#
# print yahoo.get_50day_moving_avg();
#
# print yahoo.get_avg_daily_volume()