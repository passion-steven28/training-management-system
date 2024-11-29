from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course_list'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('new/', views.CourseCreateView.as_view(), name='course_create'),
    path('<int:pk>/enroll/', views.enroll_course, name='course_enroll'),
    path('<int:course_pk>/add-material/', views.add_material, name='add_material'),
]