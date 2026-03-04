import pytest
import re
from src.app import app

def test_csrf_protection_missing_token(client):
    # Enable CSRF for this test
    app.config['WTF_CSRF_ENABLED'] = True
    
    # Try a state-changing operation without a CSRF token
    response = client.post('/api/hosts', json={
        "label": "test_host",
        "target": "user@test"
    })
    
    # Should fail with 400 Bad Request due to missing CSRF token
    assert response.status_code == 400
    assert b"The CSRF token is missing." in response.data or b"The CSRF session token is missing." in response.data

    # Restore
    app.config['WTF_CSRF_ENABLED'] = False


def test_csrf_protection_with_token(client):
    app.config['WTF_CSRF_ENABLED'] = True
    
    # First, get the main page to extract the CSRF token from the meta tag
    response = client.get('/')
    assert response.status_code == 200
    
    # Extract the token using regex
    match = re.search(r'<meta name="csrf-token" content="([^"]+)">', response.data.decode('utf-8'))
    assert match is not None, "CSRF token meta tag not found"
    csrf_token = match.group(1)
    
    # Now try the state-changing operation with the token
    response = client.post('/api/hosts', json={
        "label": "test_host",
        "target": "user@test"
    }, headers={'X-CSRFToken': csrf_token})
    
    # Should pass CSRF and be processed
    assert response.status_code in [200, 201]

    # Clean up
    client.delete('/api/hosts/test_host', headers={'X-CSRFToken': csrf_token})

    app.config['WTF_CSRF_ENABLED'] = False
