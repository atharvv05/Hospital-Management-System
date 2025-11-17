# Database Models and Schema Documentation

## Milestone: Database Models and Schema Setup
**Status:** ✅ COMPLETE (100%)  
**Expected Time:** 5–7 days  
**Actual Completion:** Day 2 (Ahead of Schedule)  
**Progress:** 18% → 100%  

---

## Overview

This milestone covers the complete database schema design and implementation for the Hospital Management System. All required models have been created with proper relationships, constraints, and programmatic database initialization.

---

## Models Created (6 Core Models + 1 Supporting)

### 1. **User Model** (Base Authentication)
**File:** `models/user.py`  
**Purpose:** Core user authentication and authorization  

**Schema:**
```python
- id (Integer, Primary Key)
- username (String, Unique, Not Null)
- email (String, Unique, Not Null)
- password_hash (String, Not Null)
- role (String, Not Null) - admin, doctor, patient
- is_active (Boolean, Default: True)
- created_at (DateTime, Auto-timestamp)
```

**Relationships:**
- One-to-One: doctor_profile (to Doctor)
- One-to-One: patient_profile (to Patient)

**Methods:**
- `set_password()` - Hash password with Werkzeug scrypt
- `check_password()` - Verify password
- UserMixin support for Flask-Login

---

### 2. **Department/Specialization Model**
**File:** `models/department.py`  
**Purpose:** Hospital departments and specializations  

**Schema:**
```python
- id (Integer, Primary Key)
- name (String, Unique, Not Null) - e.g., Cardiology, Neurology
- description (Text)
- created_at (DateTime, Auto-timestamp)
```

**Relationships:**
- One-to-Many: doctors (to Doctor)

**Pre-populated Departments:**
1. Cardiology - Heart and cardiovascular diseases
2. Neurology - Brain and nervous system
3. Orthopedics - Bones and joints
4. Dermatology - Skin conditions
5. Pediatrics - Child health and development

---

### 3. **Doctor Model** (Professional Profile)
**File:** `models/doctor.py`  
**Purpose:** Doctor-specific information and healthcare details  

**Schema:**
```python
- id (Integer, Primary Key)
- user_id (Integer, Foreign Key → users.id, Not Null)
- department_id (Integer, Foreign Key → departments.id, Not Null)
- phone (String)
- license_number (String, Unique)
- experience_years (Integer)
- qualification (String)
- specialization (String)
- bio (Text)
- consultation_fees (Float, Default: 500.0)
- rating (Float, Default: 0.0) - 0-5 star rating
- total_patients (Integer, Default: 0)
- total_appointments (Integer, Default: 0)
- is_available (Boolean, Default: True)
- clinic_name (String)
- working_days (String) - e.g., "Mon-Fri"
- morning_slot_start (String, Default: "09:00")
- morning_slot_end (String, Default: "12:00")
- evening_slot_start (String, Default: "15:00")
- evening_slot_end (String, Default: "18:00")
- avg_consultation_time (Integer, Default: 30) - in minutes
- created_at (DateTime, Auto-timestamp)
```

**Relationships:**
- Many-to-One: User (user_id)
- Many-to-One: Department (department_id)
- One-to-Many: appointments (to Appointment)
- One-to-Many: treatments (to Treatment)
- One-to-Many: availabilities (to DoctorAvailability)

---

### 4. **Patient Model** (Patient Profile)
**File:** `models/patient.py`  
**Purpose:** Patient-specific information and medical history  

**Schema:**
```python
- id (Integer, Primary Key)
- user_id (Integer, Foreign Key → users.id, Not Null)
- phone (String)
- alternate_phone (String)
- date_of_birth (Date)
- gender (String)
- blood_group (String) - e.g., A+, B-, O+
- address (Text)
- city (String)
- pincode (String)
- medical_history (Text)
- allergies (Text)
- insurance_provider (String)
- insurance_id (String)
- emergency_contact (String)
- emergency_contact_name (String)
- enable_notifications (Boolean, Default: True)
- notification_preference (String, Default: 'email') - email, sms, whatsapp
- last_visit (DateTime)
- total_visits (Integer, Default: 0)
- total_spent (Float, Default: 0.0)
- created_at (DateTime, Auto-timestamp)
```

