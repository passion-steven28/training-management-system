from django.urls import path
from . import views

app_name = 'training'

urlpatterns = [
    path('sessions/', views.SessionListView.as_view(), name='session_list'),
    path('sessions/new/', views.SessionCreateView.as_view(), name='session_create'),
    path('sessions/<int:session_id>/attendance/', views.mark_attendance, name='mark_attendance'),
    path('sessions/<int:session_id>/evaluate/', views.submit_evaluation, name='submit_evaluation'),
    path('sessions/<int:pk>/', views.SessionDetailView.as_view(), name='session_detail'),
]