# Hospital Management System

A comprehensive web application for managing hospital operations, built with Flask, SQLite, and Bootstrap.

## Features

### Admin Functionalities
- Dashboard with statistics (total doctors, patients, appointments)
- Add/edit/delete doctor profiles
- View all appointments and patients
- Search for doctors and patients
- Manage hospital operations

### Doctor Functionalities
- View assigned appointments
- Add treatment records (diagnosis, prescription, notes)
- View patient history
- Update profile
- View list of patients

### Patient Functionalities
- Register and login
- Search doctors by specialization
- Book, reschedule, and cancel appointments
- View appointment history
- View treatment history
- Update profile

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Navigate to the project folder:
```bash
cd "hospital-management-system"
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the application:
```bash
python app.py
```

6. Open your browser and navigate to:
```
http://localhost:5000
```

## Default Login Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`

## Database

The application uses SQLite database which is created automatically on first run. No manual database setup is required.

## Project Structure

```
hospital-management-system/
├── app.py                 # Main application file
├── config.py             # Configuration settings
├── database.py           # Database initialization
├── requirements.txt      # Python dependencies
├── models/               # Database models
│   ├── __init__.py
│   ├── user.py
│   ├── doctor.py
│   ├── patient.py
│   ├── appointment.py
│   ├── treatment.py
│   └── department.py
├── routes/               # Application routes
│   ├── __init__.py
│   ├── auth.py          # Authentication routes
│   ├── admin.py         # Admin routes
│   ├── doctor.py        # Doctor routes
│   └── patient.py       # Patient routes
├── templates/            # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── index.html
│   ├── admin/
│   ├── doctor/
│   └── patient/
├── static/               # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
└── utils/                # Utility functions
    ├── __init__.py
    └── helpers.py
```

## API Endpoints

### Authentication
- `GET/POST /auth/login` - User login
- `GET/POST /auth/register` - Patient registration
- `GET /auth/logout` - User logout

### Admin Routes
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/doctors` - List all doctors
- `GET/POST /admin/add-doctor` - Add new doctor
- `GET /admin/patients` - List all patients
- `GET /admin/appointments` - List all appointments
- `GET/POST /admin/search` - Search doctors/patients

### Doctor Routes
- `GET /doctor/dashboard` - Doctor dashboard
- `GET /doctor/appointments` - View appointments
- `GET /doctor/patients` - View patients
- `GET/POST /doctor/treatment/<id>` - Add treatment record
- `GET/POST /doctor/profile` - Update profile

### Patient Routes
- `GET /patient/dashboard` - Patient dashboard
- `GET /patient/search-doctors` - Search doctors
- `GET/POST /patient/book-appointment/<id>` - Book appointment
- `GET /patient/my-appointments` - View appointments
- `GET /patient/treatment-history` - View treatment history
- `GET /patient/cancel-appointment/<id>` - Cancel appointment
- `GET/POST /patient/profile` - Update profile

## Technologies Used

- **Backend:** Flask 2.3.0, Flask-SQLAlchemy 3.0.0, Flask-Login 0.6.2
- **Database:** SQLite
- **Frontend:** HTML5, CSS3, Bootstrap 5
- **Python:** 3.8+

## Features Implemented

✅ User authentication with role-based access control
✅ Admin dashboard with statistics
✅ Doctor management
✅ Patient management
✅ Appointment booking system
✅ Treatment records
✅ Search functionality
✅ Profile management
✅ Responsive Bootstrap UI
✅ Automatic database creation
✅ Pre-configured admin account

## Security Features

- Password hashing with Werkzeug
- Session-based authentication with Flask-Login
- CSRF protection
- SQL injection prevention through ORM
- Role-based access control

## Notes

- The database (hospital.db) is created automatically on first run
- All tables are generated programmatically
- No manual database setup required
- The admin account is created automatically

## Support

For issues or questions, please refer to the project documentation or contact the development team.

---

**Version:** 1.0
**Last Updated:** November 2025
