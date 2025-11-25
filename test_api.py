"""
Test script for Hospital Management System API
Tests all endpoints with proper authentication
"""

import requests
import json
from datetime import datetime, timedelta
import sys

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:5000"
API_URL = f"{BASE_URL}/api"

# Test credentials (assuming these exist in your database)
ADMIN_CREDENTIALS = {"email": "admin@hospital.com", "password": "admin123"}
DOCTOR_CREDENTIALS = {"email": "doctor@hospital.com", "password": "doctor123"}
PATIENT_CREDENTIALS = {"email": "patient@hospital.com", "password": "patient123"}

class APITester:
    def __init__(self):
        self.session = requests.Session()
        self.results = []
    
    def log(self, message, status="INFO"):
        print(f"[{status}] {message}")
        self.results.append({"message": message, "status": status})
    
    def login(self, credentials, role_name):
        """Login and establish session"""
        try:
            # First get the login page to establish session
            self.session.get(f"{BASE_URL}/auth/login")
            
            # Then post credentials
            response = self.session.post(
                f"{BASE_URL}/auth/login",
                data=credentials,
                allow_redirects=True
            )
            
            # Check if we were redirected to a dashboard (successful login)
            if response.status_code == 200 and ('dashboard' in response.url or 'Dashboard' in response.text):
                self.log(f"✅ Logged in as {role_name}", "SUCCESS")
                return True
            else:
                self.log(f"❌ Login failed for {role_name}: {response.status_code}, URL: {response.url}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Login error for {role_name}: {str(e)}", "ERROR")
            return False
    
    def test_get(self, endpoint, expected_status=200, description=""):
        """Test GET request"""
        try:
            response = self.session.get(f"{API_URL}{endpoint}")
            if response.status_code == expected_status:
                self.log(f"✅ GET {endpoint} - {description or 'Success'}", "SUCCESS")
                return response.json() if response.content else None
            else:
                self.log(f"❌ GET {endpoint} - Expected {expected_status}, got {response.status_code}", "ERROR")
                return None
        except Exception as e:
            self.log(f"❌ GET {endpoint} - Error: {str(e)}", "ERROR")
            return None
    
    def test_post(self, endpoint, data, expected_status=201, description=""):
        """Test POST request"""
        try:
            response = self.session.post(
                f"{API_URL}{endpoint}",
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code == expected_status:
                self.log(f"✅ POST {endpoint} - {description or 'Success'}", "SUCCESS")
                return response.json() if response.content else None
            else:
                self.log(f"❌ POST {endpoint} - Expected {expected_status}, got {response.status_code}: {response.text[:200]}", "ERROR")
                return None
        except Exception as e:
            self.log(f"❌ POST {endpoint} - Error: {str(e)}", "ERROR")
            return None
    
    def test_put(self, endpoint, data, expected_status=200, description=""):
        """Test PUT request"""
        try:
            response = self.session.put(
                f"{API_URL}{endpoint}",
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code == expected_status:
                self.log(f"✅ PUT {endpoint} - {description or 'Success'}", "SUCCESS")
                return response.json() if response.content else None
            else:
                self.log(f"❌ PUT {endpoint} - Expected {expected_status}, got {response.status_code}: {response.text[:200]}", "ERROR")
                return None
        except Exception as e:
            self.log(f"❌ PUT {endpoint} - Error: {str(e)}", "ERROR")
            return None
    
    def test_delete(self, endpoint, expected_status=200, description=""):
        """Test DELETE request"""
        try:
            response = self.session.delete(f"{API_URL}{endpoint}")
            if response.status_code == expected_status:
                self.log(f"✅ DELETE {endpoint} - {description or 'Success'}", "SUCCESS")
                return response.json() if response.content else None
            else:
                self.log(f"❌ DELETE {endpoint} - Expected {expected_status}, got {response.status_code}", "ERROR")
                return None
        except Exception as e:
            self.log(f"❌ DELETE {endpoint} - Error: {str(e)}", "ERROR")
            return None
    
    def run_tests(self):
        """Run comprehensive API tests"""
        print("\n" + "="*60)
        print("HOSPITAL MANAGEMENT SYSTEM - API TESTS")
        print("="*60 + "\n")
        
        # Test 1: Unauthenticated Access (should fail)
        print("\n--- TEST 1: Unauthenticated Access ---")
        self.test_get("/doctors", expected_status=401, description="Should require authentication")
        self.test_get("/patients", expected_status=401, description="Should require authentication")
        self.test_get("/appointments", expected_status=401, description="Should require authentication")
        
        # Test 2: Admin Access
        print("\n--- TEST 2: Admin Access ---")
        if self.login(ADMIN_CREDENTIALS, "Admin"):
            # Get all doctors
            doctors_data = self.test_get("/doctors", description="List all doctors")
            if doctors_data:
                print(f"   Found {doctors_data['data']['pagination']['total']} doctors")
            
            # Get all patients
            patients_data = self.test_get("/patients", description="List all patients")
            if patients_data:
                print(f"   Found {patients_data['data']['pagination']['total']} patients")
            
            # Get all appointments
            appointments_data = self.test_get("/appointments", description="List all appointments")
            if appointments_data:
                print(f"   Found {appointments_data['data']['pagination']['total']} appointments")
            
            # Get stats
            stats_data = self.test_get("/stats", description="Get system statistics")
            if stats_data:
                print(f"   System Stats: {stats_data['data']['doctors']['total']} doctors, {stats_data['data']['patients']['total']} patients")
            
            # Test creating a patient (POST)
            new_patient_data = {
                "username": f"test_patient_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "email": f"testpatient{datetime.now().strftime('%Y%m%d%H%M%S')}@test.com",
                "password": "test123",
                "phone": "1234567890",
                "blood_group": "O+"
            }
            created_patient = self.test_post("/patients", new_patient_data, description="Create new patient")
            
            if created_patient and 'data' in created_patient:
                patient_id = created_patient['data']['id']
                
                # Test updating patient (PUT)
                update_data = {"phone": "9876543210", "city": "Mumbai"}
                self.test_put(f"/patients/{patient_id}", update_data, description="Update patient")
                
                # Test getting single patient
                self.test_get(f"/patients/{patient_id}", description="Get patient details")
        
        # Logout admin
        self.session = requests.Session()
        
        # Test 3: Doctor Access
        print("\n--- TEST 3: Doctor Access ---")
        if self.login(DOCTOR_CREDENTIALS, "Doctor"):
            # Doctors should see their appointments
            self.test_get("/appointments", description="List doctor's appointments")
            
            # Doctors should see their patients
            self.test_get("/patients", description="List doctor's patients")
            
            # Doctors cannot access stats
            self.test_get("/stats", expected_status=403, description="Should deny access to stats")
            
            # Doctors cannot create patients
            self.test_post("/patients", {"username": "test", "email": "test@test.com", "password": "test"}, 
                          expected_status=403, description="Should deny patient creation")
        
        # Logout doctor
        self.session = requests.Session()
        
        # Test 4: Patient Access
        print("\n--- TEST 4: Patient Access ---")
        if self.login(PATIENT_CREDENTIALS, "Patient"):
            # Patients should see only their appointments
            self.test_get("/appointments", description="List patient's appointments")
            
            # Patients should see only themselves
            patients_data = self.test_get("/patients", description="Get patient profile")
            if patients_data and patients_data['data']['pagination']['total'] == 1:
                print("   ✓ Patient can only see their own profile")
            
            # Patients can see doctors
            self.test_get("/doctors", description="List all doctors")
            
            # Patients cannot access stats
            self.test_get("/stats", expected_status=403, description="Should deny access to stats")
        
        # Test 5: Appointment Conflict Prevention
        print("\n--- TEST 5: Appointment Conflict Prevention ---")
        self.session = requests.Session()
        if self.login(ADMIN_CREDENTIALS, "Admin"):
            # Try to create two appointments at the same time
            tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            
            appointment_data = {
                "patient_id": 1,
                "doctor_id": 1,
                "appointment_date": tomorrow,
                "appointment_time": "10:00",
                "appointment_type": "Regular"
            }
            
            # First appointment should succeed
            first_apt = self.test_post("/appointments", appointment_data, description="Create first appointment")
            
            if first_apt:
                # Second appointment at same time should fail
                self.test_post("/appointments", appointment_data, expected_status=400, 
                             description="Prevent double booking")
        
        # Print summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        success_count = len([r for r in self.results if r['status'] == 'SUCCESS'])
        error_count = len([r for r in self.results if r['status'] == 'ERROR'])
        total_count = len(self.results)
        
        print(f"\nTotal Tests: {total_count}")
        print(f"✅ Passed: {success_count}")
        print(f"❌ Failed: {error_count}")
        print(f"Success Rate: {(success_count/total_count)*100:.1f}%\n")

if __name__ == "__main__":
    tester = APITester()
    tester.run_tests()
