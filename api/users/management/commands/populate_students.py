from datetime import datetime
import time
from django.core.management.base import BaseCommand

from factory import create_batch
from api.schools.factories.school_factory import SchoolFactory
from api.schools.models import School

from api.users.factories.student_factory import StudentFactory
from api.users.factories.user_factory import UserFactory
from api.users.models import Student
from api.users.utils.constants import FACTORY_MAX_STUDENT_SIZE


class Command(BaseCommand):

    def get_unique_timestamp(self):
        time.sleep(1)
        return datetime.strftime(datetime.utcnow(), "%s")

    def handle(self, *args, **options):
        create_batch(School, 20, FACTORY_CLASS=SchoolFactory)
        for count in range(0, FACTORY_MAX_STUDENT_SIZE):
            user = UserFactory(email=f"{self.get_unique_timestamp()}@gmail.com")
            school = School.objects.order_by('?').first()
            StudentFactory(user=user, school=school)
