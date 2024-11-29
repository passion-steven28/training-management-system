from django.contrib import admin
from .models import Venue, VenueBooking

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity', 'is_available', 'hourly_rate')
    # Remove any inlines related to venue_equipment
    # Example:
    # inlines = [EquipmentInline]  # Ensure EquipmentInline is correctly defined

admin.site.register(VenueBooking)
