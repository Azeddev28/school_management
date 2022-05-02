from django.urls import path, include

from rest_framework import routers
from rest_framework_nested import routers as nested_routers

from api.schools.bindings import school_viewset
from api.users.bindings import student_viewset

school_router = routers.SimpleRouter()

school_router.register('', school_viewset, basename='schools')

student_router = nested_routers.NestedSimpleRouter(school_router, '', lookup='school')
student_router.register('students', student_viewset, basename='nested-students')

urlpatterns = [
    path('', include(school_router.urls)),
    path('', include(student_router.urls))
]