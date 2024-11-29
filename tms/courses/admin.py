from django.contrib import admin
from .models import Course, Category, Material

# Register your models here.
admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Material)