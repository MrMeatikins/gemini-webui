import pytest
import os
import io
import json
from src.app import app, init_app

@pytest.fixture
def client(test_data_dir, monkeypatch):
    monkeypatch.setenv("DATA_DIR", str(test_data_dir))
    app.config['TESTING'] = True
    app.config['DATA_DIR'] = str(test_data_dir)
    app.config['BYPASS_AUTH_FOR_TESTING'] = 'true'
    app.config['SECRET_KEY'] = 'test-secret-key'
    with app.app_context():
        init_app()
    with app.test_client() as client:
        yield client

def test_upload_file_success(client, test_data_dir):
    data = {
        'file': (io.BytesIO(b"test content"), 'testfile.txt')
    }
    response = client.post('/api/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    resp_data = json.loads(response.data)
    assert resp_data['status'] == 'success'
    assert resp_data['filename'] == 'testfile.txt'

    # Verify file is saved in DATA_DIR/workspace
    save_path = os.path.join(test_data_dir, 'workspace', 'testfile.txt')
    assert os.path.exists(save_path)
    with open(save_path, 'rb') as f:
        assert f.read() == b"test content"

def test_upload_file_no_file(client):
    response = client.post('/api/upload', data={}, content_type='multipart/form-data')
    assert response.status_code == 400
    resp_data = json.loads(response.data)
    assert resp_data['message'] == 'No file part'

def test_download_file_success(client, test_data_dir):
    # Setup file in workspace
    workspace_dir = os.path.join(test_data_dir, 'workspace')
    os.makedirs(workspace_dir, exist_ok=True)
    save_path = os.path.join(workspace_dir, 'download_test.txt')
    with open(save_path, 'wb') as f:
        f.write(b"download content")

    response = client.get('/api/download/download_test.txt')
    assert response.status_code == 200
    assert response.data == b"download content"
    assert response.headers['Content-Disposition'].startswith('attachment;')
