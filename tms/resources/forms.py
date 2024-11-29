from django import forms
from .models import Venue, VenueBooking

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = [
            'name',
            'location',
            'capacity',
            'hourly_rate',
            'notes',
            'is_available'
        ]

class VenueBookingForm(forms.ModelForm):
    class Meta:
        model = VenueBooking
        fields = ['venue', 'start_time', 'end_time', 'purpose']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }