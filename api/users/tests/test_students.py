from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from factory import create_batch

from api.users.factories.student_factory import StudentFactory
from api.schools.factories.school_factory import SchoolFactory
from api.users.models import Student
from api.users.factories.user_factory import UserFactory
from api.schools.models import School
from api.users.utils.factory_utils import get_unique_timestamp


class StudentModelViewSetTest(APITestCase):

    def setUp(self):
        self.total_students = 5
        create_batch(School, 20, FACTORY_CLASS=SchoolFactory)
        for count in range(0, 5):
            user = UserFactory(
                email=f"{get_unique_timestamp()}@gmail.com")
            school = School.objects.order_by('?').first()
            StudentFactory(user=user, school=school)
            self.student_url = reverse('students-list')

    def test_retrieve_students_list(self):
        response = self.client.get(self.student_url)
        self.assertEqual(response.status_code, HTTP_200_OK, "Couldn't fetch students")
        self.assertLessEqual(abs(len(response.data) - self.total_students), 1, "Didn't fetch all of the students")

    def get_student_payload(self):
        student_data = {
            "gender": "M",
            "location": "pakistan",
            "nationality": "Pakistani",
            "dob": "2001-02-02",
            "school": {
                "uuid": School.objects.order_by('?').first().uuid
            },
            "user": {
                "first_name": "Random",
                "last_name": "random",
                "email": "random@gmail.com"
            }
        }
        return student_data

    def test_create_student(self):
        response = self.client.post(
            self.student_url, self.get_student_payload(), format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED, "Couldn't create student")

    def test_patch_student(self):
        student_id = Student.objects.first().id
        response = self.client.patch(
            f'{self.student_url}{student_id}/', self.get_student_payload(), format='json')
        self.assertEqual(response.status_code, HTTP_200_OK, f"Couldn't partially update student with id {student_id}")

    def test_put_student(self):
        student_id = Student.objects.first().id
        response = self.client.put(
            f'{self.student_url}{student_id}/', self.get_student_payload(), format='json')
        self.assertEqual(response.status_code, HTTP_200_OK, f"Couldn't partially update student with id {student_id}")

    def test_delete_student(self):
        student_id = Student.objects.first().id
        response = self.client.delete(
            f'{self.student_url}{student_id}/', format='json')
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT, f"Couldn't delete student with id {student_id}")
