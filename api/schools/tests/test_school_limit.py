from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from api.schools.factories.school_factory import SchoolFactory
from api.users.utils.factory_utils import get_unique_timestamp
from api.schools.models import School


class SchoolModelViewSetTest(APITestCase):

    MAX_STUDENTS = 2

    def setUp(self):
        SchoolFactory(max_student_count=self.MAX_STUDENTS)
        self.school_url = reverse('schools-list')
        self.student_url = reverse('students-list')

    def get_student_payload(self):
        student_data = {
            "gender": "M",
            "location": "pakistan",
            "nationality": "Pakistani",
            "dob": "2001-02-02",
            "school": {
                "uuid": School.objects.first().uuid
            },
            "user": {
                "first_name": "Random",
                "last_name": "random",
                "email": f"{get_unique_timestamp()}@gmail.com"
            }
        }
        return student_data
 
    def test_add_max_students(self):
        for count in range(0, self.MAX_STUDENTS):
            print(count)
            response = self.client.post(self.student_url, self.get_student_payload(), format='json')
            self.assertEqual(response.status_code, HTTP_201_CREATED, "Couldn't create student")

        response = self.client.post(self.student_url, self.get_student_payload(), format='json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST, "Couldn't create student")
