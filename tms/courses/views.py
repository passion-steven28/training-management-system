from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from .models import Course, Material
from .forms import CourseForm, MaterialForm

CustomUser = get_user_model()


class CourseListView(ListView):
    model = Course
    template_name = "courses/course_list.html"
    context_object_name = "courses"
    ordering = ["-start_date"]


class CourseDetailView(DetailView):
    model = Course
    template_name = "courses/course_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/course_form.html"
    success_url = reverse_lazy("courses:course_list")

    def test_func(self):
        return self.request.user.user_type in ["admin", "trainer"]


@login_required
def enroll_course(request, pk):
    try:
        with transaction.atomic():
            course = get_object_or_404(Course, pk=pk)

            # Get user type safely
            user_type = getattr(request.user, "user_type", None)

            # Check if user has proper attributes
            if not hasattr(request.user, "user_type"):
                messages.error(
                    request, "Invalid user account type. Please contact administrator."
                )
                return redirect("courses:course_detail", pk=pk)

            # Prevent trainers from enrolling
            if user_type in ["admin", "trainer"]:
                messages.error(request, "Trainers cannot enroll in courses.")
                return redirect("courses:course_detail", pk=pk)

            if request.user not in course.participants.all():
                # Check capacity
                if course.participants.count() >= course.capacity:
                    messages.error(request, "This course is already full.")
                    return redirect("courses:course_detail", pk=pk)

                course.participants.add(request.user)
                messages.success(
                    request, f"You have successfully enrolled in {course.title}"
                )
            else:
                messages.info(request, "You are already enrolled in this course.")

    except AttributeError as e:
        messages.error(
            request, "User account configuration error. Please contact administrator."
        )
    except Exception as e:
        messages.error(request, f"Error enrolling in course: {str(e)}")

    return redirect("courses:course_detail", pk=pk)


@login_required
def add_material(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if request.method == "POST":
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.course = course
            material.save()
            return redirect("courses:course_detail", pk=course_pk)
    else:
        form = MaterialForm()
    return render(
        request, 
        "courses/material_form.html", 
        {"form": form, "course_pk": course_pk}
    )
