# API Endpoint Testing Guide - Hospital Management System

## Base URL
```
http://localhost:5000/api
```

## Authentication
All API endpoints require authentication. Use session cookies from Flask-Login.

## HTTP Methods Supported
- GET: Retrieve resources
- POST: Create new resources
- PUT: Update existing resources
- DELETE: Delete/deactivate resources

---

## Doctor Endpoints

### 1. GET /api/doctors
List all doctors (with pagination and filters)

**Query Parameters:**
- `department_id` (int): Filter by department
- `specialization` (string): Filter by specialization
- `is_available` (boolean): Filter by availability
- `page` (int, default=1): Page number
- `per_page` (int, default=20): Items per page

**Example:**
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/doctors?page=1&per_page=10" -Method GET -WebSession $session
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Success",
  "data": {
    "doctors": [...],
    "pagination": {
      "page": 1,
      "per_page": 10,
      "total": 25,
      "pages": 3
    }
  }
}
```

### 2. GET /api/doctors/<id>
Get single doctor details

**Example:**
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/doctors/1" -Method GET -WebSession $session
```

### 3. POST /api/doctors (Admin Only)
Create new doctor

**Required Fields:**
- username
- email
- password
- department_id
- license_number

**Example:**
```powershell
$body = @{
    username = "Dr. Smith"
    email = "smith@hospital.com"
    password = "secure123"
    department_id = 1
    license_number = "DOC12345"
    phone = "9876543210"
    specialization = "Cardiology"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/doctors" -Method POST -Body $body -ContentType "application/json" -WebSession $session
```

### 4. PUT /api/doctors/<id> (Admin Only)
Update doctor details

**Example:**
```powershell
$body = @{
    phone = "9999999999"
    consultation_fees = 800
    is_available = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/doctors/1" -Method PUT -Body $body -ContentType "application/json" -WebSession $session
```

### 5. DELETE /api/doctors/<id> (Admin Only)
Deactivate doctor (soft delete)

**Example:**
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/doctors/1" -Method DELETE -WebSession $session
```

---

## Patient Endpoints

### 1. GET /api/patients
List patients (role-based access)
- Admin: All patients
- Doctor: Their patients
- Patient: Only themselves

**Query Parameters:**
- `page` (int, default=1)
- `per_page` (int, default=20)

**Example:**
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/patients" -Method GET -WebSession $session
```

### 2. GET /api/patients/<id>
Get single patient details

### 3. POST /api/patients (Admin Only)
Create new patient

**Required Fields:**
- username
- email
- password

**Example:**
```powershell
$body = @{
    username = "John Doe"
    email = "john@example.com"
    password = "secure123"
    phone = "1234567890"
    blood_group = "O+"
    date_of_birth = "1990-05-15"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/patients" -Method POST -Body $body -ContentType "application/json" -WebSession $session
```

### 4. PUT /api/patients/<id>
Update patient details
- Admin: Can update any patient
- Patient: Can only update themselves

**Example:**
```powershell
$body = @{
    phone = "9999888877"
    address = "123 Main Street"
    city = "Mumbai"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/patients/1" -Method PUT -Body $body -ContentType "application/json" -WebSession $session
```

### 5. DELETE /api/patients/<id> (Admin Only)
Deactivate patient (soft delete)

---

## Appointment Endpoints

### 1. GET /api/appointments
List appointments (role-based access)
- Admin: All appointments
- Doctor: Their appointments
- Patient: Their appointments

**Query Parameters:**
- `status` (string): Filter by status (Booked/Completed/Cancelled)
- `date_from` (YYYY-MM-DD): Filter by date range
- `date_to` (YYYY-MM-DD): Filter by date range
- `page` (int, default=1)
- `per_page` (int, default=20)

