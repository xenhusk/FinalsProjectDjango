from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.views.decorators.http import require_POST
import csv, io
import json

from .models import Student, Course
from .forms import StudentForm, CourseForm, CSVUploadForm

def index(request):
    # Calculate statistics for the homepage
    total_students = Student.objects.count()
    total_courses = Course.objects.count()
    active_students = Student.objects.filter(is_archived=False).count()
    active_courses = Course.objects.filter(is_archived=False).count()
    
    # Calculate enrollment rate (students with at least one course)
    enrolled_students = Student.objects.filter(courses__isnull=False, is_archived=False).distinct().count()
    enrollment_rate = round((enrolled_students / active_students * 100) if active_students > 0 else 0, 1)
    
    # Get latest activity (most recent student added)
    latest_student = Student.objects.filter(is_archived=False).order_by('-created_at').first()
    latest_activity = f"Student {latest_student.first_name} {latest_student.last_name} added" if latest_student else "No recent activity"
    
    context = {
        'total_students': total_students,
        'total_courses': active_courses,
        'active_students': active_students,
        'enrollment_rate': enrollment_rate,
        'latest_activity': latest_activity,
    }
    
    return render(request, 'StudentManagement/index.html', context)

# Student Views

def student_list(request):
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort_by', 'id_number')
    order = request.GET.get('order', 'asc')
    show_archived = request.GET.get('show_archived', '') == 'true'
    
    # Filter by archive status and search query
    if show_archived:
        students = Student.objects.all()
    else:
        students = Student.objects.filter(is_archived=False)
    if search_query:
        students = students.filter(
            Q(id_number__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(year_section__icontains=search_query)
        )
    
    # Apply sorting
    if order == 'desc':
        sort_field = f"-{sort_by}"
    else:
        sort_field = sort_by
    
    students = students.order_by(sort_field)
    
    # Pagination
    page_number = request.GET.get('page', 1)
    paginator = Paginator(students, 10)  # Show 10 students per page
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'sort_by': sort_by,
        'order': order,
        'total_count': paginator.count
    }
    return render(request, 'StudentManagement/student_list.html', context)

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully.')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'StudentManagement/student_form.html', {'form': form, 'title': 'Add Student', 'edit_mode': False})

def edit_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully.')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'StudentManagement/student_form.html', {'form': form, 'title': 'Edit Student', 'edit_mode': True})

