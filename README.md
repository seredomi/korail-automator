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
