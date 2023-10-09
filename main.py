from selenium import webdriver
from selenium.webdriver.firefox.service import service
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.firefox.
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
# import javascript executor



import csv
import re
from datetime import datetime, timezone, timedelta
import time
import sys
import os
from os import path


# DIALOG STUFF ------------------------------------------------------------------------------------
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
                     "pyj": "pyeongtaek-jije",
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

# SITE NAV STUFF -----------------------------------------------------------------------------------

class Train:
    #TODO: add price?
    def __init__(self, train_nbr, train_type, dep_time, arr_time):
        self.number = train_nbr
        self.train_type = train_type
        self.dep_time = dep_time
        self.arr_time = arr_time

def showSchedule(driver, search, profile):
    driver.get("https://www.letskorail.com/ebizbf/EbizbfForeign_pr16100.do?gubun=1")

    # select departure date
    Select(driver.find_element(By.NAME, "selGoYear")).select_by_value(search.depTime.strftime("%Y"))
    Select(driver.find_element(By.NAME, "selGoMonth")).select_by_value(search.depTime.strftime("%m"))
    Select(driver.find_element(By.NAME, "selGoDay")).select_by_value(search.depTime.strftime("%d"))
    Select(driver.find_element(By.NAME, "selGoHour")).select_by_value(search.depTime.strftime("%H"))

    # select stations
    departure = driver.find_element(By.NAME, "txtGoStart")
    departure.clear()
    departure.send_keys(search.depStn)
    arrival = driver.find_element(By.NAME, "txtGoEnd")
    arrival.clear()
    arrival.send_keys(search.arrStn)

    # inquire button
    driver.find_element(By.XPATH, "//*[@id=\"resrv_info\"]/ul/li/a").click()

    # get train info
    trains = []
    for i in range(1, 11):
        try:
            train_nbr = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div[3]/form[1]/div[2]/table/tbody/tr[" + str(i) + "]/td[2]/a/span").get_attribute('innerHTML').strip()
            train_type = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div[3]/form[1]/div[2]/table/tbody/tr[" + str(i) + "]/td[3]").get_attribute('innerHTML').strip()
            dep_time = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div[3]/form[1]/div[2]/table/tbody/tr[" + str(i) + "]/td[6]").get_attribute('innerHTML').strip()
            arr_time = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div[3]/form[1]/div[2]/table/tbody/tr[" + str(i) + "]/td[7]").get_attribute('innerHTML').strip()
            trains.append(Train(train_nbr, train_type, dep_time, arr_time))
        except:
            break

    # print train info
    if (len(trains) == 0):
        print("no trains found")
        return trains
    else:
        print("next " + str(len(trains)) + " trains:")
        for i in range(len(trains)):
            print("%3d. %4s %11s %5s %5s" %
                  (i+1, trains[i].number, trains[i].train_type, trains[i].dep_time, trains[i].arr_time))

    return len(trains)


def selectTrain(numTrains):
    start, end = -1, -1

    # select train(s) -- TODO: needs a lot of refactoring
    print("select train (enter a number or a range): ", end="")
    while start == -1:
        choice = input().strip()
        # string is '-'
        if choice == "-":
            start = 0; end = numTrains-1
        # string is a number
        elif re.search(r'^\d+$', choice):
            choice = int(choice)
            if choice < 1 or choice > numTrains:
                print("should be a number b/w 1 and " + str(numTrains) + ", try again: ", end="")
            else:
                start = choice-1; end = start
        # string is -#
        elif re.search(r'^-\d+$', choice):
            choice = int(choice[1:])
            if choice < 1 or choice > numTrains:
                print("should be a number b/w 1 and " + str(numTrains) + ", try again: ", end="")
            else:
                start = 0; end = int(choice)-1
        # string is #-
        elif re.search(r'^\d+-$', choice):
            choice = int(choice[:-1])
            if choice < 1 or choice > numTrains:
                print("should be a number b/w 1 and " + str(numTrains) + ", try again: ", end="")
            else:
                start = choice-1; end = numTrains-1
        # string is #-#
        elif re.search(r'^\d+-\d+$', choice):
            choice = choice.split("-")
            choice = [int(i) for i in choice]
            if choice[0] > choice[1] or choice[0] < 1 or choice[1] > numTrains:
                print("should be a range b/w 1 and " + str(numTrains) + ", try again: ", end="")
            else:
                start = choice[0]-1; end = choice[1]-1
        else:
            print("should be a number or a range, try again: ", end="")

    print("start: " + str(start) + ", end: " + str(end))
    return start, end


def refresh(driver, indices):
    # refreshes and tries to book every option every 0.5 seconds
    while True:
        for i in range(indices[0], indices[1]+1):
            try:
                print("attempting to book train " + str(i+1))
                driver.find_element(By.NAME, "btnRsv1_" + str(i)).click()
                return
            except:
                pass
        driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div[3]/form[1]/p/a/img").click()
        


def bookTicket(driver, profile, indices):

    refresh(driver, indices)
    time.sleep(1)

    # name
    driver.find_element(By.NAME, "txtCustFirstNm").send_keys(profile.fname)
    driver.find_element(By.NAME, "txtCustLastNm").send_keys(profile.lname)
    # male
    driver.find_element(By.ID, "ipt_grb01").click()
    # pw, email, country
    driver.find_element(By.NAME, "txtCustPw").send_keys(profile.pin)
    driver.find_element(By.NAME, "txtCustPw2").send_keys(profile.pin)
    driver.find_element(By.NAME, "txtEmailAddr").send_keys(profile.email)
    Select(driver.find_element(By.NAME, "selNationCd")).select_by_value(profile.country)
    # agree checkbox
    driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div[3]/form/div[3]/b/input").click()
    # next button
    driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div[3]/form/b/p/a/img").click()
    # foreign card radio
    driver.find_element(By.XPATH, "//*[@id=\"ipt_rdpi01\"]").click()
    # next button
    driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/form/div/p[2]/a/img").click()



    driver.save_screenshot("/home/ser/media/image/screenshots/browser.png")
    print("screenshotted! :)")

    
def payTicket(driver, profile):
    # TODO: figure this shit out (elements are hidden / not open for interaction)

    time.sleep(5)
    # element = driver.find_element(By.XPATH, "//*[@id=\"all_agree\"]")
    # driver.execute_script("document.getElementByXpath(\"//*[@id=\"all_agree\"]\")".click())

def main():

    options = webdriver.FirefoxOptions()
    # os.environ['MOZ_HEADLESS'] = '1'
    with webdriver.Firefox(service=Service(executable_path='/usr/bin/geckodriver',
                                           log_output=os.path.devnull)) as driver:
        # driver.implicitly_wait(0.5)

        # get profile
        profile = getProfile()

        choice = getAction()
        search = getSearch()
        num_trains = showSchedule(driver, search, profile)
        indices = selectTrain(num_trains)
        bookTicket(driver, profile, indices)
        payTicket(driver, profile)

        # keep window open
        while True:
            i = 1

if __name__ == "__main__":
    main()
