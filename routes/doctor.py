from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models.doctor import Doctor
from models.appointment import Appointment
from models.treatment import Treatment
from models.patient import Patient

doctor_bp = Blueprint('doctor', __name__, url_prefix='/doctor')

def doctor_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'doctor':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@doctor_bp.route('/dashboard')
@doctor_required
def dashboard():
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    if not doctor:
        # Create doctor profile if it doesn't exist (safety fallback)
        from models.department import Department
        default_dept = Department.query.first()
        if default_dept:
            doctor = Doctor(user_id=current_user.id, department_id=default_dept.id)
            db.session.add(doctor)
            db.session.commit()
        else:
            flash('Error: No departments found. Please contact administrator.', 'danger')
            return redirect(url_for('auth.logout'))
    
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).all() if doctor.id else []
    
    return render_template('doctor/dashboard.html', 
                         doctor=doctor, 
                         appointments=appointments)

@doctor_bp.route('/appointments')
@login_required
@doctor_required
def appointments():
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
    
    return render_template('doctor/appointments.html', appointments=appointments)

@doctor_bp.route('/treatment/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
@doctor_required
def add_treatment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    
    if request.method == 'POST':
        diagnosis = request.form.get('diagnosis')
        prescription = request.form.get('prescription')
        notes = request.form.get('notes')
        
        treatment = Treatment(appointment_id=appointment_id,
                            patient_id=appointment.patient_id,
                            doctor_id=appointment.doctor_id,
                            diagnosis=diagnosis,
                            prescription=prescription,
                            notes=notes)
        
        appointment.status = 'Completed'
        db.session.add(treatment)
        db.session.commit()
        
        flash('Treatment record added successfully', 'success')
        return redirect(url_for('doctor.appointments'))
    
    return render_template('doctor/treatment.html', appointment=appointment)

@doctor_bp.route('/patients')
@login_required
@doctor_required
def patients():
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
    patients = list(set([appointment.patient for appointment in appointments]))
    
    return render_template('doctor/patients.html', patients=patients)

@doctor_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@doctor_required
def profile():
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        doctor.phone = request.form.get('phone')
        doctor.bio = request.form.get('bio')
        current_user.email = request.form.get('email')
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('doctor.profile'))
    
    return render_template('doctor/profile.html', doctor=doctor)
