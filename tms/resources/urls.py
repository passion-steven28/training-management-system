from django.urls import path
from . import views

app_name = 'resources'

urlpatterns = [
    path('venues/', views.VenueListView.as_view(), name='venue_list'),
    path('venues/new/', views.VenueCreateView.as_view(), name='venue_create'),
    path('venues/book/', views.book_venue, name='book_venue'),
    path('venues/check-availability/', views.check_venue_availability, name='check_availability'),
]