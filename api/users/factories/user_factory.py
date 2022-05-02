from factory.django import DjangoModelFactory

from api.users.utils.factory_utils import get_unique_timestamp


class UserFactory(DjangoModelFactory):
    class Meta:
        model = 'users.User'

    email = f'{get_unique_timestamp()}random@gmail.com'
