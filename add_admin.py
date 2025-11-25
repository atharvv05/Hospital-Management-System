#!/usr/bin/env python
"""
Script to add a new admin user to the Hospital Management System
Usage: python add_admin.py
"""

import sys
from app import create_app, db
from models.user import User

def add_admin(username, email, password):
    """Add a new admin user to the database"""
    app = create_app()
    
    with app.app_context():
        # Check if username already exists
        if User.query.filter_by(username=username).first():
            print(f"❌ Error: Username '{username}' already exists!")
            return False
        
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            print(f"❌ Error: Email '{email}' already registered!")
            return False
        
        # Validate password
        if len(password) < 6:
            print("❌ Error: Password must be at least 6 characters long!")
            return False
        
        try:
            # Create new admin user
            admin = User(
                username=username,
                email=email,
                role='admin',
                is_active=True
            )
            admin.set_password(password)
            
            db.session.add(admin)
            db.session.commit()
            
            print(f"✅ Admin user created successfully!")
            print(f"   Username: {username}")
            print(f"   Email: {email}")
            print(f"   Role: admin")
            print(f"\n🔐 Login with these credentials:")
            print(f"   URL: http://localhost:5000/auth/login")
            print(f"   Username: {username}")
            print(f"   Password: {password}")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creating admin: {str(e)}")
            return False

def interactive_add_admin():
    """Interactive mode to add admin"""
    print("\n" + "="*50)
    print("🏥 Hospital Management System - Add Admin")
    print("="*50)
    
    username = input("\nEnter username: ").strip()
    if not username:
        print("❌ Username cannot be empty!")
        return False
    
    if len(username) < 3:
        print("❌ Username must be at least 3 characters!")
        return False
    
    email = input("Enter email: ").strip()
    if not email or '@' not in email:
        print("❌ Invalid email address!")
        return False
    
    password = input("Enter password (min 6 chars): ").strip()
    if not password:
        print("❌ Password cannot be empty!")
        return False
    
    if len(password) < 6:
        print("❌ Password must be at least 6 characters!")
        return False
    
    confirm_password = input("Confirm password: ").strip()
    if password != confirm_password:
        print("❌ Passwords do not match!")
        return False
    
    print("\n⏳ Creating admin user...")
    return add_admin(username, email, password)

if __name__ == '__main__':
    if len(sys.argv) > 3:
        # Command line mode: python add_admin.py <username> <email> <password>
        username = sys.argv[1]
        email = sys.argv[2]
        password = sys.argv[3]
        add_admin(username, email, password)
    else:
        # Interactive mode
        interactive_add_admin()
