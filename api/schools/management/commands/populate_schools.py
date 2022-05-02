from django.core.management.base import BaseCommand

from factory import create_batch

from api.schools.factories.school_factory import SchoolFactory
from api.schools.models import School


class Command(BaseCommand):

    def handle(self, *args, **options):
        create_batch(School, 20, FACTORY_CLASS=SchoolFactory)
