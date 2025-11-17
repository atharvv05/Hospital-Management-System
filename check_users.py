from app import create_app, db
from models.user import User
from models.patient import Patient
from models.doctor import Doctor

app = create_app()
with app.app_context():
    users = User.query.all()
    print(f'\nTotal registered users: {len(users)}\n')
    
    for user in users:
        print(f'Username: {user.username}')
        print(f'Email: {user.email}')
        print(f'Role: {user.role}')
        print(f'Active: {user.is_active}')
        print(f'Created: {user.created_at}')
        
        # Show role-specific info
        if user.role == 'patient':
            patient = Patient.query.filter_by(user_id=user.id).first()
            if patient:
                print(f'Patient ID: {patient.id}')
        elif user.role == 'doctor':
            doctor = Doctor.query.filter_by(user_id=user.id).first()
            if doctor:
                print(f'Doctor ID: {doctor.id}')
                print(f'Department ID: {doctor.department_id}')
        
        print('-' * 60)