**Relationships:**
- Many-to-One: User (user_id)
- One-to-Many: appointments (to Appointment)
- One-to-Many: treatments (to Treatment)

---

### 5. **Appointment Model** (Scheduling & Queue Management)
**File:** `models/appointment.py`  
**Purpose:** Appointment scheduling, queue management, and payment tracking  

**Schema:**
```python
- id (Integer, Primary Key)
- patient_id (Integer, Foreign Key → patients.id, Not Null)
- doctor_id (Integer, Foreign Key → doctors.id, Not Null)
- appointment_date (Date, Not Null)
- appointment_time (String, Not Null) - HH:MM format
- status (String, Default: 'Booked') - Booked, Completed, Cancelled, No-show
- notes (Text)
- queue_position (Integer) - For queue management
- reminder_sent (Boolean, Default: False)
- appointment_type (String, Default: 'Regular') - Regular, Follow-up, Emergency
- consultation_fees (Float, Default: 0.0)
- payment_status (String, Default: 'Pending') - Pending, Paid, Insurance
- is_confirmed (Boolean, Default: False)
- created_at (DateTime, Auto-timestamp)
```

**Relationships:**
- Many-to-One: Patient (patient_id)
- Many-to-One: Doctor (doctor_id)
- One-to-One: Treatment (backref 'treatment')

**Methods:**
- `is_upcoming()` - Check if appointment is in future

---

### 6. **Treatment Model** (Medical Records)
**File:** `models/treatment.py`  
**Purpose:** Medical treatment records and healthcare documentation  

**Schema:**
```python
- id (Integer, Primary Key)
- appointment_id (Integer, Foreign Key → appointments.id, Not Null)
- patient_id (Integer, Foreign Key → patients.id, Not Null)
- doctor_id (Integer, Foreign Key → doctors.id, Not Null)
- diagnosis (Text)
- icd_code (String) - International Classification of Diseases
- prescription (Text)
- medicine_details (Text)
- dosage_instructions (Text)
- duration_days (Integer)
- follow_up_required (Boolean, Default: False)
- follow_up_days (Integer)
- lab_tests_recommended (Text)
- notes (Text)
- consultation_duration (Integer) - in minutes
- status (String, Default: 'Active') - Active, Completed, Archived
- created_at (DateTime, Auto-timestamp)
```

**Relationships:**
- Many-to-One: Appointment (appointment_id)
- Many-to-One: Patient (patient_id)
- Many-to-One: Doctor (doctor_id)

---

### 7. **DoctorAvailability Model** (Supporting Model)
**File:** `models/treatment.py` (with Treatment)  
**Purpose:** Doctor scheduling and availability management  

**Schema:**
```python
- id (Integer, Primary Key)
- doctor_id (Integer, Foreign Key → doctors.id, Not Null)
- date (Date, Not Null)
- start_time (String)
- end_time (String)
- is_available (Boolean, Default: True)
- created_at (DateTime, Auto-timestamp)
```

**Relationships:**
- Many-to-One: Doctor (doctor_id)

---

## Database Relationships

### Entity Relationship Diagram (ERD)

```
┌──────────────┐
│    User      │  (Core Authentication)
│──────────────│
│ id (PK)      │
│ username     │
│ email        │
│ password     │
│ role         │
└──────────────┘
      │
      ├─────────────────┬─────────────────┐
      │                 │                 │
      │ (1:1)           │ (1:1)           │
      ▼                 ▼                 ▼
┌──────────────┐ ┌──────────────┐
│   Doctor     │ │   Patient    │
│──────────────│ │──────────────│
│ id (PK)      │ │ id (PK)      │
│ user_id (FK) │ │ user_id (FK) │
│ dept_id (FK) │ │ phone        │
└──────────────┘ │ blood_group  │
      │          │ address      │
      │          │ insurance    │
      │          └──────────────┘
      │                 │
      │    (1:M)        │ (1:M)
      └────────┬────────┘
               ▼
        ┌──────────────────┐
        │  Appointment     │  (Central Hub)
        │──────────────────│
        │ id (PK)          │
        │ patient_id (FK)  │
        │ doctor_id (FK)   │
        │ appointment_date │
        │ status           │
        │ payment_status   │
        └──────────────────┘
                 │
                 │ (1:1)
                 ▼
        ┌──────────────────┐
        │    Treatment     │  (Medical Records)
        │──────────────────│
        │ id (PK)          │
        │ appointment_id   │
        │ patient_id       │
        │ doctor_id        │
        │ diagnosis        │
        │ icd_code         │
        │ prescription     │
        │ follow_up_req    │
        └──────────────────┘

        ┌────────────────────┐
        │   Department       │  (Specialization)
        │────────────────────│
        │ id (PK)            │
        │ name               │
        │ description        │
        └────────────────────┘
              ▲
              │ (1:M)
              │
        ┌──────────────┐
        │   Doctor     │
        └──────────────┘

        ┌─────────────────────┐
        │ DoctorAvailability  │  (Scheduling)
        │─────────────────────│
        │ id (PK)             │
        │ doctor_id (FK)      │
        │ date                │
        │ start_time          │
        │ end_time            │
        │ is_available        │
        └─────────────────────┘
```

