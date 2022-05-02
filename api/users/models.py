import uuid
from datetime import date
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django.contrib.auth.models import UnicodeUsernameValidator
from django.contrib.auth.models import  PermissionsMixin

from api.base_models import BaseModel
from api.schools.models import School
from api.users.managers import UserManager
from api.users.utils.choices import GENDER_CHOICES


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Email, uuid and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator()

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    email = models.CharField(
        _('email'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator, validate_email],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    last_active = models.DateTimeField(_('last_active'), null=True, blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    objects = UserManager()

    USERNAME_FIELD = EMAIL_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Student(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    student_id = models.UUIDField(default=uuid.uuid4, editable=False)
    location = models.CharField(max_length=50)
    nationality = models.CharField(max_length=30)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    dob = models.DateField()
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='school_students')

    @property
    def student_age(self):
        current_date = date.today()
        return (current_date.year - self.dob.year)
    
    def __str__(self):
        return self.user.full_name