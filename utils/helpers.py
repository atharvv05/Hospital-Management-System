# Utility functions for the application

def get_user_role(user):
    """Get the role of a user"""
    return user.role if user else None

def is_admin(user):
    """Check if user is admin"""
    return user and user.role == 'admin'

def is_doctor(user):
    """Check if user is doctor"""
    return user and user.role == 'doctor'

def is_patient(user):
    """Check if user is patient"""
    return user and user.role == 'patient'
