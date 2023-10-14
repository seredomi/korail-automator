from nav import *
from search import *
from profiles import *


import csv
import re
from datetime import datetime, timezone, timedelta
import time
import sys
import os
from os import path

def getAction() -> int:
    print("enter:\n" + 
          "  1 to get times\n" +
          "  2 to book ticket\n" +
          "  3 to view ticket\n" +
          "  4 to cancel ticket\n" +
          "  5 to exit")
    choice = input()
    while not choice.isdigit() or int(choice) < 1 or int(choice) > 5:
        print("should be a number b/w 1 and 5, try again: ", end="")
        choice = input()
    return int(choice)

def main():

        # get profile
        curr_profile = getProfile()

        while True:
            choice = getAction()
            if choice == 1:
                driver = startBrowser()
                curr_search = getSearch()
                showSchedule(driver, curr_search, curr_profile)
                num_trains = showSchedule(driver, curr_search, curr_profile)
                indices = selectTrain(num_trains)
                bookTicket(driver, curr_profile, indices)
                payTicket(driver, curr_profile)
            else:
                print("not yet implemented")
                continue

        # keep window open
        while True:
            i = 1

if __name__ == "__main__":
    main()
