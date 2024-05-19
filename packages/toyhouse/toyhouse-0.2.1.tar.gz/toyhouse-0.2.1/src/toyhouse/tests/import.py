# Reminders: Enter editable mode using
# py -m pip install -e .
# The dot shows that it's referring to the current file.

# Build using: 
# py -m build

# Upload using Command Prompt in the repository location and: 
# py -m twine upload --skip-existing dist/*
# where the username is __token__ and the password is the token value

import toyhouse
session = toyhouse.Session("ceruloryx", "Winterwatcher566")
session.auth()
other = (toyhouse.User(session, "blizzcatcher")).favs
me = (toyhouse.User(session, "ceruloryx")).chars

def user_comparison(m, u):
    li = [(mine[0], mine[2], yours[3]) for mine in m for yours in u if mine[1] == yours[1]]
    return li

def folder_filter(id, other):
    return([i for i in other if str(id) in i[3]])    

print(user_comparison(me, other))
