from rest_framework import serializers

from api.users.utils.choices import GENDER_CHOICES


class GenderField(serializers.Field):

    def to_representation(self, value):
        return value.get_gender_display()

    def to_internal_value(self, data):
        return {'gender': data}
