from app import db

class Doctor(db.Model):
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    phone = db.Column(db.String(20))
    license_number = db.Column(db.String(50), unique=True)
    experience_years = db.Column(db.Integer)
    qualification = db.Column(db.String(200))
    specialization = db.Column(db.String(100))
    bio = db.Column(db.Text)
    consultation_fees = db.Column(db.Float, default=500.0)
    rating = db.Column(db.Float, default=0.0)
    total_patients = db.Column(db.Integer, default=0)
    total_appointments = db.Column(db.Integer, default=0)
    is_available = db.Column(db.Boolean, default=True)
    clinic_name = db.Column(db.String(100))
    working_days = db.Column(db.String(100))  # e.g., "Mon-Fri"
    morning_slot_start = db.Column(db.String(10), default="09:00")
    morning_slot_end = db.Column(db.String(10), default="12:00")
    evening_slot_start = db.Column(db.String(10), default="15:00")
    evening_slot_end = db.Column(db.String(10), default="18:00")
    avg_consultation_time = db.Column(db.Integer, default=30)  # in minutes
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    user = db.relationship('User', backref='doctor_profile')
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)
    treatments = db.relationship('Treatment', backref='doctor', lazy=True)
    availabilities = db.relationship('DoctorAvailability', backref='doctor', lazy=True)
