from factory.django import DjangoModelFactory
from datetime import datetime
import time

def get_unique_timestamp():
    return datetime.strftime(datetime.utcnow(), "%s")


class UserFactory(DjangoModelFactory):
    class Meta:
        model = 'users.User'

    email = f'{get_unique_timestamp()}random@gmail.com'
