from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app import db
from models.user import User
from models.doctor import Doctor
from models.patient import Patient
from models.appointment import Appointment
from models.department import Department
from datetime import datetime
from sqlalchemy import or_, and_

api_bp = Blueprint('api', __name__, url_prefix='/api')

# ==================== Helper Functions ====================

def api_auth_required(f):
    """Decorator to require authentication for API endpoints"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin role for API endpoints"""
    from functools import wraps
    @wraps(f)
    @api_auth_required
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

def success_response(data, message="Success", status=200):
    """Return successful JSON response"""
    return jsonify({
        'success': True,
        'message': message,
        'data': data
    }), status

def error_response(message, status=400):
    """Return error JSON response"""
    return jsonify({
        'success': False,
        'error': message
    }), status

# ==================== Model Serialization ====================

def doctor_to_dict(doctor, include_user=True):
    """Convert Doctor model to dictionary"""
    data = {
        'id': doctor.id,
        'phone': doctor.phone,
        'license_number': doctor.license_number,
        'experience_years': doctor.experience_years,
        'qualification': doctor.qualification,
        'specialization': doctor.specialization,
        'bio': doctor.bio,
        'consultation_fees': doctor.consultation_fees,
        'rating': doctor.rating,
        'total_patients': doctor.total_patients,
        'total_appointments': doctor.total_appointments,
        'is_available': doctor.is_available,
        'clinic_name': doctor.clinic_name,
        'working_days': doctor.working_days,
        'morning_slot_start': doctor.morning_slot_start,
        'morning_slot_end': doctor.morning_slot_end,
        'evening_slot_start': doctor.evening_slot_start,
        'evening_slot_end': doctor.evening_slot_end,
        'avg_consultation_time': doctor.avg_consultation_time,
        'created_at': doctor.created_at.isoformat() if doctor.created_at else None,
    }
    
    if include_user and doctor.user:
        data['user'] = {
            'id': doctor.user.id,
            'username': doctor.user.username,
            'email': doctor.user.email,
            'is_active': doctor.user.is_active
        }
    
    if doctor.department:
        data['department'] = {
            'id': doctor.department.id,
            'name': doctor.department.name
        }
    
    return data

def patient_to_dict(patient, include_user=True):
    """Convert Patient model to dictionary"""
    data = {
        'id': patient.id,
        'phone': patient.phone,
        'alternate_phone': patient.alternate_phone,
        'date_of_birth': patient.date_of_birth.isoformat() if patient.date_of_birth else None,
        'gender': patient.gender,
        'blood_group': patient.blood_group,
        'address': patient.address,
        'city': patient.city,
        'pincode': patient.pincode,
        'medical_history': patient.medical_history,
        'allergies': patient.allergies,
        'insurance_provider': patient.insurance_provider,
        'insurance_id': patient.insurance_id,
        'emergency_contact': patient.emergency_contact,
        'emergency_contact_name': patient.emergency_contact_name,
        'enable_notifications': patient.enable_notifications,
        'notification_preference': patient.notification_preference,
        'last_visit': patient.last_visit.isoformat() if patient.last_visit else None,
        'total_visits': patient.total_visits,
        'total_spent': patient.total_spent,
        'created_at': patient.created_at.isoformat() if patient.created_at else None,
    }
    
    if include_user and patient.user:
        data['user'] = {
            'id': patient.user.id,
            'username': patient.user.username,
            'email': patient.user.email,
            'is_active': patient.user.is_active
        }
    
    return data

