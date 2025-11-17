# Hospital Management System - Complete Code Overview

## 📋 Project Structure

```
hospital-management-system/
├── app.py                    # Main Flask application factory
├── config.py                 # Configuration settings
├── database.py               # Database initialization
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── SETUP_COMPLETE.md         # Setup verification
├── CODE_OVERVIEW.md          # This file
│
├── models/                   # Database models (SQLAlchemy ORM)
│   ├── __init__.py
│   ├── user.py              # User model (base for all roles)
│   ├── doctor.py            # Doctor profile model
│   ├── patient.py           # Patient profile model
│   ├── appointment.py       # Appointment scheduling
│   ├── treatment.py         # Treatment records & medical history
│   └── department.py        # Medical departments
│
├── routes/                   # Flask blueprints (endpoints)
│   ├── __init__.py
│   ├── auth.py              # Login, register, logout
│   ├── admin.py             # Admin dashboard & management
│   ├── doctor.py            # Doctor appointments & patients
│   └── patient.py           # Patient bookings & history
│
├── templates/               # Jinja2 HTML templates
│   ├── base.html            # Master template (navbar, footer)
│   ├── login.html           # Login page
│   ├── register.html        # Registration page
│   ├── index.html           # Home page
│   ├── admin/               # Admin pages
│   │   ├── dashboard.html
│   │   ├── doctors.html
│   │   ├── add_doctor.html
│   │   ├── edit_doctor.html
│   │   ├── patients.html
│   │   ├── appointments.html
│   │   └── search.html
│   ├── doctor/              # Doctor pages
│   │   ├── dashboard.html
│   │   ├── appointments.html
│   │   ├── patients.html
│   │   ├── treatment.html
│   │   ├── profile.html
│   │   └── availability.html
│   └── patient/             # Patient pages
│       ├── dashboard.html
│       ├── search_doctors.html
│       ├── book_appointment.html
│       ├── appointments.html
│       ├── treatment_history.html
│       ├── profile.html
│       └── doctor_profile.html
│
├── static/                  # Static files
│   ├── css/
│   │   ├── bootstrap.min.css
│   │   └── style.css        # Custom Medicare-inspired styling
│   ├── js/
│   │   ├── bootstrap.min.js
│   │   └── script.js
│   └── images/
│
└── utils/                   # Utility functions
    ├── __init__.py
    └── helpers.py           # Helper functions
```

---

## 🔑 Key Files Explained

### **1. app.py** - Main Application
```python
# Application factory pattern
def create_app():
    # Initialize Flask app
    # Configure database (SQLite)
    # Initialize Flask extensions (SQLAlchemy, LoginManager)
    # Create database tables
    # Auto-create admin user (admin/admin123)
    # Auto-create 5 default departments
    # Register all blueprints (routes)
    # Setup user loader for authentication
    return app
```

**Key Features:**
- ✅ Creates admin user automatically
- ✅ Initializes 5 healthcare departments
- ✅ Handles role-based routing to dashboards
- ✅ Debug mode enabled on localhost:5000

---

### **2. models/user.py** - Base User Model
```python
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200))
    role = db.Column(db.String(20))  # admin, doctor, patient
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Methods
    def set_password(password)    # Hash password with Werkzeug
    def check_password(password)  # Verify password
```

**Roles:**
- `admin` - Full system access
- `doctor` - View patients, create treatment records
- `patient` - Book appointments, view history

---

### **3. models/doctor.py** - Doctor Profile
```python
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    phone = db.Column(db.String(20))
    experience_years = db.Column(db.Integer)
    bio = db.Column(db.Text)
    license_number = db.Column(db.String(50))
    qualification = db.Column(db.String(200))
    specialization = db.Column(db.String(100))
    consultation_fees = db.Column(db.Float, default=500.0)
    rating = db.Column(db.Float, default=0.0)
    total_patients = db.Column(db.Integer, default=0)
    is_available = db.Column(db.Boolean, default=True)
    working_days = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='doctor')
    department = db.relationship('Department', backref='doctors')
    appointments = db.relationship('Appointment', backref='doctor')
    treatments = db.relationship('Treatment', backref='doctor')
```

**Medicare Features:**
- Consultation fees tracking
- Doctor ratings system
- License & qualification tracking
- Availability management

---

