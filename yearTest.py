import tweet
import datetime
# pick a year
year = 2006
# create date objects
begin_year = datetime.date(year, 1, 1)
end_year = datetime.date(year, 12, 31)
one_day = datetime.timedelta(days=1)
next_day = begin_year
for day in range(0, 366):  # includes potential leap year
    if next_day > end_year:
        break
#    print ("echo '" + str(next_day.month)+ " / "+str(next_day.day)+"' >> testOutput.txt")
    print ("python3 tweet.py "+str(next_day.month)+ " "+str(next_day.day) +" >> testOutput.txt")
    # increment date object by one day
    next_day += one_day
