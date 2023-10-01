from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import service
from selenium.webdriver.firefox.service import Service

import csv
import re

class Profile:
    def __init__(self, pname, fname, lname, pin, email, country):
        self.pname = pname
        self.fname = fname
        self.lname = lname
        self.pin = pin
        self.email = email
        self.country = country
         

# read filename, return dict of profiles
# needs error checking
def getProfiles() -> list:

    filename = "./user-info.csv"
    profiles = list()

    with open(filename, newline='') as csvfile:
        profilereader = csv.reader(csvfile)
        for row in profilereader:
            if len(row) != 6:
                raise ValueError("bad csv -- should be 6 fields in row: " + str(row))
            if row[0] == "pname":
                continue
            for j in range(len(row)): 
                row[j] = row[j].strip()
            profiles.append(Profile(row[0], row[1], row[2], row[3], row[4], row[5]))
    
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
        # fname/lname not just letters
        justLetters = re.compile(r'^[a-zA-Z]+$')
        if not justLetters.match(profiles[i].fname):
            raise ValueError("bad csv -- should only be letters in first name: " + profiles[i].fname)
        if not justLetters.match(profiles[i].lname):
            raise ValueError("bad csv -- should only be letters in last name: " + profiles[i].lname)
        # pin not 6-13 digits
        sixToThirteenDigits = re.compile(r'^\d{6,13}$')
        if not sixToThirteenDigits.match(profiles[i].pin):
            raise ValueError("bad csv -- pin should be 6-13 digits: " + profiles[i].pin)
        # email not valid
        validEmail = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not validEmail.match(profiles[i].email):
            raise ValueError("bad csv -- email not valid: " + profiles[i].email)
        # country code not valid
        validCountryCode = re.compile(r'^[A-Z]{2}$')
        if not validCountryCode.match(profiles[i].country):
            raise ValueError("bad csv -- country code should be ISO 3166-1 alpha-2: "
                             + profiles[i].country)

    return profiles




def main():

    with webdriver.Firefox(service=Service('/usr/bin/geckodriver')) as driver:
        # driver.get("https://www.letskorail.com/ebizbf/EbizbfForeign_pr16100.do?gubun=1")
        title = driver.title
        driver.implicitly_wait(1)

        profiles = getProfiles()
        print("choose your profile. enter:")
        for i in range(len(profiles)):
            print("  " + str(i+1) + " for " + profiles[i].pname)

        # for profile in profiles:
        #     print(profiles[profile].pname + " " + profiles[profile].fname + " " + profiles[profile].lname + " " + profiles[profile].pin + " " + profiles[profile].email + " " + profiles[profile].country)

        while(True):
            i = 1

if __name__ == "__main__":
    main()
