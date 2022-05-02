from factory.django import DjangoModelFactory


class SchoolFactory(DjangoModelFactory):
    class Meta:
        model = 'schools.School'

    max_student_count = 30
