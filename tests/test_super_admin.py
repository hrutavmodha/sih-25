
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)

# ------------------------------
# Test Super Admin Auth
# ------------------------------
@patch('database.supabase')
@patch('src.superAdmin.auth.create_jwt_token')
def test_admin_login(mock_create_jwt_token, mock_supabase):
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [{
        "id": 1,
        "email": "super@admin.com",
        "password": "a_hashed_password",
        "status": "active",
        "role": "super_admin"
    }]
    mock_create_jwt_token.return_value = "a_mock_token"

    with patch('hashlib.sha256') as mock_sha256:
        mock_sha256.return_value.hexdigest.return_value = "a_hashed_password"
        response = client.post("/super-admin/login", json={
            "email": "super@admin.com",
            "password": "password"
        })

    assert response.status_code == 200
    assert response.json() == {"access_token": "a_mock_token", "token_type": "bearer"}

# ------------------------------
# Test Super Admin Admins
# ------------------------------
@patch('src.superAdmin.admins.verify_super_admin')
@patch('database.supabase')
def test_add_admin(mock_supabase, mock_verify_super_admin):
    mock_verify_super_admin.return_value = {"role": "super_admin"}
    mock_supabase.table.return_value.insert.return_value.execute.return_value.data = [{
        "id": 2, "name": "New Admin"
    }]
    response = client.post("/super-admin/admins", json={
        "name": "New Admin",
        "email": "new@admin.com",
        "password": "password",
        "role": "admin",
        "status": "active"
    }, headers={"Authorization": "Bearer a_mock_token"})
    assert response.status_code == 200
    assert response.json()['name'] == "New Admin"

@patch('src.superAdmin.admins.verify_admin_or_super')
@patch('database.supabase')
def test_list_admins(mock_supabase, mock_verify_admin_or_super):
    mock_verify_admin_or_super.return_value = {"role": "super_admin"}
    mock_supabase.table.return_value.select.return_value.order.return_value.execute.return_value.data = [
        {"id": 1, "name": "Admin 1"},
        {"id": 2, "name": "Admin 2"}
    ]
    response = client.get("/super-admin/admins", headers={"Authorization": "Bearer a_mock_token"})
    assert response.status_code == 200
    assert len(response.json()) == 2

@patch('src.superAdmin.admins.verify_admin_or_super')
@patch('database.supabase')
def test_update_admin(mock_supabase, mock_verify_admin_or_super):
    mock_verify_admin_or_super.return_value = {"role": "super_admin"}
    mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value.data = [{
        "id": 1, "name": "Updated Admin"
    }]
    response = client.put("/super-admin/admins/1", json={"name": "Updated Admin"}, headers={"Authorization": "Bearer a_mock_token"})
    assert response.status_code == 200
    assert response.json()['name'] == "Updated Admin"

@patch('src.superAdmin.admins.verify_super_admin')
@patch('database.supabase')
def test_delete_admin(mock_supabase, mock_verify_super_admin):
    mock_verify_super_admin.return_value = {"role": "super_admin"}
    mock_supabase.table.return_value.delete.return_value.eq.return_value.execute.return_value.data = [{"id": 1}]
    response = client.delete("/super-admin/admins/1", headers={"Authorization": "Bearer a_mock_token"})
    assert response.status_code == 200
    assert response.json()['message'] == "Admin deleted successfully"

# ------------------------------
# Test Super Admin Profile
# ------------------------------
@patch('src.superAdmin.profile.verify_super_admin')
@patch('database.supabase')
def test_get_super_admin_profile(mock_supabase, mock_verify_super_admin):
    mock_verify_super_admin.return_value = {"role": "super_admin"}
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [{
        "id": 1, "name": "Super Admin"
    }]
    response = client.get("/super-admin/profile", headers={"Authorization": "Bearer a_mock_token"})
    assert response.status_code == 200
    assert response.json()['name'] == "Super Admin"

@patch('src.superAdmin.profile.verify_super_admin')
@patch('database.supabase')
def test_update_super_admin_profile(mock_supabase, mock_verify_super_admin):
    mock_verify_super_admin.return_value = {"role": "super_admin"}
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [{"id": 1}]
    mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value.data = [{
        "id": 1, "name": "Updated Super Admin"
    }]
    response = client.put("/super-admin/profile", json={"name": "Updated Super Admin"}, headers={"Authorization": "Bearer a_mock_token"})
    assert response.status_code == 200
    assert response.json()['name'] == "Updated Super Admin"
