
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)

# Note: There are duplicate routes in src/student/main.py and the specific
# route files (auth.py, chat.py, news.py). These tests assume the routes
# from the specific files are the correct ones.

# ------------------------------
# Test Student Auth
# ------------------------------
@patch('database.supabase')
@patch('src.student.auth.create_jwt_token')
def test_student_login(mock_create_jwt_token, mock_supabase):
    # Mock Supabase response
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [{
        "id": 1,
        "email": "test@example.com",
        "password": "a_hashed_password",
        "status": "active"
    }]
    # Mock JWT token creation
    mock_create_jwt_token.return_value = "a_mock_token"

    with patch('hashlib.sha256') as mock_sha256:
        mock_sha256.return_value.hexdigest.return_value = "a_hashed_password"
        response = client.post("/student/login", json={
            "email": "test@example.com",
            "password": "password"
        })
    
    assert response.status_code == 200
    assert response.json() == {"access_token": "a_mock_token", "token_type": "bearer"}

# ------------------------------
# Test Student Chat
# ------------------------------
@patch('database.supabase')
def test_send_chat_query_solved(mock_supabase):
    # Mock FAQ match
    mock_supabase.table.return_value.select.return_value.execute.return_value.data = [
        {"id": 1, "question": "What is FastAPI?", "answer": "A web framework."}
    ]
    # Mock insert to chat_logs
    mock_supabase.table.return_value.insert.return_value.execute.return_value.data = [{"id": 1}]

    response = client.post("/student/chat", json={
        "student_id": 1,
        "query_text": "fastapi",
        "detected_language": "en"
    })
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == "solved"
    assert data['bot_response'] == "A web framework."

@patch('database.supabase')
def test_send_chat_query_unsolved(mock_supabase):
    # Mock no FAQ match
    mock_supabase.table.return_value.select.return_value.execute.return_value.data = []
    # Mock insert to unsolved_queries and chat_logs
    mock_supabase.table.return_value.insert.return_value.execute.return_value.data = [{"id": 1}]

    response = client.post("/student/chat", json={
        "student_id": 1,
        "query_text": "A new question",
        "detected_language": "en"
    })
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == "unsolved"
    assert "admin will review" in data['bot_response']

@patch('database.supabase')
def test_get_chat_history(mock_supabase):
    mock_supabase.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value.data = [
        {"query_text": "Q1", "bot_response": "A1"},
        {"query_text": "Q2", "bot_response": "A2"}
    ]
    response = client.get("/student/chat/1")
    assert response.status_code == 200
    assert len(response.json()) == 2

# ------------------------------
# Test Student Main
# ------------------------------
@patch('database.supabase')
def test_get_student_home(mock_supabase):
    # Mock student details
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [{
        "name": "Test Student",
        "department": "CS",
        "enrollment_no": "12345"
    }]
    # Mock latest news
    mock_supabase.table.return_value.select.return_value.order.return_value.limit.return_value.execute.return_value.data = [
        {"id": 1, "title": "News 1"}
    ]

    response = client.get("/student/home/1")
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == "Test Student"
    assert len(data['latest_news']) == 1
    assert "Mahatma Gandhi" in data['motivational_quote']

# ------------------------------
# Test Student News
# ------------------------------
@patch('database.supabase')
def test_get_student_news(mock_supabase):
    mock_supabase.table.return_value.select.return_value.order.return_value.execute.return_value.data = [
        {"id": 1, "title": "News 1"},
        {"id": 2, "title": "News 2"}
    ]
    response = client.get("/student/news")
    assert response.status_code == 200
    assert len(response.json()) == 2
