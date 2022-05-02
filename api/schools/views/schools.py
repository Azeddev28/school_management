from api.base_views import BaseModelViewset

from api.schools.models import School
from api.schools.serializers import SchoolSerializer


class SchoolModelViewset(BaseModelViewset):
    serializer_class = SchoolSerializer
    queryset = School.objects.all()
    search_fields = ['name', 'max_student_count']
