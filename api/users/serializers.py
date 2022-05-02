import logging
from django.contrib.auth import get_user_model

from rest_framework import serializers

from api.schools.models import School
from api.users.models import Student
from api.users.utils.constants import MAX_STUDENT_ERROR_MESSAGE, SCHOOL_NOT_FOUND_ERROR_MESSAGE

logger = logging.getLogger('school_logger')

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    "User Serializer for user within Student Serializer"
    class Meta:
        fields = ['first_name', 'last_name', 'email']
        model = User
        extra_kwargs = {
            'email': {'validators': []},
        }



class SchoolStudentSerializer(serializers.ModelSerializer):
    "Serializer for adding school within Student Serializer"
    uuid = serializers.CharField(required=True)

    class Meta:
        fields = ['uuid', ]
        model = School


class StudentSerializer(serializers.ModelSerializer):
    "Serializer to serializer student model"
    age = serializers.CharField(source='student_age', required=False)
    school = SchoolStudentSerializer()
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ['id', 'student_id', 'location',
                  'nationality', 'gender', 'age',
                  'dob', 'school', 'user']
        read_only_fields = ['age', 'student_id']

    def validate(self, attrs):
        school_data = attrs.get('school')
        if not school_data:
            return super().validate(attrs)

        school_uuid = school_data.get('uuid')
        school = self._fetch_school_by_uuid(school_uuid)
        if not school:
            logger.error(f'{SCHOOL_NOT_FOUND_ERROR_MESSAGE} for school {school_uuid}')
            raise serializers.ValidationError(detail=f"{SCHOOL_NOT_FOUND_ERROR_MESSAGE} {school_uuid}")

        if not self._can_add_student(school):
            logger.error(f'{MAX_STUDENT_ERROR_MESSAGE} for school {school.id}')
            raise serializers.ValidationError(detail=MAX_STUDENT_ERROR_MESSAGE)

        attrs['school'] = school
        return super().validate(attrs)

    def _fetch_school_by_uuid(self, school_uuid):
        return School.objects.filter(uuid=school_uuid).first()

    def _can_add_student(self, school):
        student_count = school.school_students.count()
        if student_count == 0 or (student_count < school.max_student_count):
            return True

        return False

    def __update_or_create_user(self, validated_data):
        user_data = validated_data.pop('user', None)
        if not user_data:
            return None

        user_email = user_data.pop('email', None)
        user_data = dict(user_data)
        user, created = User.objects.update_or_create(email=user_email, defaults=user_data)
        return user
    
    def _check_user_email(self, email):
        if User.objects.filter(email=email).exists():
            logger.error(f'This email already exists {email}')
            raise serializers.ValidationError("This email already exists!.")
        return email
    
    def create(self, validated_data):
        self._check_user_email(validated_data.get('user').get('email'))
        user = self.__update_or_create_user(validated_data)
        if not user:
            return

        student = Student.objects.create(user=user, **validated_data)
        return student

    def update(self, instance, validated_data):
        user = self.__update_or_create_user(validated_data)
        if user:
            validated_data['user'] = user

        for field in validated_data:
            setattr(instance, field, validated_data.get(field))

        instance.save()
        return instance
