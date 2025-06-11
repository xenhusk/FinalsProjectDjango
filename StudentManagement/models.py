from django.db import models
from django.utils import timezone

# Create your models here.

class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    credits = models.PositiveIntegerField(default=3)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.code} - {self.name}"
    
    class Meta:
        db_table = "Courses"

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    id_number = models.CharField(max_length=11, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    year_section = models.CharField(max_length=20, blank=True, null=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    courses = models.ManyToManyField(Course, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}>"
    
    class Meta:
        db_table = "Students"