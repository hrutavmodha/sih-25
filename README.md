# FastAPI & Supabase Backend

This project is a high-performance backend service built with Python, FastAPI, and Supabase. It provides a structured, role-based API for a multi-user application, featuring distinct functionalities for Students, Admins, and Super Admins.

## ✨ Features

- **Modular Architecture**: Code is cleanly organized by user role (`admin`, `student`, `superAdmin`) for easy maintenance and scalability.
- **Role-Based Access Control**: Different API endpoints are exposed based on the user's role.
- **Data Validation**: Uses Pydantic for strong, type-hinted data validation for all incoming requests and outgoing responses.
- **Database Integration**: Seamlessly connects to a Supabase project for database operations and more.
- **CORS Enabled**: Pre-configured with Cross-Origin Resource Sharing (CORS) middleware to allow connections from a frontend application.
- **Live Reloading**: The development server is set up with `uvicorn` for automatic reloading on code changes.

## 🛠️ Tech Stack

- **Backend Framework**: FastAPI
- **Database & BaaS**: Supabase
- **Server**: Uvicorn
- **Data Validation**: Pydantic
- **Environment Variables**: python-dotenv
- **Language**: Python 3.10+

## 📂 Project Structure

The project follows a modular structure to keep concerns separated.

```
SIH/
├── .env                # Environment variables (Supabase keys, etc.)
├── database.py         # Supabase client initialization
├── main.py             # Main FastAPI application entrypoint
├── models/             # Pydantic models for data validation
│   └── admin/
│       ├── dashboard.py
│       ├── news.py
│       └── students.py
├── README.md           # This file
├── requirements.txt    # Python dependencies
├── run.sh              # Script to start the development server
└── src/                # Main source code directory
    ├── __init__.py     # Aggregates all routers
    ├── admin/          # Admin-specific module
    │   ├── __init__.py # Admin router definition
    │   ├── dashboard.py
    │   ├── faqs.py
    │   ├── news.py
    │   └── students.py
    ├── student/        # Student-specific module
    │   ├── __init__.py
    │   ├── auth.py
    │   └── ...
    └── superAdmin/     # Super-admin-specific module
        ├── __init__.py
        ├── auth.py
        └── ...
```

## 🚀 Getting Started

Follow these instructions to get the project up and running on your local machine.

### 1. Prerequisites

- Python 3.10 or higher
- A Supabase account and a new project created.

### 2. Clone the Repository

```bash
git clone https://github.com/hrutavmodha/sih-25.git
cd sih-25
```

### 3. Set Up a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

```bash
# For Unix/macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### 4. Install Dependencies

Install the required Python packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the root directory and add your Supabase project credentials. You can find these in your Supabase project dashboard under `Project Settings > API`.

**`.env` file:**
```
SUPABASE_URL="YOUR_SUPABASE_URL"
SUPABASE_KEY="YOUR_SUPABASE_API_KEY"
```

### 6. Set Up Supabase Tables

Ensure your Supabase database has the required tables (`students`, `news`, `faqs`, etc.) with the correct columns that match the Pydantic models and API logic.

### 7. Run the Application

Use the provided shell script to start the development server.

```bash
sh run.sh
```

The API will be running at `http://127.0.0.1:8000`.

## 📚 API Documentation

Once the server is running, FastAPI automatically generates interactive API documentation. You can access it at:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc