import constants as c

from datetime import datetime, timedelta, timezone
import time

class Search:
    def __init__(self, depStn, arrStn, depTime):
        self.depStn = depStn
        self.arrStn = arrStn
        self.depTime = depTime

def getSearch() -> Search:

    print("where are you leaving from? ", end="")
    depStn = input()
    if depStn in c.STATION_SHORTCUTS:
        depStn = c.STATION_SHORTCUTS[depStn]
    print("where are you going? ", end="")
    arrStn = input()
    if arrStn in c.STATION_SHORTCUTS:
        arrStn = c.STATION_SHORTCUTS[arrStn]
    print("what day/time? (now, hh, hh:mm, mm/dd hh:mm) ", end="")
    depTime = datetime(1, 1, 1)
    while depTime.year == 1:
        depTimeIn = input()
        if depTimeIn == "now":
            depTime = datetime.now(timezone(timedelta(hours=9), 'KST'))
        else:
            try:
                year = str(datetime.now().year)
                depTime = datetime.strptime(year + depTimeIn, "%Y%m/%d %H:%M")
            except ValueError:
                print("bad format, try again: ", end="")
                continue
            # if month is in the past, add a year
            if datetime.now().month == 12 and depTime.month < 4:
                depTime = datetime(depTime.year+1, depTime.month, depTime.day,
                                   depTime.hour, depTime.minute)
            if depTime < datetime.now():
                print("date is in the past, try again: ", end="")
                depTime = datetime(1, 1, 1)
            elif depTime - datetime.now() > timedelta(days=29):
                print("can only book trains 30 days in advance, try again: ", end="")
                depTime = datetime(1, 1, 1)
                
    return Search(depStn, arrStn, depTime)
