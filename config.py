from os import urandom, path

from vote.selection import weighted_sample


# Web Server
CSRF_ENABLED = True
SECRET_KEY = urandom(30)
PROPAGATE_EXCEPTIONS = True

# SQLAlchemy
basedir = path.abspath(path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(path.join(basedir, 'app.db'))

# LDAP
LDAP_URI = 'ldap://ec2-23-23-226-137.compute-1.amazonaws.com'
LDAP_SEARCH_BASE = 'ou=People,dc=invenia,dc=ca'

# Administrator
ADMIN_USERS = ['gem.newman']

# Voting
WINNERS = 5             # 5 options will be selected.
PREMIUM_LIMIT = 2       # No more than 2 "premium" options will be selected.
SELECTION = weighted_sample




# ADD THE FOLLOWING TO THE DATABASE
from collections import OrderedDict
OPTIONS = {
    "lunch": OrderedDict(
        [
            ("Japanese",
                [
                    "Asoyama Sushi",
                    "Kenko Niwa Japanese",
                    "Miso Japanese Restaurant",
                    "Sushi Gozen",
                    "Sushi Hon",
                    "Sushi Jet",
                    "Sura Suhi",
                    "Umi Sushi",
                    "Wasabi Sabi",
                ]),
            ("Indian",
                [
                    "Tandoor House",
                    "Water Lily",
                    "Clay Oven",
                    "Karahi of India",
                    "Dhoom Indian Restaurant",
                    "Sizzling Dhaba",
                ]),
            ("Chinese",
                [
                    "North Garden",
                    "Asia City",
                    "Szechuan Restaurant",
                ]),
            ("Other Asian",
                [
                    "Palatal Stir-Fry Express",
                    "Saigon Jon's Vietnamese Kitchen",
                    "Siam Thai",
                    "BIMI Korean/Japanese",
                    "Loha's Asian Restaurant",
                ]),
            ("Mexican",
                [
                    "Burrito Splendido",
                    "Taco del Mar",
                    "Vamos Tacos",
                    "Carlos & Murphy's",
                ]),
            ("Pizza & Italian",
                [
                    "Panago",
                    "Buccaccino's",
                    "Niccolinos",
                    "Boston Pizza",
                    "Carbone Coal Fired Pizza",
                    "Van Goes Pizza & Chicken",
                    "Garbonzo's Pizza",
                ]),
            ("Burgers & Sandwiches",
                [
                    "Nick's on Broadway",
                    "Flat Land Wrap",
                    "Falafel Place",
                    "Pita Pit",
                    "The Fyxx",
                    "Junior's",
                    "Myer's Delicatessen",
                ]),
            ("Cafes, Chalets, and Miscellany",
                [
                    "Desserts Plus",
                    "Good Eats",
                    "Saffron Restaurant",
                    "Osborne Village Cafe",
                    "Booster Juice",
                    "Joey's Only Seafood",
                    "Swiss Chalet",
                    "Stella's Cafe and Bakery",
                    "Prairie Ink Cafe",
                    "Confusion Corner Bar & Grill",
                    "Applebees",
                    "Tony Roma's",
                ]),
        ])
}

PREMIUM = {
    "game": {},
    "lunch": {
        "Asoyama Sushi",
        "Kenko Niwa Japanese",
        "Miso Japanese Restaurant",
        "Sushi Gozen",
        "Sushi Hon",
        "Sushi Jet",
        "Sura Suhi",
        "Umi Sushi",
        "Wasabi Sabi",
        "Water Lily",
        "Clay Oven",
        "Karahi of India",
        "Dhoom Indian Restaurant",
        "Sizzling Dhaba",
        "North Garden",
        "Asia City",
        "Szechuan Restaurant",
        "Carlos & Murphy's",
        "Boston Pizza",
        "Carbone Coal Fired Pizza",
        "Van Goes Pizza & Chicken",
        "Garbonzo's Pizza",
        "Prairie Ink Cafe",
        "Buccaccino's",
        "Niccolinos",
        "Confusion Corner Bar & Grill",
        "Applebees",
        "Tony Roma's",
    }
}
