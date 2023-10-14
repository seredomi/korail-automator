import csv
import re

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
