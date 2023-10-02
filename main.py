from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import service
from selenium.webdriver.firefox.service import Service

import csv
import re
from datetime import datetime, timezone, timedelta

# PROFILE STUFF -----------------------------------------------------------------------------------
class Profile:
    def __init__(self, pname, fname, lname, pin, email, country, isDefault=False):
        self.pname = pname
        self.fname = fname
        self.lname = lname
        self.pin = pin
        self.email = email
        self.country = country

class Search:
    def __init__(self, depStn, arrStn, depTime):
        self.depStn = depStn
        self.arrStn = arrStn
        self.depTime = depTime

def getProfile() -> Profile:
    filename = "./user-info.csv"
    profiles = list()
    # try to read from file
    try:
        with open(filename, 'r', newline='') as csvfile:
            profilereader = csv.reader(csvfile)

            for row in profilereader:
                if len(row) != 6:
                    raise ValueError("bad csv -- should be 6 fields in row: " + str(row))
                if row[0] == "pname":
                    continue
                for j in range(len(row)): 
                    row[j] = row[j].strip()
                profiles.append(Profile(row[0], row[1].upper(), row[2].upper(),
                                        row[3], row[4], row[5].upper()))
        if len(profiles) == 1:
            print("using profile: " + profiles[0].pname)
            return profiles[0]
        else:
            print("choose your profile. enter:")
            for i in range(len(profiles)):
                print("  " + str(i+1) + " for " + profiles[i].pname)
            choice = input()
            while not choice.isdigit() or int(choice) < 1 or int(choice) > len(profiles):
                print("should be a number bw 1 and " + str(len(profiles)) + ", try again: ", end="")
                choice = input()
            return profiles[int(choice)-1]


    # else create new file
    except FileNotFoundError:
        with open(filename, 'w', newline='') as csvfile:
            print("no profiles in user-info.csv:")
            newProf = newProfile()
            profiles.append(newProf)
            csvfile.write(newProf.pname + "," + newProf.fname + "," + newProf.lname + "," +
                          newProf.pin + "," + newProf.email + "," + newProf.country + "\n")

    return profiles

# dialog to create new profile
def newProfile() -> Profile:
    print("enter new profile name: ", end="")
    pname = input()
    print("enter first name: ", end="")
    fname = input()
    while not checkName(fname):
        print("it should only be letters, try again: ", end="")
        fname = input()
    print("enter last name: ", end="")
    lname = input()
    while not checkName(lname):
        print("it should only be letters, try again: ", end="")
        lname = input()
    print("enter pin: ", end="")
    pin = input()
    while not checkPin(pin):
        print("it should be 6-13 digits, try again: ", end="")
        pin = input()
    print("enter email: ", end="")
    email = input()
    while not checkEmail(email):
        print("not a valid email, try again: ", end="")
        email = input()
    print("enter country code: ", end="")
    country = input()
    while not checkCountry(country):
        print("it should be two capital letters, try again: ", end="")
        country = input()

    return Profile(pname, fname, lname, pin, email, country)

def checkProfiles(profiles: list):
    # error checking
    profiles.sort(key=lambda x: x.pname)
    for i in range(len(profiles)):
        # TODO: account for header row?
        if profiles[i].pname == "profile name":
            continue
        #     profiles.remove(profiles[i])
        # duplicate pnames
        if i < len(profiles)-1 and profiles[i].pname == profiles[i+1].pname:
            raise ValueError("bad csv -- duplicate profile name: " + profiles[i].pname)
        if not checkName(profiles[i].fname):
            raise ValueError("bad first name -- should only be letters: " + fname)
        if not checkName(profiles[i].lname):
            raise ValueError("bad last name -- should only be letters: " + lname)
        if not checkPin(profiles[i].pin):
            raise ValueError("bad pin -- should be 6-13 digits: " + pin)
        if not checkEmail(profiles[i].email):
            raise ValueError("bad email -- not valid: " + email)
        if not checkCountry(profiles[i].country):
            raise ValueError("bad country code -- should be ISO 3166-1 alpha-2: " + country)

def checkName(name: str):
    justLetters = re.compile(r'^[a-zA-Z]+$')
    return justLetters.match(name)
def checkPin(pin: str):
    sixToThirteenDigits = re.compile(r'^\d{6,13}$')
    return sixToThirteenDigits.match(pin)
def checkEmail(email: str):
    validEmail = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return validEmail.match(email)
def checkCountry(country: str):
    validCountryCode = re.compile(r'^[A-Z]{2}$')
    return validCountryCode.match(country)



# SEARCH STUFF -------------------------------------------------------------------------------------

class Search:
    def __init__(self, depStn, arrStn, depTime):
        self.depStn = depStn
        self.arrStn = arrStn
        self.depTime = depTime

def getSearch() -> Search:
    stnShorthands = {"py": "pyeongtaek",
                     "pyj": "pyeongtaekjije",
                     "su": "suwon",
                     "se": "seoul",
                     "yo": "yongsan",
                     "bu": "busan",
                     "da": "daegu" }

    print("where are you leaving from? ", end="")
    depStn = input()
    if depStn in stnShorthands:
        depStn = stnShorthands[depStn]
    print("where are you going? ", end="")
    arrStn = input()
    if arrStn in stnShorthands:
        arrStn = stnShorthands[arrStn]
    print("what day/time? (asap, mm/dd hh:mm) ", end="")
    depTime = datetime(1, 1, 1)
    while depTime.year == 1:
        depTimeIn = input()
        if depTimeIn == "asap":
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


# SITE NAV STUFF -----------------------------------------------------------------------------------

def main():

    with webdriver.Firefox(service=Service('/usr/bin/geckodriver')) as driver:
        # driver.get("https://www.letskorail.com/ebizbf/EbizbfForeign_pr16100.do?gubun=1")
        title = driver.title
        driver.implicitly_wait(1)

        # get profile
        profile = getProfile()

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

        if choice == "1":

            print("searching for trains from " + depStn + " to " + arrStn +
                  " on " + depTime.strftime("%m/%d") + " at " + depTime.strftime("%H:%M"))






        # keep window open
        while True:
            i = 1

if __name__ == "__main__":
    main()
