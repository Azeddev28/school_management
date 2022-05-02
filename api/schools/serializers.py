from rest_framework import serializers

from api.schools.models import School


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name', 'max_student_count', 'uuid']
        read_only_fields = ['uuid']