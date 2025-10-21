
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)

# ------------------------------
# Test Admin Dashboard
# ------------------------------
@patch('database.supabase')
def test_get_admin_dashboard(mock_supabase):
    # Mock Supabase responses
    mock_supabase.table.return_value.select.return_value.execute.side_effect = [
        MagicMock(count=10),  # students
        MagicMock(count=20),  # faqs
        MagicMock(count=15),  # solved faqs
        MagicMock(count=5),   # unsolved faqs
        MagicMock(count=3),   # unsolved queries
    ]

    response = client.get("/admin/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert data['total_users'] == 10
    assert data['total_faqs'] == 20
    assert data['solved_faqs'] == 15
    assert data['unsolved_faqs'] == 8  # 5 + 3
    assert data['success_rate'] == 65.22 # (15 / (15 + 8)) * 100

# ------------------------------
# Test Admin FAQs
# ------------------------------
@patch('database.supabase')
def test_add_faq(mock_supabase):
    mock_supabase.table.return_value.insert.return_value.execute.return_value.data = [{
        "id": 1,
        "question": "Test Question",
        "answer": "Test Answer",
        "source_type": "manual",
        "created_by": 1,
        "status": "pending"
    }]
    response = client.post("/admin/faqs", data={
        "question": "Test Question",
        "answer": "Test Answer",
        "source_type": "manual",
        "created_by": 1
    })
    assert response.status_code == 200
    assert response.json()['question'] == "Test Question"

@patch('database.supabase')
def test_get_all_faqs(mock_supabase):
    mock_supabase.table.return_value.select.return_value.order.return_value.execute.return_value.data = [
        {"id": 1, "question": "Q1"},
        {"id": 2, "question": "Q2"}
    ]
    response = client.get("/admin/faqs")
    assert response.status_code == 200
    assert len(response.json()) == 2

@patch('database.supabase')
def test_update_faq(mock_supabase):
    mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value.data = [{
        "id": 1, "question": "Updated Question"
    }]
    response = client.put("/admin/faqs/1", json={"question": "Updated Question"})
    assert response.status_code == 200
    assert response.json()['question'] == "Updated Question"

@patch('database.supabase')
def test_delete_faq(mock_supabase):
    mock_supabase.table.return_value.delete.return_value.eq.return_value.execute.return_value.data = [{"id": 1}]
    response = client.delete("/admin/faqs/1")
    assert response.status_code == 200
    assert response.json()['message'] == "FAQ deleted successfully"

# ------------------------------
# Test Admin News
# ------------------------------
@patch('database.supabase')
def test_add_news(mock_supabase):
    mock_supabase.table.return_value.insert.return_value.execute.return_value.data = [{
        "id": 1, "title": "Test News"
    }]
    response = client.post("/admin/news", json={"title": "Test News", "content": "Test Content", "created_by": 1})
    assert response.status_code == 200
    assert response.json()['title'] == "Test News"

@patch('database.supabase')
def test_list_all_news(mock_supabase):
    mock_supabase.table.return_value.select.return_value.order.return_value.execute.return_value.data = [
        {"id": 1, "title": "News 1"},
        {"id": 2, "title": "News 2"}
    ]
    response = client.get("/admin/news")
    assert response.status_code == 200
    assert len(response.json()) == 2

@patch('database.supabase')
def test_update_news(mock_supabase):
    mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value.data = [{
        "id": 1, "title": "Updated News"
    }]
    response = client.put("/admin/news/1", json={"title": "Updated News"})
    assert response.status_code == 200
    assert response.json()['title'] == "Updated News"

@patch('database.supabase')
def test_delete_news(mock_supabase):
    mock_supabase.table.return_value.delete.return_value.eq.return_value.execute.return_value.data = [{"id": 1}]
    response = client.delete("/admin/news/1")
    assert response.status_code == 200
    assert response.json()['message'] == "News deleted successfully"

# ------------------------------
# Test Admin Students
# ------------------------------
@patch('database.supabase')
def test_add_student(mock_supabase):
    mock_supabase.table.return_value.insert.return_value.execute.return_value.data = [{
        "id": 1, "name": "Test Student"
    }]
    response = client.post("/admin/students", json={
        "name": "Test Student",
        "email": "test@example.com",
        "password": "password",
        "department": "CS",
        "enrollment_no": "12345"
    })
    assert response.status_code == 200
    assert response.json()['name'] == "Test Student"

@patch('database.supabase')
def test_list_students(mock_supabase):
    mock_supabase.table.return_value.select.return_value.order.return_value.execute.return_value.data = [
        {"id": 1, "name": "Student 1"},
        {"id": 2, "name": "Student 2"}
    ]
    response = client.get("/admin/students")
    assert response.status_code == 200
    assert len(response.json()) == 2

@patch('database.supabase')
def test_update_student(mock_supabase):
    mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value.data = [{
        "id": 1, "name": "Updated Student"
    }]
    response = client.put("/admin/students/1", json={"name": "Updated Student"})
    assert response.status_code == 200
    assert response.json()['name'] == "Updated Student"

@patch('database.supabase')
def test_delete_student(mock_supabase):
    mock_supabase.table.return_value.delete.return_value.eq.return_value.execute.return_value.data = [{"id": 1}]
    response = client.delete("/admin/students/1")
    assert response.status_code == 200
    assert response.json()['message'] == "Student deleted successfully"

# ------------------------------
# Test Admin Unsolved Queries
# ------------------------------
@patch('database.supabase')
def test_list_unsolved_queries(mock_supabase):
    mock_supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value.data = [
        {"id": 1, "query_text": "Query 1"},
        {"id": 2, "query_text": "Query 2"}
    ]
    response = client.get("/admin/unsolved")
    assert response.status_code == 200
    assert len(response.json()) == 2

@patch('database.supabase')
def test_update_unsolved_query(mock_supabase):
    # Mock the initial select query to find the query to update
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [{
        "id": 1,
        "student_id": 1,
        "query_text": "Test Query"
    }]
    # Mock the update and other calls
    mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value.data = [{"id": 1}]
    mock_supabase.table.return_value.insert.return_value.execute.return_value.data = [{"id": 1}]
    mock_supabase.table.return_value.delete.return_value.eq.return_value.execute.return_value.data = [{"id": 1}]
    
    response = client.put("/admin/unsolved/1", json={"reviewed": True, "solved": True, "answer": "Test Answer"})
    assert response.status_code == 200
    assert response.json()['message'] == "Query solved, added to FAQs, and student chat updated."

