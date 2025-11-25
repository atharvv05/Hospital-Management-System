import sys
from flask import Flask

# Ensure `import app` returns this module object (avoid duplicate module instances)
sys.modules['app'] = sys.modules.get(__name__)
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

# If this file is executed as a script, ensure imports of `app` (from other modules)
# resolve to this same module instance. This avoids creating two different
# module objects (one as __main__ and another as 'app') which can cause
# Flask-SQLAlchemy to think the current app isn't registered.
if __name__ == "__main__":
    sys.modules.setdefault('app', sys.modules.get('__main__'))

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hospital-management-system-secret-key-2025'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['REMEMBER_COOKIE_DURATION'] = 86400 * 7  # 7 days
    app.config['REMEMBER_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
    app.config['PERMANENT_SESSION_LIFETIME'] = 86400 * 7  # 7 days
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    with app.app_context():
        # Import models after app context
        from models.user import User
        from models.department import Department
        from models.doctor import Doctor
        from models.patient import Patient
        from models.appointment import Appointment
        from models.treatment import Treatment, DoctorAvailability
        
        # Create all tables
        db.create_all()
        
        # Create default departments if they don't exist
        if db.session.query(Department).count() == 0:
            departments_data = [
                {'name': 'Cardiology', 'description': 'Heart and cardiovascular diseases'},
                {'name': 'Neurology', 'description': 'Brain and nervous system'},
                {'name': 'Orthopedics', 'description': 'Bones and joints'},
                {'name': 'Dermatology', 'description': 'Skin conditions'},
                {'name': 'Pediatrics', 'description': 'Child health and development'},
            ]
            for dept_data in departments_data:
                dept = Department(name=dept_data['name'], description=dept_data['description'])
                db.session.add(dept)
            db.session.commit()
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.doctor import doctor_bp
    from routes.patient import patient_bp
    from routes.api import api_bp
    # Debug routes (local-only)
    from routes.debug import debug_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(debug_bp)
    
    @login_manager.user_loader
    def load_user(user_id):
        from models.user import User
        return db.session.query(User).get(int(user_id))
    
    @app.route('/')
    def index():
        from flask_login import current_user
        from flask import render_template
        return render_template('index.html')
    
    return app

app = create_app()

if __name__ == '__main__':
    # Run without the reloader during automated tests to avoid double-import issues
    app.run(debug=False, host='localhost', port=5000)