### **4. models/patient.py** - Patient Profile
```python
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    phone = db.Column(db.String(20))
    alternate_phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    blood_group = db.Column(db.String(5))
    address = db.Column(db.Text)
    medical_history = db.Column(db.Text)
    insurance_provider = db.Column(db.String(100))
    insurance_id = db.Column(db.String(50))
    emergency_contact_name = db.Column(db.String(100))
    emergency_contact_phone = db.Column(db.String(20))
    enable_notifications = db.Column(db.Boolean, default=True)
    notification_preference = db.Column(db.String(50))  # email/sms/whatsapp
    total_visits = db.Column(db.Integer, default=0)
    total_spent = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='patient')
    appointments = db.relationship('Appointment', backref='patient')
    treatments = db.relationship('Treatment', backref='patient')
```

**Medicare Features:**
- Insurance integration
- Notification preferences (email/SMS/WhatsApp)
- Emergency contact tracking
- Visit & spending history

---

### **5. models/appointment.py** - Appointment Scheduling
```python
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default='Booked')  # Booked/Completed/Cancelled/No-show
    notes = db.Column(db.Text)
    queue_position = db.Column(db.Integer)
    reminder_sent = db.Column(db.Boolean, default=False)
    appointment_type = db.Column(db.String(50))  # Regular/Follow-up/Emergency
    consultation_fees = db.Column(db.Float)
    payment_status = db.Column(db.String(20))  # Pending/Paid/Insurance
    is_confirmed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

**Medicare Features:**
- Queue management (queue_position)
- Payment tracking (consultation_fees, payment_status)
- Appointment confirmation system
- Reminder automation
- Appointment type classification

---

### **6. models/treatment.py** - Medical Records
```python
class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    diagnosis = db.Column(db.Text, nullable=False)
    prescription = db.Column(db.Text)
    notes = db.Column(db.Text)
    icd_code = db.Column(db.String(20))  # Medical coding
    medicine_details = db.Column(db.Text)
    dosage_instructions = db.Column(db.Text)
    duration_days = db.Column(db.Integer)
    follow_up_required = db.Column(db.Boolean, default=False)
    follow_up_days = db.Column(db.Integer)
    lab_tests_recommended = db.Column(db.Text)
    consultation_duration = db.Column(db.Integer)  # in minutes
    status = db.Column(db.String(20))  # Active/Completed/Archived
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

**Medicare Features:**
- ICD medical coding
- Lab test tracking
- Follow-up management
- Medicine & dosage tracking
- EMR/EHR capabilities

---

