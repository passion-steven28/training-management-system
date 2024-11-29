from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from .models import Venue, VenueBooking
from .forms import VenueForm, VenueBookingForm

class VenueListView(ListView):
    model = Venue
    template_name = 'resources/venue_list.html'
    context_object_name = 'venues'

class VenueCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Venue
    form_class = VenueForm
    template_name = 'resources/venue_form.html'
    success_url = reverse_lazy('resources:venue_list')

    def test_func(self):
        return self.request.user.user_type == 'admin'

    def form_valid(self, form):
        try:
            form.instance.is_available = True  # Set default value
            self.object = form.save()
            messages.success(self.request, 'Venue created successfully.')
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f'Error creating venue: {str(e)}')
            return self.form_invalid(form)

def check_venue_availability(request):
    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        venue_id = request.POST.get('venue_id')
        
        conflicting_bookings = VenueBooking.objects.filter(
            venue_id=venue_id,
            start_time__lt=end_time,
            end_time__gt=start_time,
            status='approved'
        )
        
        return JsonResponse({'available': not conflicting_bookings.exists()})

def book_venue(request):
    if request.method == 'POST':
        form = VenueBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.booked_by = request.user
            booking.status = 'pending'
            
            # Check availability
            conflicting_bookings = VenueBooking.objects.filter(
                venue=booking.venue,
                start_time__lt=booking.end_time,
                end_time__gt=booking.start_time,
                status='approved'
            )
            
            if conflicting_bookings.exists():
                messages.error(request, 'Venue is not available for selected time period')
                return redirect('resources:venue_list')
                
            booking.save()
            messages.success(request, 'Booking request submitted successfully')
            return redirect('resources:booking_detail', pk=booking.pk)
    else:
        form = VenueBookingForm()
    
    return render(request, 'resources/booking_form.html', {'form': form})

from django.db import models