from app import db
from datetime import datetime

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default='Booked')  # Booked, Completed, Cancelled, No-show
    notes = db.Column(db.Text)
    queue_position = db.Column(db.Integer)  # For queue management
    reminder_sent = db.Column(db.Boolean, default=False)
    appointment_type = db.Column(db.String(50), default='Regular')  # Regular, Follow-up, Emergency
    consultation_fees = db.Column(db.Float, default=0.0)
    payment_status = db.Column(db.String(20), default='Pending')  # Pending, Paid, Insurance
    is_confirmed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def is_upcoming(self):
        from datetime import datetime as dt
        app_datetime = dt.strptime(f"{self.appointment_date} {self.appointment_time}", "%Y-%m-%d %H:%M")
        return app_datetime > dt.now()
