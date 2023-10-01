# korail-automator

## korail (south korea's train service) has some issues
- annoying interface
- doesnt remember repetitive info like name, email, stations, etc
- tickets sell out often

## my solution
- use python + selenium to maniuplate a browser to interact with the site
- read user data from file
- cli to:
  - choose user profile
  - get train times
  - book tickets (if sold out -> refresh/wait until available)
  - view tickets already purchased