def appointment_to_dict(appointment, include_relations=True):
    """Convert Appointment model to dictionary"""
    data = {
        'id': appointment.id,
        'patient_id': appointment.patient_id,
        'doctor_id': appointment.doctor_id,
        'appointment_date': appointment.appointment_date.isoformat() if appointment.appointment_date else None,
        'appointment_time': appointment.appointment_time,
        'status': appointment.status,
        'notes': appointment.notes,
        'queue_position': appointment.queue_position,
        'reminder_sent': appointment.reminder_sent,
        'appointment_type': appointment.appointment_type,
        'consultation_fees': appointment.consultation_fees,
        'payment_status': appointment.payment_status,
        'is_confirmed': appointment.is_confirmed,
        'created_at': appointment.created_at.isoformat() if appointment.created_at else None,
    }
    
    if include_relations:
        if appointment.patient and appointment.patient.user:
            data['patient'] = {
                'id': appointment.patient.id,
                'name': appointment.patient.user.username,
                'email': appointment.patient.user.email,
                'phone': appointment.patient.phone
            }
        
        if appointment.doctor and appointment.doctor.user:
            data['doctor'] = {
                'id': appointment.doctor.id,
                'name': appointment.doctor.user.username,
                'specialization': appointment.doctor.specialization,
                'department': appointment.doctor.department.name if appointment.doctor.department else None
            }
    
    return data

# ==================== Doctor API Endpoints ====================

@api_bp.route('/doctors', methods=['GET'])
@api_auth_required
def get_doctors():
    """
    GET /api/doctors - List all doctors
    Query params: department_id, specialization, is_available, page, per_page
    """
    # Get query parameters
    department_id = request.args.get('department_id', type=int)
    specialization = request.args.get('specialization')
    is_available = request.args.get('is_available')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Build query
    query = Doctor.query.join(User).filter(User.is_active == True)
    
    if department_id:
        query = query.filter(Doctor.department_id == department_id)
    
    if specialization:
        query = query.filter(Doctor.specialization.ilike(f'%{specialization}%'))
    
    if is_available is not None:
        is_available_bool = is_available.lower() in ['true', '1', 'yes']
        query = query.filter(Doctor.is_available == is_available_bool)
    
    # Paginate
    doctors_page = query.paginate(page=page, per_page=per_page, error_out=False)
    
    doctors_data = [doctor_to_dict(doctor) for doctor in doctors_page.items]
    
    return success_response({
        'doctors': doctors_data,
        'pagination': {
            'page': doctors_page.page,
            'per_page': doctors_page.per_page,
            'total': doctors_page.total,
            'pages': doctors_page.pages
        }
    })

@api_bp.route('/doctors/<int:doctor_id>', methods=['GET'])
@api_auth_required
def get_doctor(doctor_id):
    """GET /api/doctors/<id> - Get single doctor details"""
    doctor = Doctor.query.get(doctor_id)
    
    if not doctor:
        return error_response('Doctor not found', 404)
    
    return success_response(doctor_to_dict(doctor))

