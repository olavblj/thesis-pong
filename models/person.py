import requests

from config import URL
from utils.prints import Print


class Person:
    def __init__(self, id, name, gender, age, **kwargs):
        self.id = id
        self.name = name
        self.gender = gender
        self.age = age

    def __str__(self):
        return "{} ({}{})".format(self.name, self.gender[0], self.age)

    @classmethod
    def create_or_fetch(cls, name, age, gender):
        url = URL.persons

        r = requests.post(url, data=dict(name=name, age=age, gender=gender))
        json_resp = r.json()

        person = cls(**json_resp)

        if r.status_code == 201:
            Print.api("Created New Person: {})".format(person))
        elif r.status_code == 200:
            Print.api("Fetched Existing Person: {}".format(person))

        return person
