import uuid
from django.db import models
from django.core.validators import MinValueValidator

from api.base_models import BaseModel
from api.schools.utils.constants import MINIMUM_STUDENT_COUNT


class School(BaseModel):
    name = models.CharField(max_length=20)
    max_student_count = models.IntegerField(validators=[
            MinValueValidator(MINIMUM_STUDENT_COUNT)
        ])
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
