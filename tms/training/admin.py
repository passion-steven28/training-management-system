from django.contrib import admin
from .models import Attendance, Evaluation, Session, PreAssessment, PostAssessment

# Register your models here.
admin.site.register(Session)
admin.site.register(Attendance)
admin.site.register(Evaluation)
admin.site.register(PreAssessment)
admin.site.register(PostAssessment)
