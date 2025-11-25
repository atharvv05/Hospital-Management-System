from app import create_app

app = create_app()

TEST_USERNAME = 'admin_john'
TEST_PASSWORD = 'SecurePass123'

with app.test_client() as client:
    # Perform login
    resp = client.post('/auth/login', data={'username': TEST_USERNAME, 'password': TEST_PASSWORD, 'role': 'admin'}, follow_redirects=True)
    print('POST /auth/login -> status:', resp.status_code)
    # Show final request path after redirects
    try:
        print('Final request path:', resp.request.path)
    except Exception:
        print('No request path available')
    body = resp.get_data(as_text=True)
    # Heuristic: check for dashboard markers
    dashboard_markers = ['Admin Dashboard', 'Total Doctors', 'Quick Actions', '/admin/dashboard']
    found = [m for m in dashboard_markers if m in body]
    print('Dashboard markers found in response:', found)
    # Also check if session cookie set in client cookie jar
    cookies = client.cookie_jar
    print('Cookies in test client:')
    for c in cookies:
        print(f' - {c.name}: {c.value}; domain={c.domain}; path={c.path}')
