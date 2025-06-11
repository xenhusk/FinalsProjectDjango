# Student Management System

A comprehensive Django-based web application for educational institutions to manage students and courses with advanced features.

![Django](https://img.shields.io/badge/Django-5.2.3-green.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-latest-blue.svg)

## 🌟 Features

- **Student Management**
  - Create, view, update, and archive student records
  - Detailed student profiles with academic information
  - Bulk import students from CSV files

- **Course Management**
  - Create, view, update, and archive courses
  - Track course credits, descriptions, and other details
  - Bulk import courses from CSV files

- **Advanced UI Features**
  - Responsive navigation bar
  - Search functionality for both students and courses
  - Pagination for better performance with large datasets
  - Column sorting for all relevant fields
  - Filter views to show/hide archived items

- **Reporting & Statistics**
  - Comprehensive dashboard with key metrics
  - Data visualization charts
  - Toggle options to include/exclude archived items from statistics

- **Data Preservation**
  - Archive instead of delete functionality
  - Restore capability for archived records
  - Visual indicators for archived items

## 📋 Prerequisites

- Python 3.12 or higher
- PostgreSQL database
- pip (Python package manager)

## 🛠️ Installation

1. **Clone the repository**
   ```powershell
   git clone https://github.com/xenhusk/FinalsProjectDjango.git
   cd FinalsProjectDjango
   ```

2. **Create and activate a virtual environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the project root with the following variables:
   ```
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=StudentManagement
   DB_USER=yourusername
   DB_PASSWORD=yourpassword
   DB_HOST=localhost
   DB_PORT=5432
   SECRET_KEY=your-secret-key
   ```

5. **Run migrations**
   ```powershell
   python manage.py migrate
   ```

6. **Create a superuser**
   ```powershell
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```powershell
   python manage.py runserver
   ```

8. **Access the application**
   - Open your browser and navigate to http://localhost:8000/
   - Admin interface is available at http://localhost:8000/admin/

## 📤 Importing Sample Data

The system supports importing student and course data via CSV files:

1. Navigate to the import page
2. Choose either student or course import
3. Upload a CSV file with the correct format:
   - **Students**: First Name, Last Name, Email, Student ID, Year/Section
   - **Courses**: Course Code, Title, Description, Credits

Example CSV files are included in the repository (`students.csv` and `courses.csv`).

## 🖥️ System Architecture

- **Backend**: Django 5.2.3, Python 3.12
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Environment Management**: python-dotenv

## 📁 Project Structure

- **StudentManagement/** - Core application with models, views, and forms
- **templates/** - HTML templates for all views
- **finalsproject/** - Project settings and URL configuration
- **.env** - Environment variables (not committed to the repository)

## 📊 Data Models

### Student Model
- First name and last name
- Email address
- Student ID
- Year/Section
- Archive status
- Timestamps (created_at, updated_at)

### Course Model
- Course code
- Title
- Description
- Credits
- Archive status
- Timestamps (created_at, updated_at)

## 🔒 Security Features

- Database credentials stored in environment variables
- Django's built-in CSRF protection
- Form validation to prevent malicious data input
- Secure sensitive information handling

## 🛣️ Future Enhancements

- User authentication and role-based access control
- Student enrollment in courses
- Grade tracking and reporting
- API endpoints for integration with other systems
- Email notifications for important events
- Calendar integration for course schedules

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contributors

- Your Name

## 📧 Contact

For questions or support, please contact: your.email@example.com
