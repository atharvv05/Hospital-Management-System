from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from models.user import User
from models.patient import Patient
from models.doctor import Doctor

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role', 'patient')
        
        # Validate role
        if role not in ['admin', 'doctor', 'patient']:
            flash('Invalid role selected', 'danger')
            return redirect(url_for('auth.login'))
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.is_active:
            # Verify role matches
            if user.role != role:
                flash(f'Your account is registered as {user.role.capitalize()}. Please select the correct role.', 'warning')
                return redirect(url_for('auth.login'))
            
            # Login user with remember flag to persist session
            login_user(user, remember=True)
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user.role == 'doctor':
                return redirect(url_for('doctor.dashboard'))
            else:
                return redirect(url_for('patient.dashboard'))
        else:
            flash('Invalid credentials or role mismatch', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    from models.department import Department
    
    # Fetch departments for dropdown
    departments = Department.query.all()
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role', 'patient')
        department_id = request.form.get('department_id')
        
        # Validate role
        if role not in ['admin', 'doctor', 'patient']:
            flash('Invalid role selected', 'danger')
            return redirect(url_for('auth.register'))
        
        # Validate department for doctors
        if role == 'doctor':
            if not department_id:
                flash('Please select a department/specialization', 'danger')
                return redirect(url_for('auth.register'))
            try:
                department_id = int(department_id)
                dept = Department.query.get(department_id)
                if not dept:
                    flash('Invalid department selected', 'danger')
                    return redirect(url_for('auth.register'))
            except (ValueError, TypeError):
                flash('Invalid department selection', 'danger')
                return redirect(url_for('auth.register'))
        
        # Check password match
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('auth.register'))
        
        # Check password strength
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'danger')
            return redirect(url_for('auth.register'))
        
        # Check if username exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose another.', 'danger')
            return redirect(url_for('auth.register'))
        
        # Check if email exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please login or use another email.', 'danger')
            return redirect(url_for('auth.register'))
        
        try:
            # Create user account
            user = User(username=username, email=email, role=role, is_active=True)
            user.set_password(password)
            db.session.add(user)
            db.session.flush()  # Get the user ID without committing
            
            # Create role-specific profile
            if role == 'patient':
                patient = Patient(user_id=user.id)
                db.session.add(patient)
            elif role == 'doctor':
                doctor = Doctor(user_id=user.id, department_id=department_id)
                db.session.add(doctor)
            # Admin doesn't need a separate profile
            
            db.session.commit()
            
            # Store data in session for success page
            session['reg_success'] = {
                'username': username,
                'email': email,
                'role': role
            }
            
            return redirect(url_for('auth.register_success'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed: {str(e)}', 'danger')
            return redirect(url_for('auth.register'))
    
    return render_template('register.html', departments=departments)

@auth_bp.route('/register/success')
def register_success():
    # Get data from session
    reg_data = session.get('reg_success')
    
    if not reg_data:
        flash('Invalid access. Please register again.', 'warning')
        return redirect(url_for('auth.register'))
    
    username = reg_data.get('username')
    email = reg_data.get('email')
    role = reg_data.get('role')
    
    # Clear the session data after displaying
    session.pop('reg_success', None)
    
    return render_template('register_success.html', username=username, email=email, role=role)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
