from app import db

class Treatment(db.Model):
    __tablename__ = 'treatments'
    
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    diagnosis = db.Column(db.Text)
    icd_code = db.Column(db.String(20))  # International Classification of Diseases
    prescription = db.Column(db.Text)
    medicine_details = db.Column(db.Text)
    dosage_instructions = db.Column(db.Text)
    duration_days = db.Column(db.Integer)
    follow_up_required = db.Column(db.Boolean, default=False)
    follow_up_days = db.Column(db.Integer)
    lab_tests_recommended = db.Column(db.Text)
    notes = db.Column(db.Text)
    consultation_duration = db.Column(db.Integer)  # in minutes
    status = db.Column(db.String(20), default='Active')  # Active, Completed, Archived
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    appointment = db.relationship('Appointment', backref='treatment')

class DoctorAvailability(db.Model):
    __tablename__ = 'doctor_availabilities'
    
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.String(10))
    end_time = db.Column(db.String(10))
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
