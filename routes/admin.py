from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models.user import User
from models.doctor import Doctor
from models.patient import Patient
from models.appointment import Appointment
from models.department import Department
from models.treatment import Treatment
from datetime import datetime
from sqlalchemy import or_, and_

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
    """Enhanced admin dashboard with KPIs and statistics"""
    total_doctors = Doctor.query.count()
    total_patients = Patient.query.count()
    total_appointments = Appointment.query.count()
    
    # Upcoming appointments (today onwards)
    today = datetime.today().date()
    upcoming_appointments = Appointment.query.filter(
        and_(
            Appointment.appointment_date >= today,
            Appointment.status.in_(['Booked', 'Confirmed'])
        )
    ).count()
    
    # Past appointments (completed)
    past_appointments = Appointment.query.filter(
        Appointment.status == 'Completed'
    ).count()
    
    # Get active doctors (is_active = True)
    active_doctors = Doctor.query.join(User).filter(User.is_active == True).count()
    
    # Get active patients (is_active = True)
    active_patients = Patient.query.join(User).filter(User.is_active == True).count()
    
    # Total treatments
    total_treatments = Treatment.query.count()
    
    # Department statistics
    departments = Department.query.all()
    dept_stats = []
    for dept in departments:
        doctor_count = Doctor.query.filter_by(department_id=dept.id).count()
        dept_stats.append({
            'name': dept.name,
            'doctors': doctor_count
        })
    
    return render_template('admin/dashboard.html', 
                         total_doctors=total_doctors,
                         active_doctors=active_doctors,
                         total_patients=total_patients,
                         active_patients=active_patients,
                         total_appointments=total_appointments,
                         upcoming_appointments=upcoming_appointments,
                         past_appointments=past_appointments,
                         total_treatments=total_treatments,
                         dept_stats=dept_stats)

@admin_bp.route('/doctors')
@admin_required
def doctors():
    """View all doctors with active/inactive status"""
    page = request.args.get('page', 1, type=int)
    doctors = Doctor.query.join(User).paginate(page=page, per_page=10)
    return render_template('admin/doctors.html', doctors=doctors)

