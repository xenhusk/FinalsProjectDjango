from django import forms
from .models import Student, Course

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['id_number','first_name', 'last_name', 'year_section', 'age', 'gender', 'email', 'courses']
        widgets = {
            'courses': forms.CheckboxSelectMultiple(),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'name', 'description', 'credits', 'is_active']

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()