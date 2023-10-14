import constants as c
from search import Search

import os
from os import path
import re

from selenium import webdriver
from selenium.webdriver.firefox.service import service
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

class Train:
    #TODO: add price?
    def __init__(self, train_nbr, train_type, dep_time, arr_time):
        self.number = train_nbr
        self.train_type = train_type
        self.dep_time = dep_time
        self.arr_time = arr_time

def startBrowser():
    return webdriver.Firefox(service=Service(executable_path=c.GECKO_DRIVER_PATH,
                                             log_output=os.path.devnull))


def showSchedule(driver, search, profile):
    options = webdriver.FirefoxOptions()
    # os.environ['MOZ_HEADLESS'] = '1'
    with webdriver.Firefox(service=Service(executable_path=c.GECKO_DRIVER_PATH,
                                           log_output=os.path.devnull)) as driver:

        driver.get(c.BOOK_URL)

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
                print("should be a number in range 1-" + str(numTrains) + ", try again: ", end="")
            else:
                start = choice-1; end = start
        # string is -#
        elif re.search(r'^-\d+$', choice):
            choice = int(choice[1:])
            if choice < 1 or choice > numTrains:
                print("should be a number in range 1-" + str(numTrains) + ", try again: ", end="")
            else:
                start = 0; end = int(choice)-1
        # string is #-
        elif re.search(r'^\d+-$', choice):
            choice = int(choice[:-1])
            if choice < 1 or choice > numTrains:
                print("should be a number in range 1-" + str(numTrains) + ", try again: ", end="")
            else:
                start = choice-1; end = numTrains-1
        # string is #-#
        elif re.search(r'^\d+-\d+$', choice):
            choice = choice.split("-")
            choice = [int(i) for i in choice]
            if choice[0] > choice[1] or choice[0] < 1 or choice[1] > numTrains:
                print("should be in range 1-" + str(numTrains) + ", try again: ", end="")
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
