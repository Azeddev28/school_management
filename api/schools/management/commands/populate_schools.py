import logging
from django.core.management.base import BaseCommand

from factory import create_batch

from api.schools.factories.school_factory import SchoolFactory
from api.schools.models import School

logger = logging.getLogger('school_logger')

class Command(BaseCommand):

    def handle(self, *args, **options):
        create_batch(School, 20, FACTORY_CLASS=SchoolFactory)
        logger.info('Schools added successfully')
