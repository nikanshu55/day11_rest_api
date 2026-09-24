Day 11 – FastAPI Employee REST API

A simple Employee Management REST API built using FastAPI and PostgreSQL.

This project demonstrates how a backend API communicates with PostgreSQL database and performs CRUD operations on employee data.

Technologies Used
Python
FastAPI
Uvicorn
PostgreSQL
Psycopg2
Pydantic
python-dotenv
Features
Create employee
Get all employees
Get employee by ID
Update employee
Delete employee
Request validation
Email validation
Duplicate email checking
Department and manager validation
Error handling
PostgreSQL database integration
Swagger API documentation
API Endpoints
Method	Endpoint	Description
GET	/employees	Get all employees
GET	/employees/{id}	Get employee by ID
POST	/employees	Create a new employee
PUT	/employees/{id}	Update an employee
DELETE	/employees/{id}	Delete an employee
Project Structure
day11_rest_api/
│
├── app.py
├── requirements.txt
├── day10.1.sql
├── day10.2.sql
├── .env
├── .gitignore
└── README.md
Files

app.py
Main FastAPI application containing API routes, validation, database connection, and error handling.

requirements.txt
Contains the Python packages required for the project.

day10.1.sql
Contains the PostgreSQL database schema and table definitions.

day10.2.sql
Contains sample data for the database.

.env
Contains local database configuration.

.gitignore
Contains files that should not be committed to Git.

Database Setup

Create a PostgreSQL database:

CREATE DATABASE employee_management;

Create a .env file:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=employee_management
DB_USER=postgres
DB_PASSWORD=your_password

Run the database schema:

psql -U postgres -h localhost -d employee_management -f day10.1.sql

Insert sample data:

psql -U postgres -h localhost -d employee_management -f day10.2.sql
Installation

Clone the repository:

git clone https://github.com/nikanshu55/day11_rest_api.git

Go to the project directory:

cd day11_rest_api

Create a virtual environment:

python3 -m venv venv

Activate the virtual environment:

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt
Run the Application

Start the FastAPI server:

uvicorn app:app --reload

The API will be available at:

http://127.0.0.1:8000
API Documentation

FastAPI provides interactive Swagger documentation automatically.

Open:

http://127.0.0.1:8000/docs

From Swagger UI, you can view and test all available API endpoints.

CRUD Operations
POST    → Create employee
GET     → Read employee data
PUT     → Update employee
DELETE  → Delete employee
Project purpose 

The purpose of this project is to understand and implement:

REST API development
FastAPI application structure
HTTP methods
Request and response handling
JSON data
Request validation
HTTP status codes
PostgreSQL integration
CRUD operations
Swagger API testing
Environment variable management