from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Employee Management REST API",
    description="Day 11 REST API Practical",
    version="1.0.0"
)


# -----------------------------
# Database Connection
# -----------------------------
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


# -----------------------------
# Request JSON Model
# -----------------------------
class EmployeeCreate(BaseModel):
    employee_name: str
    email: EmailStr
    phone: Optional[str] = None
    joining_date: date
    department_id: int
    manager_id: Optional[int] = None


# -----------------------------
# GET /employees
# -----------------------------
@app.get("/employees")
def get_employees():

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT
                e.employee_id,
                e.employee_name,
                e.email,
                e.phone,
                e.joining_date,
                e.department_id,
                e.manager_id,
                d.department_name
            FROM employee e
            JOIN department d
                ON e.department_id = d.department_id
            ORDER BY e.employee_id;
        """)

        rows = cursor.fetchall()

        employees = []

        for row in rows:
            employees.append({
                "employee_id": row[0],
                "employee_name": row[1],
                "email": row[2],
                "phone": row[3],
                "joining_date": row[4],
                "department_id": row[5],
                "manager_id": row[6],
                "department_name": row[7]
            })

        return {
            "success": True,
            "count": len(employees),
            "data": employees
        }

    finally:
        cursor.close()
        conn.close()


# -----------------------------
# GET /employees/{id}
# -----------------------------
@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT
                e.employee_id,
                e.employee_name,
                e.email,
                e.phone,
                e.joining_date,
                e.department_id,
                e.manager_id,
                d.department_name
            FROM employee e
            JOIN department d
                ON e.department_id = d.department_id
            WHERE e.employee_id = %s;
        """, (employee_id,))

        row = cursor.fetchone()

        if not row:
            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        return {
            "success": True,
            "data": {
                "employee_id": row[0],
                "employee_name": row[1],
                "email": row[2],
                "phone": row[3],
                "joining_date": row[4],
                "department_id": row[5],
                "manager_id": row[6],
                "department_name": row[7]
            }
        }

    finally:
        cursor.close()
        conn.close()


# -----------------------------
# POST /employees
# -----------------------------
@app.post("/employees", status_code=201)
def create_employee(employee: EmployeeCreate):

    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        # Check department
        cursor.execute(
            "SELECT department_id FROM department WHERE department_id = %s",
            (employee.department_id,)
        )

        if not cursor.fetchone():
            raise HTTPException(
                status_code=400,
                detail="Department does not exist"
            )

        # Check manager
        if employee.manager_id is not None:

            cursor.execute(
                "SELECT employee_id FROM employee WHERE employee_id = %s",
                (employee.manager_id,)
            )

            if not cursor.fetchone():
                raise HTTPException(
                    status_code=400,
                    detail="Manager does not exist"
                )

        # Check duplicate email
        cursor.execute(
            "SELECT employee_id FROM employee WHERE email = %s",
            (employee.email,)
        )

        if cursor.fetchone():
            raise HTTPException(
                status_code=409,
                detail="Email already exists"
            )

        # Insert employee
        cursor.execute("""
            INSERT INTO employee
            (
                employee_name,
                email,
                phone,
                joining_date,
                department_id,
                manager_id
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING employee_id;
        """, (
            employee.employee_name,
            employee.email,
            employee.phone,
            employee.joining_date,
            employee.department_id,
            employee.manager_id
        ))

        employee_id = cursor.fetchone()[0]

        conn.commit()

        return {
            "success": True,
            "message": "Employee created successfully",
            "employee_id": employee_id
        }

    except HTTPException:
        conn.rollback()
        raise

    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

    finally:
        cursor.close()
        conn.close()


# -----------------------------
# PUT /employees/{id}
# -----------------------------
@app.put("/employees/{employee_id}")
def update_employee(
    employee_id: int,
    employee: EmployeeCreate
):

    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        # Check employee
        cursor.execute(
            "SELECT employee_id FROM employee WHERE employee_id = %s",
            (employee_id,)
        )

        if not cursor.fetchone():
            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        # Prevent employee from becoming their own manager
        if employee.manager_id == employee_id:
            raise HTTPException(
                status_code=400,
                detail="Employee cannot be their own manager"
            )

        # Check department
        cursor.execute(
            "SELECT department_id FROM department WHERE department_id = %s",
            (employee.department_id,)
        )

        if not cursor.fetchone():
            raise HTTPException(
                status_code=400,
                detail="Department does not exist"
            )

        # Check manager
        if employee.manager_id is not None:

            cursor.execute(
                "SELECT employee_id FROM employee WHERE employee_id = %s",
                (employee.manager_id,)
            )

            if not cursor.fetchone():
                raise HTTPException(
                    status_code=400,
                    detail="Manager does not exist"
                )

        # Check duplicate email
        cursor.execute("""
            SELECT employee_id
            FROM employee
            WHERE email = %s
            AND employee_id != %s;
        """, (employee.email, employee_id))

        if cursor.fetchone():
            raise HTTPException(
                status_code=409,
                detail="Email already exists"
            )

        # Update employee
        cursor.execute("""
            UPDATE employee
            SET
                employee_name = %s,
                email = %s,
                phone = %s,
                joining_date = %s,
                department_id = %s,
                manager_id = %s
            WHERE employee_id = %s;
        """, (
            employee.employee_name,
            employee.email,
            employee.phone,
            employee.joining_date,
            employee.department_id,
            employee.manager_id,
            employee_id
        ))

        conn.commit()

        return {
            "success": True,
            "message": "Employee updated successfully",
            "employee_id": employee_id
        }

    except HTTPException:
        conn.rollback()
        raise

    except Exception:
        conn.rollback()
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

    finally:
        cursor.close()
        conn.close()


# -----------------------------
# DELETE /employees/{id}
# -----------------------------
@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):

    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        # Check employee
        cursor.execute(
            "SELECT employee_id FROM employee WHERE employee_id = %s",
            (employee_id,)
        )

        if not cursor.fetchone():
            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        try:
            cursor.execute(
                "DELETE FROM employee WHERE employee_id = %s",
                (employee_id,)
            )

            conn.commit()

        except psycopg2.IntegrityError:
            conn.rollback()

            raise HTTPException(
                status_code=409,
                detail="Employee cannot be deleted because related records exist"
            )

        return {
            "success": True,
            "message": "Employee deleted successfully"
        }

    finally:
        cursor.close()
        conn.close()