from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import service
from selenium.webdriver.firefox.service import Service

import csv

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
            if row[0] == "pname":
                continue
            for j in range(len(row)): 
                row[j] = row[j].strip()
            profiles.append(Profile(row[0], row[1], row[2], row[3], row[4], row[5]))
    
    # csv validation
    profiles.sort(key=lambda x: x.pname)
    for i in range(len(profiles)):
        if i < len(profiles)-1 and profiles[i].pname == profiles[i+1].pname:
            raise ValueError("bad csv -- duplicate profile name: " + profiles[i].pname)
        if profiles[i].fname 

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
