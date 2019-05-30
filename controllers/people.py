
"""
This is the people module and supports all the ReST actions for the
PEOPLE collection
"""

# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# Data to serve with our API
PEOPLE = {
    "Farrell": {
        "fname": "Doug",
        "lname": "Farrell",
        "timestamp": get_timestamp(),
    },
    "Brockman": {
        "fname": "Kent",
        "lname": "Brockman",
        "timestamp": get_timestamp(),
    },
    "Easter": {
        "fname": "Bunny",
        "lname": "Easter",
        "timestamp": get_timestamp(),
    },
}

"""
This function responds to a request for /api/people
with the complete lists of people
:return:        json string of list of people
"""
def read_all():
    # Create the list of people from our data
    return [PEOPLE[key] for key in sorted(PEOPLE.keys())]

"""
This function responds to a request for /api/people/{lname}
with one matching person from people
:param lname:   last name of person to find
:return:        person matching last name
"""
def read_one(lname):
    # Does the person exist in people?
    if lname in PEOPLE:
        person = PEOPLE.get(lname)
    else:
        abort(404, "Person with last name {lname} not found".format(lname=lname))

    return person

"""
This function creates a new person in the people structure
based on the passed in person data
:param person:  person to create in people structure
:return:        201 on success, 406 on person exists
"""
def create(person):
    lname = person.get("lname", None)
    fname = person.get("fname", None)

    # Does the person exist already?
    if lname not in PEOPLE and lname is not None:
        PEOPLE[lname] = {
            "lname": lname,
            "fname": fname,
            "timestamp": get_timestamp(),
        }

        return make_response("{lname} successfully created".format(lname=lname), 201)
    else:
        abort(406, "Peron with last name {lname} already exists".format(lname=lname))


"""
This function updates an existing person in the people structure
:param lname:   last name of person to update in the people structure
:param person:  person to update
:return:        updated person structure
"""
def update(lname, person):
    # Does the person exist in people?
    if lname in PEOPLE:
        PEOPLE[lname]["fname"] = person.get("fname")
        PEOPLE[lname]["timestamp"] = get_timestamp()

        return PEOPLE[lname]
    else:
        abort(404, "Person with last name {lname} not found".format(lname=lname))

"""
This function deletes a person from the people structure
:param lname:   last name of person to delete
:return:        200 on successful delete, 404 if not found
"""
def delete(lname):
    # Does the person to delete exist?
    if lname in PEOPLE:
        del PEOPLE[lname]
        return make_response("{lname} successfully deleted".format(lname=lname), 200)
    else:
        abort(404, "Person with last name {lname} not found".format(lname=lname))