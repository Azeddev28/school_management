from api.base_views import BaseModelViewset
from api.users.models import Student
from api.users.serializers import StudentSerializer


class StudentsModelViewset(BaseModelViewset):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    search_fields = ['location', 'gender', 'nationality']
