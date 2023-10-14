# korail-automator

## korail has an annoying interface 
- doesnt remember repetitive info like name, email, stations, etc
- tickets sell out often, and when they become available, i get beat out by other purchasers

## my solution
- use python + selenium to maniuplate a browser to interact with the site
- read user data from file
- cli to:
  - choose user profile
  - get train times
  - book tickets (if sold out -> refresh/wait until available and quickly purchase)
  - view/refund tickets already purchased

## planned tui
main menu
- [s]earch
  - (autofill last query)
  - [k/j] move b/w queries
  - [d]eparting station
  - [a]rriving station
  - [h]our of departure
  - [enter] run query

  - [k/j] move b/w trains
  - [s]elect
  - [r]ange
  - [enter] try to book
      
- [c]heck
  - [p]rint
  - [r]efund
  - [k/j] move b/w tickets

- [p]rofiles
  - [s]elect
  - [e]dit
  - [d]elete
  - [a]dd
  - [k/j] move b/w profiles

[k/j] move b/w options
[esc] return to main menu at any time
