# Database initialization module
# Models are automatically created when app.py is run

from app import db
from models.user import User
from models.doctor import Doctor
from models.patient import Patient
from models.appointment import Appointment
from models.treatment import Treatment
from models.department import Department

def init_db():
    """Initialize database"""
    db.create_all()
