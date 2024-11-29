from django.db import models
from accounts.models import CustomUser

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=200)
    cover_image = models.ImageField(
        upload_to='course_covers/', 
        null=True, 
        blank=True,
        default='course_covers/default.jpg'
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    capacity = models.IntegerField()
    is_online = models.BooleanField(default=False)
    trainers = models.ManyToManyField(CustomUser, related_name='courses_training')
    participants = models.ManyToManyField(CustomUser, related_name='courses_enrolled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Material(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='materials/')
    upload_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.course.title}"