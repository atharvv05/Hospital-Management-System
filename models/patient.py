from app import db

class Patient(db.Model):
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    phone = db.Column(db.String(20))
    alternate_phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    blood_group = db.Column(db.String(5))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    pincode = db.Column(db.String(10))
    medical_history = db.Column(db.Text)
    allergies = db.Column(db.Text)
    insurance_provider = db.Column(db.String(100))
    insurance_id = db.Column(db.String(50))
    emergency_contact = db.Column(db.String(20))
    emergency_contact_name = db.Column(db.String(100))
    enable_notifications = db.Column(db.Boolean, default=True)
    notification_preference = db.Column(db.String(50), default='email')  # email, sms, whatsapp
    last_visit = db.Column(db.DateTime)
    total_visits = db.Column(db.Integer, default=0)
    total_spent = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    user = db.relationship('User', backref='patient_profile')
    appointments = db.relationship('Appointment', backref='patient', lazy=True)
    treatments = db.relationship('Treatment', backref='patient', lazy=True)
