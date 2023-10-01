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
  - book tickets (wait and refresh until available if sold out)
  - get tickets that are currently purchased
