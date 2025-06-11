from django import forms
from .models import Student, Course

class StudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to show only active, non-archived courses
        self.fields['courses'].queryset = Course.objects.filter(is_active=True, is_archived=False)
        self.fields['courses'].widget.attrs.update({'class': 'form-check-input'})
        
    class Meta:
        model = Student
        fields = ['id_number','first_name', 'last_name', 'year_section', 'age', 'gender', 'email', 'courses']
        widgets = {
            'id_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter student ID'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'year_section': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 3-A'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '100'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
            'courses': forms.CheckboxSelectMultiple(),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'name', 'description', 'credits', 'is_active']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., CS101'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter course name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter course description'}),
            'credits': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '6'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'is_active': 'Course is currently active',
        }
        help_texts = {
            'credits': 'Number of credit hours for this course (1-6)',
            'code': 'Unique course code identifier',
        }

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv'}),
        help_text='Upload a CSV file with student or course data'
    )