@api_bp.route('/doctors', methods=['POST'])
@admin_required
def create_doctor():
    """
    POST /api/doctors - Create new doctor
    Required: username, email, password, department_id, license_number
    """
    data = request.get_json()
    
    if not data:
        return error_response('No data provided')
    
    # Validate required fields
    required_fields = ['username', 'email', 'password', 'department_id', 'license_number']
    for field in required_fields:
        if field not in data:
            return error_response(f'Missing required field: {field}')
    
    # Check if email already exists
    if User.query.filter_by(email=data['email']).first():
        return error_response('Email already registered')
    
    # Check if license number already exists
    if Doctor.query.filter_by(license_number=data['license_number']).first():
        return error_response('License number already exists')
    
    # Check if department exists
    department = Department.query.get(data['department_id'])
    if not department:
        return error_response('Invalid department_id')
    
    try:
        # Create user
        user = User(
            username=data['username'],
            email=data['email'],
            role='doctor',
            is_active=True
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.flush()
        
        # Create doctor
        doctor = Doctor(
            user_id=user.id,
            department_id=data['department_id'],
            license_number=data['license_number'],
            phone=data.get('phone'),
            experience_years=data.get('experience_years', 0),
            qualification=data.get('qualification'),
            specialization=data.get('specialization'),
            bio=data.get('bio'),
            consultation_fees=data.get('consultation_fees', 500.0),
            is_available=data.get('is_available', True)
        )
        db.session.add(doctor)
        db.session.commit()
        
        return success_response(doctor_to_dict(doctor), 'Doctor created successfully', 201)
    
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error creating doctor: {str(e)}', 500)

@api_bp.route('/doctors/<int:doctor_id>', methods=['PUT'])
@admin_required
def update_doctor(doctor_id):
    """PUT /api/doctors/<id> - Update doctor details"""
    doctor = Doctor.query.get(doctor_id)
    
    if not doctor:
        return error_response('Doctor not found', 404)
    
    data = request.get_json()
    if not data:
        return error_response('No data provided')
    
    try:
        # Update doctor fields
        if 'phone' in data:
            doctor.phone = data['phone']
        if 'experience_years' in data:
            doctor.experience_years = data['experience_years']
        if 'qualification' in data:
            doctor.qualification = data['qualification']
        if 'specialization' in data:
            doctor.specialization = data['specialization']
        if 'bio' in data:
            doctor.bio = data['bio']
        if 'consultation_fees' in data:
            doctor.consultation_fees = data['consultation_fees']
        if 'is_available' in data:
            doctor.is_available = data['is_available']
        if 'clinic_name' in data:
            doctor.clinic_name = data['clinic_name']
        if 'working_days' in data:
            doctor.working_days = data['working_days']
        
        # Update user fields if provided
        if 'username' in data:
            doctor.user.username = data['username']
        if 'email' in data:
            # Check if email is already taken by another user
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user and existing_user.id != doctor.user_id:
                return error_response('Email already taken')
            doctor.user.email = data['email']
        if 'is_active' in data:
            doctor.user.is_active = data['is_active']
        
        db.session.commit()
        
        return success_response(doctor_to_dict(doctor), 'Doctor updated successfully')
    
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error updating doctor: {str(e)}', 500)

@api_bp.route('/doctors/<int:doctor_id>', methods=['DELETE'])
@admin_required
def delete_doctor(doctor_id):
    """DELETE /api/doctors/<id> - Delete doctor (soft delete by deactivating)"""
    doctor = Doctor.query.get(doctor_id)
    
    if not doctor:
        return error_response('Doctor not found', 404)
    
    try:
        # Soft delete by deactivating the user
        doctor.user.is_active = False
        doctor.is_available = False
        db.session.commit()
        
        return success_response({'id': doctor_id}, 'Doctor deactivated successfully')
    
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error deleting doctor: {str(e)}', 500)

# ==================== Patient API Endpoints ====================

@api_bp.route('/patients', methods=['GET'])
@api_auth_required
def get_patients():
    """
    GET /api/patients - List all patients
    Admin: can see all patients
    Doctor: can see their patients
    Patient: can only see themselves
    Query params: page, per_page
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    if current_user.role == 'admin':
        # Admin can see all patients
        query = Patient.query.join(User).filter(User.is_active == True)
    elif current_user.role == 'doctor':
        # Doctor can see their patients (who have appointments with them)
        doctor = Doctor.query.filter_by(user_id=current_user.id).first()
        if not doctor:
            return error_response('Doctor profile not found', 404)
        
        # Get patient IDs from appointments
        patient_ids = db.session.query(Appointment.patient_id).filter_by(doctor_id=doctor.id).distinct().all()
        patient_ids = [pid[0] for pid in patient_ids]
        
        query = Patient.query.filter(Patient.id.in_(patient_ids))
    elif current_user.role == 'patient':
        # Patient can only see themselves
        query = Patient.query.filter_by(user_id=current_user.id)
    else:
        return error_response('Unauthorized', 403)
    
    # Paginate
    patients_page = query.paginate(page=page, per_page=per_page, error_out=False)
    
    patients_data = [patient_to_dict(patient) for patient in patients_page.items]
    
    return success_response({
        'patients': patients_data,
        'pagination': {
            'page': patients_page.page,
            'per_page': patients_page.per_page,
            'total': patients_page.total,
            'pages': patients_page.pages
        }
    })

@api_bp.route('/patients/<int:patient_id>', methods=['GET'])
@api_auth_required
def get_patient(patient_id):
    """GET /api/patients/<id> - Get single patient details"""
    patient = Patient.query.get(patient_id)
    
    if not patient:
        return error_response('Patient not found', 404)
    
    # Authorization check
    if current_user.role == 'patient' and patient.user_id != current_user.id:
        return error_response('Unauthorized access', 403)
    elif current_user.role == 'doctor':
        # Check if doctor has treated this patient
        doctor = Doctor.query.filter_by(user_id=current_user.id).first()
        has_appointment = Appointment.query.filter_by(doctor_id=doctor.id, patient_id=patient_id).first()
        if not has_appointment:
            return error_response('Unauthorized access', 403)
    
    return success_response(patient_to_dict(patient))

@api_bp.route('/patients', methods=['POST'])
@admin_required
def create_patient():
    """
    POST /api/patients - Create new patient
    Required: username, email, password
    """
    data = request.get_json()
    
    if not data:
        return error_response('No data provided')
    
    # Validate required fields
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return error_response(f'Missing required field: {field}')
    
    # Check if email already exists
    if User.query.filter_by(email=data['email']).first():
        return error_response('Email already registered')
    
    try:
        # Create user
        user = User(
            username=data['username'],
            email=data['email'],
            role='patient',
            is_active=True
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.flush()
        
        # Create patient
        patient = Patient(
            user_id=user.id,
            phone=data.get('phone'),
            alternate_phone=data.get('alternate_phone'),
            date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date() if data.get('date_of_birth') else None,
            gender=data.get('gender'),
            blood_group=data.get('blood_group'),
            address=data.get('address'),
            city=data.get('city'),
            pincode=data.get('pincode'),
            medical_history=data.get('medical_history'),
            allergies=data.get('allergies'),
            insurance_provider=data.get('insurance_provider'),
            insurance_id=data.get('insurance_id'),
            emergency_contact=data.get('emergency_contact'),
            emergency_contact_name=data.get('emergency_contact_name')
        )
        db.session.add(patient)
        db.session.commit()
        
        return success_response(patient_to_dict(patient), 'Patient created successfully', 201)
    
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error creating patient: {str(e)}', 500)

@api_bp.route('/patients/<int:patient_id>', methods=['PUT'])
@api_auth_required
def update_patient(patient_id):
    """PUT /api/patients/<id> - Update patient details"""
    patient = Patient.query.get(patient_id)
    
    if not patient:
        return error_response('Patient not found', 404)
    
    # Authorization check
    if current_user.role == 'patient' and patient.user_id != current_user.id:
        return error_response('Unauthorized access', 403)
    elif current_user.role == 'doctor':
        return error_response('Doctors cannot update patient details', 403)
    
    data = request.get_json()
    if not data:
        return error_response('No data provided')
    
    try:
        # Update patient fields
        if 'phone' in data:
            patient.phone = data['phone']
        if 'alternate_phone' in data:
            patient.alternate_phone = data['alternate_phone']
        if 'date_of_birth' in data:
            patient.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        if 'gender' in data:
            patient.gender = data['gender']
        if 'blood_group' in data:
            patient.blood_group = data['blood_group']
        if 'address' in data:
            patient.address = data['address']
        if 'city' in data:
            patient.city = data['city']
        if 'pincode' in data:
            patient.pincode = data['pincode']
        if 'medical_history' in data:
            patient.medical_history = data['medical_history']
        if 'allergies' in data:
            patient.allergies = data['allergies']
        if 'emergency_contact' in data:
            patient.emergency_contact = data['emergency_contact']
        if 'emergency_contact_name' in data:
            patient.emergency_contact_name = data['emergency_contact_name']
        
        # Update user fields if provided and if admin
        if current_user.role == 'admin':
            if 'username' in data:
                patient.user.username = data['username']
            if 'email' in data:
                existing_user = User.query.filter_by(email=data['email']).first()
                if existing_user and existing_user.id != patient.user_id:
                    return error_response('Email already taken')
                patient.user.email = data['email']
            if 'is_active' in data:
                patient.user.is_active = data['is_active']
        
        db.session.commit()
        
        return success_response(patient_to_dict(patient), 'Patient updated successfully')
    
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error updating patient: {str(e)}', 500)

@api_bp.route('/patients/<int:patient_id>', methods=['DELETE'])
@admin_required
def delete_patient(patient_id):
    """DELETE /api/patients/<id> - Delete patient (soft delete by deactivating)"""
    patient = Patient.query.get(patient_id)
    
    if not patient:
        return error_response('Patient not found', 404)
    
    try:
        # Soft delete by deactivating the user
        patient.user.is_active = False
        db.session.commit()
        
        return success_response({'id': patient_id}, 'Patient deactivated successfully')
    
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error deleting patient: {str(e)}', 500)

# ==================== Appointment API Endpoints ====================

@api_bp.route('/appointments', methods=['GET'])
@api_auth_required
def get_appointments():
    """
    GET /api/appointments - List appointments
    Admin: all appointments
    Doctor: their appointments
    Patient: their appointments
    Query params: status, date_from, date_to, page, per_page
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    # Base query based on role
    if current_user.role == 'admin':
        query = Appointment.query
    elif current_user.role == 'doctor':
        doctor = Doctor.query.filter_by(user_id=current_user.id).first()
        if not doctor:
            return error_response('Doctor profile not found', 404)
        query = Appointment.query.filter_by(doctor_id=doctor.id)
    elif current_user.role == 'patient':
        patient = Patient.query.filter_by(user_id=current_user.id).first()
        if not patient:
            return error_response('Patient profile not found', 404)
        query = Appointment.query.filter_by(patient_id=patient.id)
    else:
        return error_response('Unauthorized', 403)
    
    # Apply filters
    if status:
        query = query.filter(Appointment.status == status)
    
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
            query = query.filter(Appointment.appointment_date >= date_from_obj)
        except ValueError:
            return error_response('Invalid date_from format. Use YYYY-MM-DD')
    
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
            query = query.filter(Appointment.appointment_date <= date_to_obj)
        except ValueError:
            return error_response('Invalid date_to format. Use YYYY-MM-DD')
    
    # Order by date and time
    query = query.order_by(Appointment.appointment_date.desc(), Appointment.appointment_time.desc())
    
    # Paginate
    appointments_page = query.paginate(page=page, per_page=per_page, error_out=False)
    
    appointments_data = [appointment_to_dict(appointment) for appointment in appointments_page.items]
    
    return success_response({
        'appointments': appointments_data,
        'pagination': {
            'page': appointments_page.page,
            'per_page': appointments_page.per_page,
            'total': appointments_page.total,
            'pages': appointments_page.pages
        }
    })

@api_bp.route('/appointments/<int:appointment_id>', methods=['GET'])
@api_auth_required
def get_appointment(appointment_id):
    """GET /api/appointments/<id> - Get single appointment details"""
    appointment = Appointment.query.get(appointment_id)
    
    if not appointment:
        return error_response('Appointment not found', 404)
    
    # Authorization check
    if current_user.role == 'patient':
        patient = Patient.query.filter_by(user_id=current_user.id).first()
        if not patient or appointment.patient_id != patient.id:
            return error_response('Unauthorized access', 403)
    elif current_user.role == 'doctor':
        doctor = Doctor.query.filter_by(user_id=current_user.id).first()
        if not doctor or appointment.doctor_id != doctor.id:
            return error_response('Unauthorized access', 403)
    
    return success_response(appointment_to_dict(appointment))

@api_bp.route('/appointments', methods=['POST'])
@api_auth_required
def create_appointment():
    """
    POST /api/appointments - Create new appointment
    Required: doctor_id, appointment_date, appointment_time
    Patient can create for themselves, Admin can create for any patient
    """
    data = request.get_json()
    
    if not data:
        return error_response('No data provided')
    
    # Validate required fields
    required_fields = ['doctor_id', 'appointment_date', 'appointment_time']
    for field in required_fields:
        if field not in data:
            return error_response(f'Missing required field: {field}')
    
    # Get patient_id
    if current_user.role == 'patient':
        patient = Patient.query.filter_by(user_id=current_user.id).first()
        if not patient:
            return error_response('Patient profile not found', 404)
        patient_id = patient.id
    elif current_user.role == 'admin':
        if 'patient_id' not in data:
            return error_response('Admin must specify patient_id')
        patient_id = data['patient_id']
    else:
        return error_response('Doctors cannot create appointments', 403)
    
    # Validate doctor exists
    doctor = Doctor.query.get(data['doctor_id'])
    if not doctor:
        return error_response('Doctor not found', 404)
    
    # Validate patient exists
    patient = Patient.query.get(patient_id)
    if not patient:
        return error_response('Patient not found', 404)
    
    try:
        # Parse appointment date
        appointment_date = datetime.strptime(data['appointment_date'], '%Y-%m-%d').date()
        
        # Check for double booking (conflict prevention)
        existing = Appointment.query.filter_by(
            doctor_id=data['doctor_id'],
            appointment_date=appointment_date,
            appointment_time=data['appointment_time'],
            status='Booked'
        ).first()
        
        if existing:
            return error_response('This time slot is already booked. Please choose another time.')
        
        # Create appointment
        appointment = Appointment(
            patient_id=patient_id,
            doctor_id=data['doctor_id'],
            appointment_date=appointment_date,
            appointment_time=data['appointment_time'],
            appointment_type=data.get('appointment_type', 'Regular'),
            notes=data.get('notes'),
            consultation_fees=doctor.consultation_fees,
            status='Booked'
        )
        
        db.session.add(appointment)
        
        # Update doctor stats
        doctor.total_appointments = (doctor.total_appointments or 0) + 1
        
        # Update patient stats
        patient.total_visits = (patient.total_visits or 0) + 1
        patient.last_visit = datetime.now()
        
        db.session.commit()
        
        return success_response(appointment_to_dict(appointment), 'Appointment created successfully', 201)
    
    except ValueError:
        return error_response('Invalid date format. Use YYYY-MM-DD')
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error creating appointment: {str(e)}', 500)

@api_bp.route('/appointments/<int:appointment_id>', methods=['PUT'])
@api_auth_required
def update_appointment(appointment_id):
    """
    PUT /api/appointments/<id> - Update appointment
    Patient can update their own appointments (reschedule, cancel)
    Doctor can update status (Complete, No-show)
    Admin can update anything
    """
    appointment = Appointment.query.get(appointment_id)
    
    if not appointment:
        return error_response('Appointment not found', 404)
    
    # Authorization check
    if current_user.role == 'patient':
        patient = Patient.query.filter_by(user_id=current_user.id).first()
        if not patient or appointment.patient_id != patient.id:
            return error_response('Unauthorized access', 403)
    elif current_user.role == 'doctor':
        doctor = Doctor.query.filter_by(user_id=current_user.id).first()
        if not doctor or appointment.doctor_id != doctor.id:
            return error_response('Unauthorized access', 403)
    
    data = request.get_json()
    if not data:
        return error_response('No data provided')
    
    try:
        # Patient can reschedule or cancel
        if current_user.role == 'patient':
            if 'appointment_date' in data or 'appointment_time' in data:
                new_date = datetime.strptime(data.get('appointment_date', str(appointment.appointment_date)), '%Y-%m-%d').date()
                new_time = data.get('appointment_time', appointment.appointment_time)
                
                # Check for conflicts (excluding current appointment)
                existing = Appointment.query.filter(
                    Appointment.doctor_id == appointment.doctor_id,
                    Appointment.appointment_date == new_date,
                    Appointment.appointment_time == new_time,
                    Appointment.status == 'Booked',
                    Appointment.id != appointment_id
                ).first()
                
                if existing:
                    return error_response('This time slot is already booked. Please choose another time.')
                
                appointment.appointment_date = new_date
                appointment.appointment_time = new_time
            
            if 'status' in data and data['status'] == 'Cancelled':
                appointment.status = 'Cancelled'
            
            if 'notes' in data:
                appointment.notes = data['notes']
        
        # Doctor can update status and notes
        elif current_user.role == 'doctor':
            if 'status' in data:
                allowed_statuses = ['Completed', 'No-show', 'Booked']
                if data['status'] in allowed_statuses:
                    appointment.status = data['status']
            
            if 'notes' in data:
                appointment.notes = data['notes']
            
            if 'is_confirmed' in data:
                appointment.is_confirmed = data['is_confirmed']
        
        # Admin can update anything
        elif current_user.role == 'admin':
            if 'appointment_date' in data:
                appointment.appointment_date = datetime.strptime(data['appointment_date'], '%Y-%m-%d').date()
            if 'appointment_time' in data:
                appointment.appointment_time = data['appointment_time']
            if 'status' in data:
                appointment.status = data['status']
            if 'notes' in data:
                appointment.notes = data['notes']
            if 'appointment_type' in data:
                appointment.appointment_type = data['appointment_type']
            if 'payment_status' in data:
                appointment.payment_status = data['payment_status']
            if 'is_confirmed' in data:
                appointment.is_confirmed = data['is_confirmed']
        
        db.session.commit()
        
        return success_response(appointment_to_dict(appointment), 'Appointment updated successfully')
    
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error updating appointment: {str(e)}', 500)

@api_bp.route('/appointments/<int:appointment_id>', methods=['DELETE'])
@api_auth_required
def delete_appointment(appointment_id):
    """
    DELETE /api/appointments/<id> - Delete/Cancel appointment
    Patient can cancel their own appointments
    Admin can delete any appointment
    """
    appointment = Appointment.query.get(appointment_id)
    
    if not appointment:
        return error_response('Appointment not found', 404)
    
    # Authorization check
    if current_user.role == 'patient':
        patient = Patient.query.filter_by(user_id=current_user.id).first()
        if not patient or appointment.patient_id != patient.id:
            return error_response('Unauthorized access', 403)
        # Patient can only cancel, not delete
        appointment.status = 'Cancelled'
        db.session.commit()
        return success_response({'id': appointment_id}, 'Appointment cancelled successfully')
    
    elif current_user.role == 'doctor':
        return error_response('Doctors cannot delete appointments', 403)
    
    elif current_user.role == 'admin':
        # Admin can hard delete
        try:
            db.session.delete(appointment)
            db.session.commit()
            return success_response({'id': appointment_id}, 'Appointment deleted successfully')
        except Exception as e:
            db.session.rollback()
            return error_response(f'Error deleting appointment: {str(e)}', 500)
    
    return error_response('Unauthorized', 403)

# ==================== Statistics Endpoints ====================

@api_bp.route('/stats', methods=['GET'])
@admin_required
def get_stats():
    """GET /api/stats - Get system statistics (admin only)"""
    total_doctors = Doctor.query.count()
    total_patients = Patient.query.count()
    total_appointments = Appointment.query.count()
    
    active_doctors = Doctor.query.join(User).filter(User.is_active == True).count()
    active_patients = Patient.query.join(User).filter(User.is_active == True).count()
    
    booked_appointments = Appointment.query.filter_by(status='Booked').count()
    completed_appointments = Appointment.query.filter_by(status='Completed').count()
    cancelled_appointments = Appointment.query.filter_by(status='Cancelled').count()
    
    # Department statistics
    departments = Department.query.all()
    dept_stats = []
    for dept in departments:
        doctor_count = Doctor.query.filter_by(department_id=dept.id).count()
        dept_stats.append({
            'id': dept.id,
            'name': dept.name,
            'doctors': doctor_count
        })
    
    return success_response({
        'doctors': {
            'total': total_doctors,
            'active': active_doctors
        },
        'patients': {
            'total': total_patients,
            'active': active_patients
        },
        'appointments': {
            'total': total_appointments,
            'booked': booked_appointments,
            'completed': completed_appointments,
            'cancelled': cancelled_appointments
        },
        'departments': dept_stats
    })
