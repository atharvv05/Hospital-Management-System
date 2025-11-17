from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models.patient import Patient
from models.doctor import Doctor
from models.department import Department
from models.appointment import Appointment
from models.treatment import Treatment
from datetime import datetime, timedelta

patient_bp = Blueprint('patient', __name__, url_prefix='/patient')

def patient_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'patient':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@patient_bp.route('/dashboard')
@patient_required
def dashboard():
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    departments = Department.query.all()
    
    return render_template('patient/dashboard.html', 
                         patient=patient, 
                         departments=departments,
                         user=current_user)

@patient_bp.route('/search-doctors')
@login_required
@patient_required
def search_doctors():
    department_id = request.args.get('department_id')
    doctors = Doctor.query.filter_by(department_id=department_id).all() if department_id else []
    
    return render_template('patient/search_doctors.html', doctors=doctors)

@patient_bp.route('/book-appointment/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
@patient_required
def book_appointment(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        appointment_date = request.form.get('appointment_date')
        appointment_time = request.form.get('appointment_time')
        
        existing = Appointment.query.filter_by(
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status='Booked'
        ).first()
        
        if existing:
            flash('Time slot already booked', 'danger')
            return redirect(url_for('patient.book_appointment', doctor_id=doctor_id))
        
        appointment = Appointment(patient_id=patient.id,
                                 doctor_id=doctor_id,
                                 appointment_date=appointment_date,
                                 appointment_time=appointment_time)
        
        db.session.add(appointment)
        db.session.commit()
        
        flash('Appointment booked successfully', 'success')
        return redirect(url_for('patient.my_appointments'))
    
    return render_template('patient/book_appointment.html', doctor=doctor)

@patient_bp.route('/my-appointments')
@login_required
@patient_required
def my_appointments():
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    appointments = Appointment.query.filter_by(patient_id=patient.id).all()
    
    return render_template('patient/appointments.html', appointments=appointments)

@patient_bp.route('/treatment-history')
@login_required
@patient_required
def treatment_history():
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    treatments = Treatment.query.filter_by(patient_id=patient.id).all()
    
    return render_template('patient/treatment_history.html', treatments=treatments)

@patient_bp.route('/cancel-appointment/<int:appointment_id>')
@login_required
@patient_required
def cancel_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    appointment.status = 'Cancelled'
    db.session.commit()
    
    flash('Appointment cancelled', 'success')
    return redirect(url_for('patient.my_appointments'))

@patient_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@patient_required
def profile():
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        patient.phone = request.form.get('phone')
        patient.date_of_birth = request.form.get('date_of_birth')
        patient.gender = request.form.get('gender')
        patient.blood_group = request.form.get('blood_group')
        patient.address = request.form.get('address')
        current_user.email = request.form.get('email')
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('patient.profile'))
    
    return render_template('patient/profile.html', patient=patient)