def student_detail(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    return render(request, 'StudentManagement/student_detail.html', {'student': student})

def import_students(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            reader = csv.reader(io_string)
            header = next(reader, None)
            count = 0
            for row in reader:
                # Check for the minimum required columns
                # if len(row) >= 7:  # id_number, first_name, last_name, email, age, gender, year_section are minimum required
                    id_number = row[0].strip()
                    email = row[3].strip()
                    
                    # Check if student with this id_number or email already exists
                    if not Student.objects.filter(id_number=id_number).exists() and not Student.objects.filter(email=email).exists():
                        try:
                            age = int(row[4].strip())
                            gender = row[5].strip()
                            year_section = row[6].strip()
                            student = Student(
                                id_number=id_number,
                                first_name=row[1].strip(), 
                                last_name=row[2].strip(), 
                                email=email,
                                age=age,
                                gender=gender,
                                year_section=year_section
                            )
                            student.save()
                            if len(row) > 7: 
                                codes = [c.strip() for c in row[7].split(';') if c.strip()]
                                for code in codes:
                                    try:
                                        course = Course.objects.get(code=code)
                                        student.courses.add(course)
                                    except Course.DoesNotExist:
                                        continue
                            count += 1
                        except (ValueError, IndexError):
                            messages.warning(request, f'Skipped row with email {email}: Invalid data format')
                    else:
                        messages.info(request, f'Skipped row with email {email}: Already exists')
            messages.success(request, f'Imported {count} new students.')
            return redirect('student_list')
    else:
        form = CSVUploadForm()
    return render(request, 'StudentManagement/import.html', {'form': form, 'title': 'Import Students'})

def export_students(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'
    writer = csv.writer(response)
    writer.writerow(['id_number', 'first_name', 'last_name', 'email', 'age', 'gender', 'year_section', 'courses'])
    for student in Student.objects.all():
        codes = ';'.join([c.code for c in student.courses.all()])
        writer.writerow([
            student.id_number, 
            student.first_name, 
            student.last_name, 
            student.email, 
            student.age, 
            student.gender,
            student.year_section or '',
            codes
        ])
    return response

def delete_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        student.is_archived = True
        student.save()
        messages.success(request, f'Student {student.first_name} {student.last_name} archived successfully.')
        return redirect('student_list')
    return render(request, 'StudentManagement/confirm_delete.html', {'object': student, 'type': 'student', 'action': 'archive'})

def restore_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        student.is_archived = False
        student.save()
        messages.success(request, f'Student {student.first_name} {student.last_name} restored successfully.')
        return redirect('student_list')
    return render(request, 'StudentManagement/confirm_restore.html', {'object': student, 'type': 'student'})

# Course Views

def course_list(request):
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort_by', 'code')
    order = request.GET.get('order', 'asc')
    show_archived = request.GET.get('show_archived', '') == 'true'
    
    # Filter by archive status and search query
    if show_archived:
        courses = Course.objects.all()
    else:
        courses = Course.objects.filter(is_archived=False)
    if search_query:
        courses = courses.filter(
            Q(code__icontains=search_query) |
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Apply sorting
    if order == 'desc':
        sort_field = f"-{sort_by}"
    else:
        sort_field = sort_by
    
    courses = courses.order_by(sort_field)
    
    # Add enrollment counts
    courses = courses.annotate(enrollment_count=Count('student'))
    
    # Pagination
    page_number = request.GET.get('page', 1)
    paginator = Paginator(courses, 10)  # Show 10 courses per page
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'sort_by': sort_by,
        'order': order,
        'total_count': paginator.count
    }
    return render(request, 'StudentManagement/course_list.html', context)

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course added successfully.')
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'StudentManagement/course_form.html', {'form': form, 'title': 'Add Course', 'edit_mode': False})

def edit_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully.')
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'StudentManagement/course_form.html', {'form': form, 'title': 'Edit Course', 'edit_mode': True})

def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrolled_students = Student.objects.filter(courses=course)
    return render(request, 'StudentManagement/course_detail.html', {
        'course': course,
        'enrolled_students': enrolled_students
    })

def import_courses(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            reader = csv.reader(io_string)
            header = next(reader, None)
            count = 0
            for row in reader:
                if len(row) >= 3:  # code, name, description are minimum required
                    code = row[0].strip()
                    if not Course.objects.filter(code=code).exists():
                        try:
                            # Process name and description
                            name = row[1].strip()
                            description = row[2].strip() if len(row) > 2 else ''
                            
                            # Process credits - default to 3 if missing or invalid
                            credits = 3  # Default value
                            if len(row) > 3 and row[3].strip():
                                try:
                                    credits = int(row[3].strip())
                                except ValueError:
                                    pass  # Keep default if conversion fails
                            
                            # Handle is_active field - convert "Yes"/"No" to boolean
                            is_active = True  # Default to active
                            if len(row) > 4 and row[4].strip():
                                is_active_val = row[4].strip().lower()
                                is_active = (is_active_val == 'yes' or is_active_val == 'true' or is_active_val == '1')
                            
                            Course.objects.create(
                                code=code,
                                name=name,
                                description=description,
                                credits=credits,
                                is_active=is_active
                            )
                            count += 1
                        except Exception as e:
                            messages.warning(request, f'Skipped row with code {code}: {str(e)}')
                            messages.warning(request, f'Skipped row with code {code}: {str(e)}')
            messages.success(request, f'Imported {count} new courses.')
            return redirect('course_list')
    else:
        form = CSVUploadForm()
    return render(request, 'StudentManagement/import.html', {'form': form, 'title': 'Import Courses'})

def export_courses(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="courses.csv"'
    writer = csv.writer(response)
    writer.writerow(['code', 'name', 'description', 'credits', 'is_active'])
    for course in Course.objects.all():
        writer.writerow([
            course.code,
            course.name,
            course.description,
            course.credits,
            'Yes' if course.is_active else 'No'
        ])
    return response

def delete_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        course.is_archived = True
        course.save()
        messages.success(request, f'Course {course.name} archived successfully.')
        return redirect('course_list')
    return render(request, 'StudentManagement/confirm_delete.html', {'object': course, 'type': 'course', 'action': 'archive'})

def restore_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        course.is_archived = False
        course.save()
        messages.success(request, f'Course {course.name} restored successfully.')
        return redirect('course_list')
    return render(request, 'StudentManagement/confirm_restore.html', {'object': course, 'type': 'course'})

# Reports View
def reports(request):
    # Filter settings
    include_archived = request.GET.get('include_archived', '') == 'true'
    
    # Base queries with filtering
    students_query = Student.objects.all() if include_archived else Student.objects.filter(is_archived=False)
    courses_query = Course.objects.all() if include_archived else Course.objects.filter(is_archived=False)
    
    # Overall statistics
    total_students = students_query.count()
    active_students = students_query.filter(is_archived=False).count()
    archived_students = Student.objects.filter(is_archived=True).count()
    
    total_courses = courses_query.count()
    active_courses = courses_query.filter(is_archived=False).count()
    archived_courses = Course.objects.filter(is_archived=True).count()
      # Gender distribution
    gender_distribution = list(students_query.values('gender').annotate(count=Count('id')))
    
    # Course enrollment stats
    course_stats = courses_query.annotate(student_count=Count('student')).values('name', 'code', 'student_count').order_by('-student_count')[:10]
    
    # Year section distribution
    year_section_distribution = list(students_query.values('year_section').annotate(count=Count('id')))
    
    # Students by courses taken
    student_course_counts = []
    for i in range(1, 6):  # 1 to 5 courses
        count = students_query.annotate(course_count=Count('courses')).filter(course_count=i).count()
        student_course_counts.append({'count': i, 'students': count})
    
    # Recent activities - using created_at timestamps
    recent_students = students_query.order_by('-created_at')[:5]
    recent_courses = courses_query.order_by('-created_at')[:5]
    
    # Archive statistics
    archive_stats = {
        'students': {
            'active': active_students,
            'archived': archived_students,
            'total': total_students
        },
        'courses': {
            'active': active_courses,
            'archived': archived_courses,
            'total': total_courses
        }    }
    
    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'gender_distribution': json.dumps(gender_distribution),
        'course_stats': course_stats,
        'year_section_distribution': json.dumps(year_section_distribution),
        'student_course_counts': json.dumps(student_course_counts),
        'recent_students': recent_students,
        'recent_courses': recent_courses,
        'archive_stats': archive_stats,
        'include_archived': include_archived
    }
    
    return render(request, 'StudentManagement/reports.html', context)
