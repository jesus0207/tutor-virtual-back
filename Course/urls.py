from django.urls import path
from .views import *

urlpatterns = [
    path('instructor/create', Create.as_view(), name='instructor_register'),
    path('instructor/list', ListOwnCourse.as_view(), name='instructor_list'),

    path('student/<int:pk>/chat', Chat.as_view(), name='chat'),
    path('student/list', List.as_view(), name='student_list')
]