from django.contrib import admin
from .models import Student, Course

# Register models with the admin site
admin.site.register(Student)
admin.site.register(Course)
