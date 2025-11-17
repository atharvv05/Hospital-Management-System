import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

# Create session with retry strategy
session = requests.Session()
retry_strategy = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

print("=" * 60)
print("Testing Doctor Login Flow with Cookies")
print("=" * 60)

# 1. Register doctor
print("\n1. Registering doctor...")
reg_data = {
    'username': 'testdoc_manual',
    'email': 'testdoc_manual@test.com',
    'password': 'testpass123',
    'confirm_password': 'testpass123',
    'role': 'doctor',
    'department_id': '1'
}

reg = session.post('http://localhost:5000/auth/register', data=reg_data, allow_redirects=False)
print(f"   Status: {reg.status_code}")
print(f"   Redirect: {reg.headers.get('Location', 'N/A')}")
print(f"   Cookies set: {len(session.cookies)}")

# 2. Visit success page
print("\n2. Visiting success page...")
success = session.get('http://localhost:5000/auth/register/success', allow_redirects=False)
print(f"   Status: {success.status_code}")

# 3. Now login
print("\n3. Logging in as doctor...")
login_data = {
    'username': 'testdoc_manual',
    'password': 'testpass123',
    'role': 'doctor'
}

login = session.post('http://localhost:5000/auth/login', data=login_data, allow_redirects=False)
print(f"   Status: {login.status_code}")
print(f"   Redirect to: {login.headers.get('Location', 'N/A')}")
print(f"   Session cookies: {session.cookies}")

# 4. Check if we have session cookie
if session.cookies:
    print(f"\n   Cookie details:")
    for cookie in session.cookies:
        print(f"   - {cookie.name}: {cookie.value[:20]}...")

# 5. Follow the redirect
print("\n4. Following redirect to dashboard...")
redirect_url = login.headers.get('Location')
if redirect_url:
    if not redirect_url.startswith('http'):
        redirect_url = 'http://localhost:5000' + redirect_url
    
    dashboard = session.get(redirect_url, allow_redirects=False)
    print(f"   Status: {dashboard.status_code}")
    
    if dashboard.status_code == 200:
        print(f"   ✓ Successfully loaded dashboard")
        print(f"   Content length: {len(dashboard.text)}")
        if 'doctor' in dashboard.text.lower():
            print(f"   ✓ Dashboard contains doctor content")
    elif dashboard.status_code in [301, 302, 303, 307, 308]:
        print(f"   ⚠ Got another redirect to: {dashboard.headers.get('Location')}")
    else:
        print(f"   ✗ Error loading dashboard")
        print(f"   Response: {dashboard.text[:200]}")
else:
    print("   No redirect location in login response!")

print("\n" + "=" * 60)
