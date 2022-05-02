from django.urls import path

from rest_framework import routers

from api.users.bindings import student_viewset


user_router = routers.SimpleRouter()

user_router.register('students', student_viewset, basename='students')

urlpatterns = []
urlpatterns += user_router.urls