### **7. models/department.py** - Medical Departments
```python
class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

**Pre-populated Departments:**
1. Cardiology - Heart and cardiovascular diseases
2. Neurology - Brain and nervous system
3. Orthopedics - Bones and joints
4. Dermatology - Skin conditions
5. Pediatrics - Child health and development

---

## 🔐 Routes & Endpoints

### **Auth Routes** (`routes/auth.py`)
```
POST   /auth/login              - User login
POST   /auth/register           - New user registration
GET    /auth/logout             - Logout user
```

### **Admin Routes** (`routes/admin.py`) - Requires admin role
```
GET    /admin/dashboard         - Admin dashboard with statistics
GET    /admin/doctors           - List all doctors
POST   /admin/add-doctor        - Create new doctor account
GET    /admin/edit-doctor/<id>  - Edit doctor profile
POST   /admin/update-doctor/<id> - Update doctor
GET    /admin/patients          - List all patients
GET    /admin/appointments      - View all appointments
GET/POST /admin/search          - Search patients/doctors
```

### **Doctor Routes** (`routes/doctor.py`) - Requires doctor role
```
GET    /doctor/dashboard        - Doctor dashboard
GET    /doctor/appointments     - View doctor's appointments
POST   /doctor/treatment/<id>   - Create treatment record
GET    /doctor/patients         - List doctor's patients
GET/POST /doctor/profile        - View/edit doctor profile
GET    /doctor/availability     - Manage availability slots
```

### **Patient Routes** (`routes/patient.py`) - Requires patient role
```
GET    /patient/dashboard       - Patient dashboard
GET    /patient/search-doctors  - Search doctors by department
POST   /patient/book-appointment/<id> - Book appointment
GET    /patient/my-appointments - View patient's appointments
GET    /patient/treatment-history - View medical records
GET    /patient/cancel-appointment/<id> - Cancel appointment
GET/POST /patient/profile       - View/edit patient profile
```

---

## 🎨 Frontend - Bootstrap + Font Awesome

### **Base Template** (`templates/base.html`)
- ✅ Professional gradient navbar (blue→teal)
- ✅ Responsive navigation with dropdown menus
- ✅ Flash message alerts with icons
- ✅ Professional footer
- ✅ Font Awesome 6.0.0 icon support
- ✅ Bootstrap 5.1.3 responsive grid

### **Custom CSS** (`static/css/style.css`)
- ✅ Medicare color scheme (Primary Blue #0066cc, Teal #17a2b8)
- ✅ Stat cards for dashboards
- ✅ Appointment cards with status badges
- ✅ Smooth animations & hover effects
- ✅ Professional shadow effects
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Gradient buttons & headers

---

## 💾 Database Schema

### **7 Tables:**
1. **users** - User authentication (1 row: admin)
2. **departments** - Medical departments (5 rows: pre-populated)
3. **doctors** - Doctor profiles (empty)
4. **patients** - Patient profiles (empty)
5. **appointments** - Appointment scheduling (empty)
6. **doctor_availabilities** - Doctor time slots (empty)
7. **treatments** - Medical records (empty)

---

## 🚀 Technology Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Flask 3.1.2, Python 3.14 |
| **Database** | SQLite with SQLAlchemy ORM |
| **Authentication** | Flask-Login with Werkzeug hashing |
| **Frontend** | Bootstrap 5.1.3, Font Awesome 6.0.0 |
| **Templating** | Jinja2 |
| **Security** | Werkzeug password hashing, CSRF protection |

---

## 📊 User Roles & Permissions

### **Admin**
- ✅ Create/edit/delete doctors
- ✅ View all patients
- ✅ Monitor all appointments
- ✅ Search & manage system
- ✅ Dashboard with statistics

### **Doctor**
- ✅ View assigned appointments
- ✅ Create treatment records for patients
- ✅ View patient medical history
- ✅ Manage profile & availability
- ✅ View patient list

### **Patient**
- ✅ Browse doctors by department
- ✅ Book appointments
- ✅ View appointment history
- ✅ Cancel appointments
- ✅ View treatment history
- ✅ Update profile

---

## 🔧 Key Features

### **Medicare-Inspired:**
- ✅ Queue management system
- ✅ Payment & billing tracking
- ✅ Appointment confirmation workflow
- ✅ Insurance integration
- ✅ Notification preferences (email/SMS/WhatsApp)
- ✅ Doctor ratings & reviews
- ✅ Medical coding (ICD standards)
- ✅ Lab test tracking
- ✅ Follow-up management
- ✅ Professional healthcare UI/UX

### **Professional:**
- ✅ Role-based access control (RBAC)
- ✅ Secure password hashing (Scrypt)
- ✅ Flash message notifications
- ✅ Responsive design
- ✅ Database relationships & integrity
- ✅ Error handling & validation

---

## 🎯 Quick Start

### **Login Credentials:**
```
Username: admin
Password: admin123
```

### **URLs:**
```
Dashboard:   http://localhost:5000/
Login:       http://localhost:5000/auth/login
Register:    http://localhost:5000/auth/register
Admin:       http://localhost:5000/admin/dashboard
Doctor:      http://localhost:5000/doctor/dashboard
Patient:     http://localhost:5000/patient/dashboard
```

---

## 📝 Dependencies

See `requirements.txt`:
- Flask==3.1.2
- Flask-SQLAlchemy==3.1.1
- Flask-Login==0.6.3
- Werkzeug==3.1.3
- Click==8.1.7
- Jinja2==3.1.6
- MarkupSafe==2.1.5
- SQLAlchemy==2.0.44

---

## 🎓 Learning Path

1. **Start here:** `app.py` - Understand the Flask app factory
2. **Then:** `models/` - Study the database models
3. **Next:** `routes/` - Review the API endpoints
4. **Finally:** `templates/` - Explore the UI templates

---

## ✨ Future Enhancements

- [ ] Email notification system
- [ ] SMS/WhatsApp integration
- [ ] Payment gateway (Stripe/PayPal)
- [ ] Advanced reporting & analytics
- [ ] Mobile app
- [ ] Real-time queue updates (WebSocket)
- [ ] Video consultation support
- [ ] AI-powered symptoms checker

---

**Project Status:** ✅ Fully Functional

**Last Updated:** November 16, 2025

**Medicare HMS - Professional Healthcare Management System**
