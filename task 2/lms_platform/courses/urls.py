from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('upload/', views.upload_course, name='upload_course'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('<int:course_id>/progress/', views.track_progress, name='track_progress'),
    path('<int:course_id>/quiz/', views.take_quiz, name='take_quiz'),
]