**Example:**
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/appointments?status=Booked" -Method GET -WebSession $session
```

### 2. GET /api/appointments/<id>
Get single appointment details

### 3. POST /api/appointments
Create new appointment (with conflict prevention)
- Patient: Can create for themselves
- Admin: Can create for any patient

**Required Fields:**
- doctor_id
- appointment_date (YYYY-MM-DD)
- appointment_time (HH:MM)

**Example:**
```powershell
$body = @{
    doctor_id = 1
    patient_id = 2
    appointment_date = "2025-11-30"
    appointment_time = "10:00"
    appointment_type = "Regular"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/appointments" -Method POST -Body $body -ContentType "application/json" -WebSession $session
```

**Conflict Prevention:**
If time slot is already booked, returns 400 error:
```json
{
  "success": false,
  "error": "This time slot is already booked. Please choose another time."
}
```

### 4. PUT /api/appointments/<id>
Update appointment
- Patient: Can reschedule or cancel
- Doctor: Can update status and notes
- Admin: Can update anything

**Example (Patient Reschedule):**
```powershell
$body = @{
    appointment_date = "2025-12-01"
    appointment_time = "14:00"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/appointments/5" -Method PUT -Body $body -ContentType "application/json" -WebSession $session
```

**Example (Doctor Update Status):**
```powershell
$body = @{
    status = "Completed"
    notes = "Patient showed improvement"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/appointments/5" -Method PUT -Body $body -ContentType "application/json" -WebSession $session
```

### 5. DELETE /api/appointments/<id>
Delete/Cancel appointment
- Patient: Can cancel (status → Cancelled)
- Admin: Can hard delete

---

## Statistics Endpoint (Admin Only)

### GET /api/stats
Get system statistics

**Example:**
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/stats" -Method GET -WebSession $session
```

**Response:**
```json
{
  "success": true,
  "data": {
    "doctors": {
      "total": 25,
      "active": 23
    },
    "patients": {
      "total": 150,
      "active": 145
    },
    "appointments": {
      "total": 500,
      "booked": 50,
      "completed": 400,
      "cancelled": 50
    },
    "departments": [...]
  }
}
```

---

## Complete Testing Flow (PowerShell)

```powershell
# 1. Login to get session
$loginBody = @{
    email = "admin@hospital.com"
    password = "admin123"
} | ConvertTo-Json

$loginResponse = Invoke-WebRequest -Uri "http://localhost:5000/auth/login" -Method POST -Body $loginBody -ContentType "application/json" -SessionVariable session

# 2. Use the session for API calls
$doctors = Invoke-RestMethod -Uri "http://localhost:5000/api/doctors" -Method GET -WebSession $session

# 3. Create a new patient
$newPatient = @{
    username = "Test Patient"
    email = "test@test.com"
    password = "test123"
} | ConvertTo-Json

$patient = Invoke-RestMethod -Uri "http://localhost:5000/api/patients" -Method POST -Body $newPatient -ContentType "application/json" -WebSession $session

# 4. Book an appointment
$appointment = @{
    doctor_id = 1
    patient_id = $patient.data.id
    appointment_date = "2025-12-01"
    appointment_time = "10:00"
} | ConvertTo-Json

$apt = Invoke-RestMethod -Uri "http://localhost:5000/api/appointments" -Method POST -Body $appointment -ContentType "application/json" -WebSession $session

# 5. Get statistics
$stats = Invoke-RestMethod -Uri "http://localhost:5000/api/stats" -Method GET -WebSession $session
```

---

## Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "error": "Missing required field: email"
}
```

### 401 Unauthorized
```json
{
  "success": false,
  "error": "Authentication required"
}
```

### 403 Forbidden
```json
{
  "success": false,
  "error": "Admin access required"
}
```

### 404 Not Found
```json
{
  "success": false,
  "error": "Doctor not found"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "error": "Error creating doctor: <error details>"
}
```

---

## API Features

✅ **RESTful Design**: Standard HTTP methods (GET, POST, PUT, DELETE)
✅ **JSON Responses**: All responses in JSON format
✅ **Role-Based Access Control**: Admin, Doctor, Patient permissions
✅ **Pagination**: List endpoints support pagination
✅ **Filtering**: Query parameters for filtering results
✅ **Conflict Prevention**: Prevents double booking of appointments
✅ **Error Handling**: Comprehensive error messages
✅ **Authentication**: Session-based with Flask-Login
✅ **Soft Delete**: Deactivate instead of hard delete for data integrity

---

## Total Endpoints: 16

| Endpoint | Methods | Description |
|----------|---------|-------------|
| /api/doctors | GET, POST | List/Create doctors |
| /api/doctors/<id> | GET, PUT, DELETE | Get/Update/Delete doctor |
| /api/patients | GET, POST | List/Create patients |
| /api/patients/<id> | GET, PUT, DELETE | Get/Update/Delete patient |
| /api/appointments | GET, POST | List/Create appointments |
| /api/appointments/<id> | GET, PUT, DELETE | Get/Update/Delete appointment |
| /api/stats | GET | System statistics (admin) |

**Total HTTP Methods Implemented:** 4 (GET, POST, PUT, DELETE)
