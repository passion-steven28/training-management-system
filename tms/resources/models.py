# models.py
from django.db import models
from django.urls import reverse
from accounts.models import CustomUser

class Venue(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)
    hourly_rate = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.capacity} capacity)"

    def get_absolute_url(self):
        return reverse('resources:venue_list')

class VenueBooking(models.Model):
    venue = models.ForeignKey(
        Venue, 
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    booked_by = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    purpose = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20, 
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected')
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)