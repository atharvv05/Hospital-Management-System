from app import create_app
import json

app = create_app()

with app.test_client() as client:
    # Login as admin
    login_resp = client.post(
        '/auth/login',
        data={'username': 'admin_john', 'password': 'SecurePass123', 'role': 'admin'},
        follow_redirects=False
    )
    print(f"1. Login POST /auth/login -> {login_resp.status_code}")
    print(f"   Location header (redirect to): {login_resp.headers.get('Location', 'N/A')}")
    
    # Now check session via debug endpoint
    debug_resp = client.get('/debug/current_user')
    print(f"\n2. Debug GET /debug/current_user -> {debug_resp.status_code}")
    debug_data = debug_resp.get_json()
    print(f"   Current user data: {json.dumps(debug_data, indent=2)}")
    
    # Try to access dashboard
    dash_resp = client.get('/admin/dashboard', follow_redirects=False)
    print(f"\n3. Dashboard GET /admin/dashboard -> {dash_resp.status_code}")
    if dash_resp.status_code == 302:
        print(f"   Redirected to: {dash_resp.headers.get('Location', 'N/A')}")
    else:
        print(f"   ✅ Dashboard accessible (not redirected)")