@admin_bp.route('/doctor/<int:doctor_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_doctor(doctor_id):
    """Edit doctor profile"""
    doctor = Doctor.query.get_or_404(doctor_id)
    departments = Department.query.all()
    
    if request.method == 'POST':
        # Validate license uniqueness (if changed)
        new_license = request.form.get('license_number')
        if new_license != doctor.license_number:
            if Doctor.query.filter_by(license_number=new_license).first():
                flash('License number already exists.', 'danger')
                return redirect(url_for('admin.edit_doctor', doctor_id=doctor_id))
        
        # Update doctor fields
        try:
            doctor.phone = request.form.get('phone')
            doctor.license_number = new_license
            doctor.qualification = request.form.get('qualification')
            doctor.specialization = request.form.get('specialization')
            doctor.department_id = int(request.form.get('department_id'))
            doctor.experience_years = int(request.form.get('experience_years', 0))
            
            db.session.commit()
            flash(f'✅ Doctor "{doctor.user.username}" updated successfully.', 'success')
            return redirect(url_for('admin.doctors'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating doctor: {str(e)}', 'danger')
            return redirect(url_for('admin.edit_doctor', doctor_id=doctor_id))
    
    return render_template('admin/edit_doctor.html', doctor=doctor, departments=departments)

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
@admin_required
def appointments():
    """View all appointments with filtering options"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', 'all')
    
    query = Appointment.query
    
    # Filter by status
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    appointments = query.order_by(Appointment.appointment_date.desc()).paginate(page=page, per_page=15)
    
    return render_template('admin/appointments.html', 
                         appointments=appointments, 
                         status_filter=status_filter)

@admin_bp.route('/patients')
@admin_required
def patients():
    """View all patients with active/inactive status"""
    page = request.args.get('page', 1, type=int)
    patients = Patient.query.join(User).paginate(page=page, per_page=10)
    return render_template('admin/patients.html', patients=patients)

@admin_bp.route('/search/patients', methods=['GET', 'POST'])
@admin_required
def search_patients():
    """Search patients by name, ID, email, or contact"""
    results = []
    query_text = ''
    
    if request.method == 'POST' or request.args.get('q'):
        query_text = request.form.get('q') or request.args.get('q', '')
        
        if query_text:
            # Search in patient name (via user), email, phone, or ID
            results = Patient.query.join(User).filter(
                or_(
                    User.username.ilike(f'%{query_text}%'),
                    User.email.ilike(f'%{query_text}%'),
                    Patient.phone.ilike(f'%{query_text}%'),
                    Patient.alternate_phone.ilike(f'%{query_text}%'),
                    Patient.id == query_text if query_text.isdigit() else False
                )
            ).all()
    
    return render_template('admin/search_patients.html', results=results, query=query_text)

@admin_bp.route('/search/doctors', methods=['GET', 'POST'])
@admin_required
def search_doctors():
    """Search doctors by name or specialization"""
    results = []
    query_text = ''
    
    if request.method == 'POST' or request.args.get('q'):
        query_text = request.form.get('q') or request.args.get('q', '')
        
        if query_text:
            # Search in doctor name (via user) or specialization
            results = Doctor.query.join(User).filter(
                or_(
                    User.username.ilike(f'%{query_text}%'),
                    Doctor.specialization.ilike(f'%{query_text}%'),
                    Doctor.qualification.ilike(f'%{query_text}%')
                )
            ).all()
    
    return render_template('admin/search_doctors.html', results=results, query=query_text)

@admin_bp.route('/doctor/<int:doctor_id>/toggle-status', methods=['POST'])
@admin_required
def toggle_doctor_status(doctor_id):
    """Enable/disable doctor account"""
    doctor = Doctor.query.get_or_404(doctor_id)
    user = doctor.user
    
    try:
        user.is_active = not user.is_active
        db.session.commit()
        
        status = "enabled" if user.is_active else "disabled"
        flash(f'✅ Doctor "{user.username}" has been {status}.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating doctor status: {str(e)}', 'danger')
    
    return redirect(url_for('admin.doctors'))

@admin_bp.route('/doctor/<int:doctor_id>/remove', methods=['POST'])
@admin_required
def remove_doctor(doctor_id):
    """Permanently remove doctor from system"""
    doctor = Doctor.query.get_or_404(doctor_id)
    user = doctor.user
    
    try:
        # Delete doctor profile first
        db.session.delete(doctor)
        # Delete user account
        db.session.delete(user)
        db.session.commit()
        
        flash(f'✅ Doctor "{user.username}" has been permanently removed from the system.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error removing doctor: {str(e)}', 'danger')
    
    return redirect(url_for('admin.doctors'))

@admin_bp.route('/patient/<int:patient_id>/toggle-status', methods=['POST'])
@admin_required
def toggle_patient_status(patient_id):
    """Enable/disable patient account"""
    patient = Patient.query.get_or_404(patient_id)
    user = patient.user
    
    try:
        user.is_active = not user.is_active
        db.session.commit()
        
        status = "enabled" if user.is_active else "disabled"
        flash(f'✅ Patient "{user.username}" has been {status}.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating patient status: {str(e)}', 'danger')
    
    return redirect(url_for('admin.patients'))

@admin_bp.route('/patient/<int:patient_id>/remove', methods=['POST'])
@admin_required
def remove_patient(patient_id):
    """Permanently remove patient from system"""
    patient = Patient.query.get_or_404(patient_id)
    user = patient.user
    
    try:
        # Delete patient profile first
        db.session.delete(patient)
        # Delete user account
        db.session.delete(user)
        db.session.commit()
        
        flash(f'✅ Patient "{user.username}" has been permanently removed from the system.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error removing patient: {str(e)}', 'danger')
    
    return redirect(url_for('admin.patients'))

@admin_bp.route('/patient/<int:patient_id>/treatments')
@login_required
@admin_required
def patient_treatments(patient_id):
    """View all treatment records for a specific patient"""
    patient = Patient.query.get_or_404(patient_id)
    treatments = Treatment.query.filter_by(patient_id=patient_id).order_by(Treatment.created_at.desc()).all()
    
    return render_template('admin/patient_treatments.html', patient=patient, treatments=treatments)

@admin_bp.route('/treatments')
@login_required
@admin_required
def all_treatments():
    """View all treatment records in the system"""
    page = request.args.get('page', 1, type=int)
    treatments = Treatment.query.order_by(Treatment.created_at.desc()).paginate(page=page, per_page=15)
    
    return render_template('admin/treatments.html', treatments=treatments)
