# korail-automator

## korail (south korea's national train service) has an annoying interface 
- doesnt remember repetitive info like name, email, stations, etc
- tickets sell out often, and when they become available, i can't enter info in quickly enough to purchase them

## my solution
- use python + selenium to maniuplate a browser to interact with the site
- read user data from file
- cli to:
  - choose user profile
  - get train times
  - book tickets (if sold out -> refresh/wait until available and quickly purchase)
  - view tickets already purchased
  - refund tickets