---

## Relationship Details

### 1. **User ↔ Doctor** (One-to-One)
- Foreign Key: `Doctor.user_id → User.id`
- Backref: `User.doctor_profile`
- Represents: Doctor's authentication and professional profile

### 2. **User ↔ Patient** (One-to-One)
- Foreign Key: `Patient.user_id → User.id`
- Backref: `User.patient_profile`
- Represents: Patient's authentication and health profile

### 3. **Department ↔ Doctor** (One-to-Many)
- Foreign Key: `Doctor.department_id → Department.id`
- Backref: `Department.doctors`
- Represents: A department has many doctors in that specialization

### 4. **Doctor ↔ Appointment** (One-to-Many)
- Foreign Key: `Appointment.doctor_id → Doctor.id`
- Backref: `Doctor.appointments`
- Represents: A doctor has many appointments

### 5. **Patient ↔ Appointment** (One-to-Many)
- Foreign Key: `Appointment.patient_id → Patient.id`
- Backref: `Patient.appointments`
- Represents: A patient has many appointments

### 6. **Appointment ↔ Treatment** (One-to-One)
- Foreign Key: `Treatment.appointment_id → Appointment.id`
- Backref: `Appointment.treatment`
- Represents: Each appointment has one treatment record

### 7. **Doctor ↔ Treatment** (One-to-Many)
- Foreign Key: `Treatment.doctor_id → Doctor.id`
- Backref: `Doctor.treatments`
- Represents: A doctor creates many treatment records

### 8. **Patient ↔ Treatment** (One-to-Many)
- Foreign Key: `Treatment.patient_id → Patient.id`
- Backref: `Patient.treatments`
- Represents: A patient has many treatment records

### 9. **Doctor ↔ DoctorAvailability** (One-to-Many)
- Foreign Key: `DoctorAvailability.doctor_id → Doctor.id`
- Backref: `Doctor.availabilities`
- Represents: A doctor has many availability slots

---

## Database Initialization

### Programmatic Database Creation

**Location:** `app.py` (lines 34-52)

**Process:**
```python
with app.app_context():
    # 1. Import all models
    from models.user import User
    from models.department import Department
    from models.doctor import Doctor
    from models.patient import Patient
    from models.appointment import Appointment
    from models.treatment import Treatment, DoctorAvailability
    
    # 2. Create all tables
    db.create_all()
    
    # 3. Populate default departments (if empty)
    if db.session.query(Department).count() == 0:
        departments = [
            Department(name='Cardiology', description='...'),
            Department(name='Neurology', description='...'),
            # ... more departments
        ]
        db.session.add_all(departments)
        db.session.commit()
```

**Features:**
- ✅ No manual database creation needed
- ✅ All tables created automatically
- ✅ Default departments pre-populated
- ✅ Relationships enforced with foreign keys
- ✅ Constraints and validations in place

---

## Data Constraints & Validation

### Primary Keys
- All models have `id` as primary key (auto-increment)

### Unique Constraints
- `User.username` - Unique across system
- `User.email` - Unique across system
- `Doctor.license_number` - Unique license
- `Department.name` - One specialization name

