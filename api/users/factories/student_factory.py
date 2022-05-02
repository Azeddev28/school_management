from factory.django import DjangoModelFactory
import factory

from api.schools.factories.school_factory import SchoolFactory
from api.users.factories.user_factory import UserFactory


class StudentFactory(DjangoModelFactory):
    class Meta:
        model = 'users.Student'
        django_get_or_create = ('user',) 
    
    user = factory.SubFactory(UserFactory)
    school = factory.SubFactory(SchoolFactory)
    dob = '2001-02-02'


