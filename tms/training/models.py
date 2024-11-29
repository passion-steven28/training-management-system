from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import CustomUser
from courses.models import Course
from resources.models import Venue

class Session(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    duration = models.DurationField()
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True, blank=True)
    is_online = models.BooleanField(default=False)
    meeting_link = models.URLField(blank=True)
    trainer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    attendance_records = models.ManyToManyField(  # Renamed from attendance
        CustomUser, 
        through='Attendance', 
        related_name='attended_sessions'
    )

    def __str__(self):
        return f"{self.title} - {self.date.strftime('%Y-%m-%d')}"

class Attendance(models.Model):
    session = models.ForeignKey(
        Session, 
        on_delete=models.CASCADE,
        related_name='attendances'
    )
    participant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=False)
    check_in_time = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['session', 'participant']

class Evaluation(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    participant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    trainer_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['session', 'participant']

class PreAssessment(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    participant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    score = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

class PostAssessment(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    participant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    score = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)