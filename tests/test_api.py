import os
import json
import pytest

def test_get_config(client):
    response = client.get('/api/config')
    assert response.status_code == 200
    data = response.get_json()
    assert 'DEFAULT_SSH_TARGET' in data

def test_update_config(client):
    new_config = {"DEFAULT_SSH_TARGET": "testuser@testhost"}
    response = client.post('/api/config', json=new_config)
    assert response.status_code == 200
    
    # Verify it saved
    response = client.get('/api/config')
    data = response.get_json()
    assert data['DEFAULT_SSH_TARGET'] == "testuser@testhost"

def test_add_ssh_key_text(client):
    key_data = {
        "name": "test_key",
        "key": "-----BEGIN OPENSSH PRIVATE KEY-----\ntest\n-----END OPENSSH PRIVATE KEY-----\n"
    }
    response = client.post('/api/keys/text', json=key_data)
    assert response.status_code == 200
    
    # Verify file exists
    data_dir = client.application.config['DATA_DIR']
    key_path = os.path.join(data_dir, ".ssh", "test_key")
    assert os.path.exists(key_path)
    with open(key_path, 'r') as f:
        content = f.read()
        assert "BEGIN OPENSSH PRIVATE KEY" in content

def test_list_ssh_keys(client):
    # Add a key first
    key_data = {"name": "list_test_key", "key": "test_content"}
    client.post('/api/keys/text', json=key_data)
    
    response = client.get('/api/keys')
    assert response.status_code == 200
    keys = response.get_json()
    assert "list_test_key" in keys

def test_remove_ssh_key(client):
    # Add a key first
    key_data = {"name": "remove_test_key", "key": "test_content"}
    client.post('/api/keys/text', json=key_data)
    
    # Remove it
    response = client.delete('/api/keys/remove_test_key')
    assert response.status_code == 200
    
    # Verify it's gone
    response = client.get('/api/keys')
    keys = response.get_json()
    assert "remove_test_key" not in keys
    
    data_dir = client.application.config['DATA_DIR']
    key_path = os.path.join(data_dir, ".ssh", "remove_test_key")
    assert not os.path.exists(key_path)

def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'ok'
