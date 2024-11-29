from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('trainer/', views.trainer_dashboard, name='trainer_dashboard'), 
    path('participant/', views.participant_dashboard, name='participant_dashboard'),
]