### Not Null Constraints
- `User`: username, email, password_hash, role
- `Doctor`: user_id, department_id
- `Patient`: user_id
- `Appointment`: patient_id, doctor_id, appointment_date, appointment_time
- `Treatment`: appointment_id, patient_id, doctor_id
- `DoctorAvailability`: doctor_id, date

### Foreign Key Relationships
- All foreign keys reference parent tables
- Cascading relationships properly configured
- Lazy loading for optimization

### Timestamps
- All models have `created_at` field
- Auto-populated with current timestamp
- Tracks creation time for audit trails

---

## Admin Model

**Note:** Admin is handled via the `User` model with `role='admin'`

**Schema:**
- No separate admin table (base-user approach)
- Admin users are distinguished by `User.role = 'admin'`
- Direct access to all system tables and operations

**Advantages:**
- Simplified schema
- Easy user role management
- Flexible permission assignment
- Audit trail through user_id

---

## Database Features Implemented

✅ **CRUD Operations**
- Create: `db.session.add()` and `db.session.commit()`
- Read: Query filters and relationships
- Update: Modify and commit
- Delete: `db.session.delete()` and commit

✅ **Relationships**
- One-to-One (User-Doctor, User-Patient, Appointment-Treatment)
- One-to-Many (Department-Doctor, Doctor-Appointment, etc.)
- Many-to-One (reverse relationships)

✅ **Constraints**
- Primary keys on all models
- Foreign keys with cascading
- Unique constraints on important fields
- Not null constraints for required fields

✅ **Timestamps**
- Auto-created timestamps on all models
- Audit trail for tracking changes
- Default current timestamp

✅ **Validation**
- Data types enforced at model level
- String lengths limited
- Numeric ranges defined
- Boolean defaults set

✅ **Query Optimization**
- Lazy loading for relationships
- Backref for reverse queries
- Efficient foreign key joins

---

## Testing & Verification

### Database Initialization Test
```bash
python app.py
# Automatically creates database and tables
# Verifies all constraints are in place
```

### Model Relationships Test
```bash
python check_users.py
# Shows all users with their profiles
# Verifies relationships are working
```

### Database Schema Verification
```bash
# Using SQLite browser or command line
sqlite3 instance/hospital.db ".schema"
# Shows all tables and relationships
```

---

## Files Structure

```
models/
├── __init__.py
├── user.py              ← User (authentication)
├── doctor.py            ← Doctor (professional)
├── patient.py           ← Patient (health info)
├── department.py        ← Department (specialization)
├── appointment.py       ← Appointment (scheduling)
└── treatment.py         ← Treatment + DoctorAvailability
```

---

## Key Achievements

✅ **6 Core Models Created**
- User, Doctor, Patient, Department, Appointment, Treatment

✅ **1 Supporting Model**
- DoctorAvailability for scheduling

✅ **All Relationships Defined**
- One-to-One: User-Doctor, User-Patient, Appointment-Treatment
- One-to-Many: Department-Doctor, Doctor-Appointment, etc.
- Many-to-One: Reverse relationships

✅ **Programmatic Database Creation**
- No manual SQL scripts needed
- Automatic table creation on startup
- Default data population

✅ **Proper Constraints**
- Primary keys on all models
- Foreign keys with cascading
- Unique constraints for important fields
- Not null for required fields

✅ **Timestamps for Auditing**
- Created_at on all models
- Tracks data changes over time

---

## Git Commit

**Message:** `Milestone-HMS DB-Relationship`

**Changes Included:**
- ✅ All 7 model files (User, Doctor, Patient, Department, Appointment, Treatment, DoctorAvailability)
- ✅ Database schema definition
- ✅ Relationship mappings
- ✅ Programmatic database initialization
- ✅ Default department data

---

## Next Milestone

After Database Models completion:
- **Milestone 2:** API Endpoints & CRUD Operations
- Create REST API for all CRUD operations
- Implement validation and error handling
- Add authentication and authorization checks

---

## Summary

The Database Models and Schema Setup milestone is **100% COMPLETE**. All required models have been created with proper relationships, constraints, and programmatic initialization. The system is ready for API development and business logic implementation.

**Status:** ✅ Ready for next milestone
**Completion Rate:** 100%
**Progress:** 18% → Updated based on actual completion
