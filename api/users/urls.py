from django.urls import path

from rest_framework import routers

from api.users.bindings import student_viewset


user_router = routers.SimpleRouter()

user_router.register('students', student_viewset, basename='students')

urlpatterns = [
    # path('token/', auth_token_view, name='obtain-token'),
    # path('logout/', logout_view, name='logout'),
    # path('register/', register_view, name='register'),
    # path('user-details/', customer_details_view, name='user-details')
    # path('students/', student_viewset)
]
urlpatterns += user_router.urls