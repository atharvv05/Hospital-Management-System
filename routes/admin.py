from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models.user import User
from models.doctor import Doctor
from models.patient import Patient
from models.appointment import Appointment
from models.department import Department

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    total_doctors = Doctor.query.count()
    total_patients = Patient.query.count()
    total_appointments = Appointment.query.count()
    
    return render_template('admin/dashboard.html', 
                         doctors=total_doctors, 
                         patients=total_patients, 
                         appointments=total_appointments)

@admin_bp.route('/doctors')
@login_required
@admin_required
def doctors():
    doctors = Doctor.query.all()
    return render_template('admin/doctors.html', doctors=doctors)

@admin_bp.route('/add-doctor', methods=['GET', 'POST'])
@login_required
@admin_required
def add_doctor():
    """
    Admin-only route to add a new doctor to the system.
    Doctors cannot register themselves; admins must create their accounts.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        department_id = request.form.get('department_id')
        phone = request.form.get('phone')
        license_number = request.form.get('license_number')
        qualification = request.form.get('qualification')
        specialization = request.form.get('specialization')
        experience_years = request.form.get('experience_years', 0)
        
        # Validation: Check if username exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose another.', 'danger')
            return redirect(url_for('admin.add_doctor'))
        
        # Validation: Check if email exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please use another email.', 'danger')
            return redirect(url_for('admin.add_doctor'))
        
        # Validation: Check if license number exists
        if Doctor.query.filter_by(license_number=license_number).first():
            flash('License number already exists in system.', 'danger')
            return redirect(url_for('admin.add_doctor'))
        
        # Validation: Check password match
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('admin.add_doctor'))
        
        # Validation: Check password strength
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return redirect(url_for('admin.add_doctor'))
        
        # Validation: Check department
        try:
            department_id = int(department_id)
            dept = Department.query.get(department_id)
            if not dept:
                flash('Invalid department selected.', 'danger')
                return redirect(url_for('admin.add_doctor'))
        except (ValueError, TypeError):
            flash('Invalid department selection.', 'danger')
            return redirect(url_for('admin.add_doctor'))
        
        try:
            # Create user account
            user = User(username=username, email=email, role='doctor', is_active=True)
            user.set_password(password)
            db.session.add(user)
            db.session.flush()  # Get the user ID without committing
            
            # Create doctor profile
            try:
                experience_years = int(experience_years) if experience_years else 0
            except (ValueError, TypeError):
                experience_years = 0
            
            doctor = Doctor(
                user_id=user.id,
                department_id=department_id,
                phone=phone,
                license_number=license_number,
                qualification=qualification,
                specialization=specialization,
                experience_years=experience_years
            )
            db.session.add(doctor)
            db.session.commit()
            
            flash(f'✅ Doctor "{username}" added successfully! They can now login with their credentials.', 'success')
            return redirect(url_for('admin.doctors'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding doctor: {str(e)}', 'danger')
            return redirect(url_for('admin.add_doctor'))
    
    departments = Department.query.all()
    return render_template('admin/add_doctor.html', departments=departments)

@admin_bp.route('/appointments')
@login_required
@admin_required
def appointments():
    appointments = Appointment.query.all()
    return render_template('admin/appointments.html', appointments=appointments)

@admin_bp.route('/patients')
@login_required
@admin_required
def patients():
    patients = Patient.query.all()
    return render_template('admin/patients.html', patients=patients)

@admin_bp.route('/search', methods=['GET', 'POST'])
@login_required
@admin_required
def search():
    results = []
    search_type = request.form.get('search_type') if request.method == 'POST' else request.args.get('search_type')
    query = request.form.get('query') if request.method == 'POST' else request.args.get('query')
    
    if query:
        if search_type == 'doctor':
            results = Doctor.query.filter(Doctor.user.has(username=query)).all()
        elif search_type == 'patient':
            results = Patient.query.filter(Patient.user.has(username=query)).all()
    
    return render_template('admin/search.html', results=results, query=query, search_type=search_type)
