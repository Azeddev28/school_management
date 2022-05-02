from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from api.schools.factories.school_factory import SchoolFactory
from factory import create_batch

from api.schools.models import School


class SchoolModelViewSetTest(APITestCase):

    def setUp(self):
        self.total_schools = 20
        create_batch(School, self.total_schools, FACTORY_CLASS=SchoolFactory)
        self.school_url = reverse('schools-list')

    def test_retrieve_school_list(self):
        response = self.client.get(self.school_url)
        self.assertEqual(response.status_code, HTTP_200_OK, "Couldn't fetch schools")
        self.assertLessEqual(abs(response.data.get('count') - self.total_schools), 1, "Didn't fetch all of the schools")

    def get_school_payload(self):
        school_data = {
            'name': 'DPS',
            'max_student_count': 10
        }
        return school_data

    def test_create_school(self):
        response = self.client.post(self.school_url, self.get_school_payload(), format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED, "Couldn't create school")

    def test_patch_school(self):
        school_id = School.objects.first().id
        response = self.client.patch(f'{self.school_url}{school_id}/', self.get_school_payload(), format='json')
        self.assertEqual(response.status_code, HTTP_200_OK, f"Couldn't partially update school with id {school_id}")

    def test_put_school(self):
        school_id = School.objects.first().id
        response = self.client.put(f'{self.school_url}{school_id}/', self.get_school_payload(), format='json')
        self.assertEqual(response.status_code, HTTP_200_OK, f"Couldn't partially update school with id {school_id}")


    def test_delete_school(self):
        school_id = School.objects.first().id
        response = self.client.delete(f'{self.school_url}{school_id}/', format='json')
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT, f"Couldn't delete school with id {school_id}")
