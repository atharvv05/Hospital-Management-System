import requests
import random

username = f'doc{random.randint(1000, 9999)}'
email = f'doc{random.randint(1000, 9999)}@test.com'

session = requests.Session()

# Register
reg_data = {
    'username': username,
    'email': email,
    'password': 'pass123',
    'confirm_password': 'pass123',
    'role': 'doctor',
    'department_id': '1'
}

reg = session.post('http://localhost:5000/auth/register', data=reg_data, allow_redirects=False)
print(f'Registration: {reg.status_code}')
print(f'Redirect to: {reg.headers.get("Location", "N/A")}')

# Get success page
success = session.get('http://localhost:5000/auth/register/success')
print(f'Success page: {success.status_code}')

# Login
login_data = {'username': username, 'password': 'pass123', 'role': 'doctor'}
login = session.post('http://localhost:5000/auth/login', data=login_data, allow_redirects=False)
print(f'Login: {login.status_code}')
print(f'Redirect to: {login.headers.get("Location", "N/A")}')

# Try to access dashboard
dash_url = login.headers.get('Location', 'http://localhost:5000/doctor/dashboard')
if not dash_url.startswith('http'):
    dash_url = 'http://localhost:5000' + dash_url
    
dash = session.get(dash_url)
print(f'Dashboard: {dash.status_code}')
print(f'Dashboard contains doctor content: {"Doctor" in dash.text}')

if dash.status_code != 200:
    print(f"ERROR: Dashboard returned {dash.status_code}")
    print(f"Response text: {dash.text[:200]}")
