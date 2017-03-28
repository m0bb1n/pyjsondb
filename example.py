import jsondb
import os

filename = "users.jsondb"

db = jsondb.DB(filename)

def setup():
    user_table = jsondb.Table("user", ["username", "gender", "color"])
    db.add_table(user_table)
    db.save()

def populate():
    db.tables["user"].insert({"username": "Joe123", "gender":"m", "color": "red"})
    db.tables["user"].insert({"username": "MaySpring", "gender":"f", "color": "green"})
    db.tables["user"].insert({"username": "GregTheChoosenOne", "gender":"m", "color": "blue"})
    db.tables["user"].insert({"username": "Jason", "gender":"m", "color":"yellow"})

    db.save()

if __name__ == "__main__":
    if (not os.path.isfile(filename)):
        setup()
        populate()

    print db.tables["user"].find_models({"gender":"f"})

