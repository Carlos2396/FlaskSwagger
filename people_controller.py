from flask import make_response, abort
from config import db
from person import Person, PersonSchema


def read_all():
    # Create the list of people from our data
    people = Person.query.order_by(Person.lname).all()

    # Serialize the data for the response
    person_schema = PersonSchema(many=True)
    data = person_schema.dump(people).data
    return data


def read_one(person_id):
    # Get the person requested
    person = Person.query.filter(Person.person_id == person_id).one_or_none()

    if person is not None:

        # Serialize the data for the response
        person_schema = PersonSchema()
        data = person_schema.dump(person).data
        return data
    else:
        abort(404,"Person not found for Id: {person_id}".format(person_id=person_id))


def create(person):
    fname = person.get("fname")
    lname = person.get("lname")

    existing_person = Person.query.filter(Person.fname == fname).filter(Person.lname == lname).one_or_none()

    if existing_person is None:
        # Create a person instance using the schema and the passed in person
        schema = PersonSchema()
        new_person = schema.load(person, session=db.session).data

        # Add the person to the database
        db.session.add(new_person)
        db.session.commit()

        # Serialize and return the newly created person in the response
        data = schema.dump(new_person).data

        return data, 201
    else:
        abort(409, "Person {fname} {lname} exists already".format(fname=fname, lname=lname))


def update(person_id, person):
    # Get the person requested from the db into session
    update_person = Person.query.filter(Person.person_id == person_id).one_or_none()

    # Did we find a person?
    if update_person is not None:
        # turn the passed in person into a db object
        schema = PersonSchema()
        update = schema.load(person, session=db.session).data

        # Set the id to the person we want to update
        update.id = update_person.person_id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated person in the response
        data = schema.dump(update_person).data

        return data, 200
    else:
        abort(404, "Person not found for Id: {person_id}".format(person_id=person_id))


def delete(person_id):
    # Get the person requested
    person = Person.query.filter(Person.person_id == person_id).one_or_none()

    # Did we find a person?
    if person is not None:
        db.session.delete(person)
        db.session.commit()
        return make_response("Person {person_id} deleted".format(person_id=person_id), 200)
    else:
        abort(404, "Person not found for Id: {person_id}".format(person_id=person_id))