#!/usr/bin/env python
"""
Milestone 0 Registration Verification Script
Checks that all required files and functionality are present
"""

import os
import sys
from pathlib import Path

def check_files():
    """Check if all required documentation files exist"""
    print("\n" + "="*60)
    print("MILESTONE 0 REGISTRATION VERIFICATION")
    print("="*60)
    
    required_files = [
        '.gitignore',
        'README.md',
        'PROJECT_REGISTRATION.md',
        'SETUP_COMPLETE.md',
        'CODE_OVERVIEW.md',
        'GIT_TRACKER_REGISTRATION.md',
        'MILESTONE_0_SUMMARY.md',
        'app.py',
        'config.py',
        'requirements.txt',
    ]
    
    required_dirs = [
        'models',
        'routes',
        'templates',
        'static',
        'utils',
    ]
    
    print("\n📄 Checking Documentation Files...")
    docs_ok = True
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - MISSING")
            docs_ok = False
    
    print("\n📁 Checking Directory Structure...")
    dirs_ok = True
    for dir in required_dirs:
        if os.path.isdir(dir):
            print(f"   ✅ {dir}/")
        else:
            print(f"   ❌ {dir}/ - MISSING")
            dirs_ok = False
    
    return docs_ok and dirs_ok

def check_git():
    """Check if Git is initialized"""
    print("\n🔧 Checking Git Configuration...")
    
    if os.path.isdir('.git'):
        print("   ✅ Git repository initialized")
        
        # Check for commits
        try:
            result = os.popen('git log --oneline -n 1').read().strip()
            if result:
                print(f"   ✅ Commits present: {result[:50]}...")
                return True
            else:
                print("   ❌ No commits found - Run: git commit -m 'Initial commit'")
                return False
        except:
            print("   ⚠️  Could not verify commits (Git might not be installed)")
            return True
    else:
        print("   ⚠️  Git not initialized - Run: git init && git add . && git commit -m 'Initial commit'")
        return False

def check_requirements():
    """Check if requirements.txt has necessary dependencies"""
    print("\n📦 Checking Dependencies...")
    
    required_packages = ['Flask', 'SQLAlchemy', 'Flask-Login', 'Werkzeug']
    
    with open('requirements.txt', 'r') as f:
        content = f.read().lower()
    
    all_present = True
    for package in required_packages:
        if package.lower() in content:
            print(f"   ✅ {package}")
        else:
            print(f"   ❌ {package} - MISSING from requirements.txt")
            all_present = False
    
    return all_present

def check_models():
    """Check if all models are present"""
    print("\n🗄️  Checking Database Models...")
    
    required_models = [
        'user.py',
        'doctor.py',
        'patient.py',
        'department.py',
        'appointment.py',
        'treatment.py',
    ]
    
    all_present = True
    for model in required_models:
        model_path = os.path.join('models', model)
        if os.path.exists(model_path):
            print(f"   ✅ {model}")
        else:
            print(f"   ❌ {model} - MISSING")
            all_present = False
    
    return all_present

def check_routes():
    """Check if all routes are present"""
    print("\n🛣️  Checking Routes...")
    
    required_routes = [
        'auth.py',
        'doctor.py',
        'patient.py',
        'admin.py',
    ]
    
    all_present = True
    for route in required_routes:
        route_path = os.path.join('routes', route)
        if os.path.exists(route_path):
            print(f"   ✅ {route}")
        else:
            print(f"   ❌ {route} - MISSING")
            all_present = False
    
    return all_present

def check_templates():
    """Check if templates exist"""
    print("\n📄 Checking Templates...")
    
    required_templates = [
        'base.html',
        'index.html',
        'login.html',
        'register.html',
    ]
    
    all_present = True
    for template in required_templates:
        template_path = os.path.join('templates', template)
        if os.path.exists(template_path):
            print(f"   ✅ {template}")
        else:
            print(f"   ❌ {template} - MISSING")
            all_present = False
    
    return all_present

def main():
    """Run all checks"""
    checks = {
        'Documentation Files': check_files(),
        'Git Repository': check_git(),
        'Dependencies': check_requirements(),
        'Database Models': check_models(),
        'Routes': check_routes(),
        'Templates': check_templates(),
    }
    
    print("\n" + "="*60)
    print("REGISTRATION READINESS SUMMARY")
    print("="*60)
    
    all_passed = True
    for check_name, result in checks.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name:.<40} {status}")
        if not result:
            all_passed = False
    
    print("="*60)
    
    if all_passed:
        print("\n🎉 ALL CHECKS PASSED - READY FOR REGISTRATION! 🎉")
        print("\nNext Steps:")
        print("1. Read: GIT_TRACKER_REGISTRATION.md")
        print("2. Test: python app.py")
        print("3. Verify: python test_doctor_login_manual.py")
        print("4. Register on Git Tracker")
        print("5. Submit for Milestone 0 evaluation")
        return 0
    else:
        print("\n⚠️  SOME CHECKS FAILED - PLEASE FIX ISSUES ABOVE")
        print("\nCommon Fixes:")
        print("- Missing files: Create them from documentation")
        print("- Git issues: Run: git init && git add . && git commit -m 'Initial commit'")
        print("- Dependencies: Run: pip install -r requirements.txt")
        return 1

if __name__ == '__main__':
    sys.exit(main())
