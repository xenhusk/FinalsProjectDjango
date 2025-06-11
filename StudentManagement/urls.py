from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.index, name='index'),
    
    # Student routes
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/detail/<int:student_id>/', views.student_detail, name='student_detail'),
    path('students/edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('students/delete/<int:student_id>/', views.delete_student, name='delete_student'),
    path('students/restore/<int:student_id>/', views.restore_student, name='restore_student'),
    path('students/import/', views.import_students, name='import_students'),
    path('students/export/', views.export_students, name='export_students'),
    
    # Course routes
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/detail/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/edit/<int:course_id>/', views.edit_course, name='edit_course'),
    path('courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),
    path('courses/restore/<int:course_id>/', views.restore_course, name='restore_course'),
    path('courses/import/', views.import_courses, name='import_courses'),
    path('courses/export/', views.export_courses, name='export_courses'),
    
    # Reports
    path('reports/', views.reports, name='reports'),
]
