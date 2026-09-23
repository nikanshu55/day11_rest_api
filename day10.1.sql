
-- 1. Department
CREATE TABLE department (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE
);


-- 2. Employee
CREATE TABLE employee (
    employee_id SERIAL PRIMARY KEY,
    employee_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    phone VARCHAR(15),
    joining_date DATE NOT NULL,
    department_id INT NOT NULL,
    manager_id INT,

    CONSTRAINT fk_employee_department
        FOREIGN KEY (department_id)
        REFERENCES department(department_id),

    CONSTRAINT fk_employee_manager
        FOREIGN KEY (manager_id)
        REFERENCES employee(employee_id)
);


-- 3. Leave Type
CREATE TABLE leave_type (
    leave_type_id SERIAL PRIMARY KEY,
    leave_type_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);


-- 4. Leave Balance
CREATE TABLE leave_balance (
    balance_id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL,
    leave_type_id INT NOT NULL,
    total_days INT NOT NULL CHECK (total_days >= 0),
    used_days INT NOT NULL DEFAULT 0 CHECK (used_days >= 0),
    remaining_days INT NOT NULL CHECK (remaining_days >= 0),

    CONSTRAINT fk_balance_employee
        FOREIGN KEY (employee_id)
        REFERENCES employee(employee_id),

    CONSTRAINT fk_balance_leave_type
        FOREIGN KEY (leave_type_id)
        REFERENCES leave_type(leave_type_id),

    CONSTRAINT unique_employee_leave_type
        UNIQUE (employee_id, leave_type_id),

    CONSTRAINT valid_balance
        CHECK (used_days <= total_days),

    CONSTRAINT valid_remaining_balance
        CHECK (remaining_days = total_days - used_days)
);


-- 5. Leave Request
CREATE TABLE leave_request (
    leave_request_id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL,
    leave_type_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    reason TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_request_employee
        FOREIGN KEY (employee_id)
        REFERENCES employee(employee_id),

    CONSTRAINT fk_request_leave_type
        FOREIGN KEY (leave_type_id)
        REFERENCES leave_type(leave_type_id),

    CONSTRAINT valid_leave_dates
        CHECK (end_date >= start_date),

    CONSTRAINT valid_leave_status
        CHECK (status IN ('Pending', 'Approved', 'Rejected', 'Cancelled'))
);


-- 6. Approval History
CREATE TABLE approval_history (
    approval_history_id SERIAL PRIMARY KEY,
    leave_request_id INT NOT NULL,
    approver_id INT NOT NULL,
    action VARCHAR(20) NOT NULL,
    comments TEXT,
    action_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_history_request
        FOREIGN KEY (leave_request_id)
        REFERENCES leave_request(leave_request_id),

    CONSTRAINT fk_history_approver
        FOREIGN KEY (approver_id)
        REFERENCES employee(employee_id),

    CONSTRAINT valid_approval_action
        CHECK (action IN ('Approved', 'Rejected', 'Cancelled'))
);