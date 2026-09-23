-- ============================================
-- DAY 10 - SAMPLE DATA
-- Employee Leave Management
-- ============================================


-- 1. DEPARTMENT DATA
INSERT INTO department (department_name)
VALUES
('IT'),
('HR'),
('Finance'),
('Sales');


-- 2. LEAVE TYPE DATA
INSERT INTO leave_type (leave_type_name, description)
VALUES
('Casual Leave', 'Leave for personal work'),
('Sick Leave', 'Leave due to illness'),
('Earned Leave', 'Planned annual leave');


-- 3. EMPLOYEE DATA
-- First insert managers
INSERT INTO employee
(employee_name, email, phone, joining_date, department_id, manager_id)
VALUES
('Rahul Sharma', 'rahul@company.com', '9876543210', '2022-01-10', 1, NULL),
('Priya Singh', 'priya@company.com', '9876543211', '2022-03-15', 2, NULL);


-- Insert employees working under managers
INSERT INTO employee
(employee_name, email, phone, joining_date, department_id, manager_id)
VALUES
('Amit Kumar', 'amit@company.com', '9876543212', '2024-06-01', 1, 1),
('Neha Gupta', 'neha@company.com', '9876543213', '2024-07-10', 1, 1),
('Rohit Verma', 'rohit@company.com', '9876543214', '2024-08-20', 2, 2);


-- 4. LEAVE BALANCE DATA
INSERT INTO leave_balance
(employee_id, leave_type_id, total_days, used_days, remaining_days)
VALUES
(3, 1, 12, 2, 10),
(3, 2, 10, 1, 9),
(3, 3, 15, 5, 10),
(4, 1, 12, 0, 12),
(4, 2, 10, 2, 8),
(5, 1, 12, 1, 11),
(5, 2, 10, 0, 10);


-- 5. LEAVE REQUEST DATA
INSERT INTO leave_request
(employee_id, leave_type_id, start_date, end_date, reason, status)
VALUES
(3, 1, '2026-09-20', '2026-09-22', 'Family function', 'Pending'),
(4, 2, '2026-09-25', '2026-09-26', 'Medical reason', 'Approved'),
(5, 1, '2026-10-05', '2026-10-06', 'Personal work', 'Rejected');


-- 6. APPROVAL HISTORY DATA
INSERT INTO approval_history
(leave_request_id, approver_id, action, comments)
VALUES
(2, 1, 'Approved', 'Leave approved by manager'),
(3, 2, 'Rejected', 'Leave cannot be approved at this time');


-- ============================================
-- CHECK ALL TABLES
-- ============================================

SELECT * FROM department;

SELECT * FROM employee;

SELECT * FROM leave_type;

SELECT * FROM leave_balance;

SELECT * FROM leave_request;

SELECT * FROM approval_history;


-- ============================================
-- JOIN TEST
-- ============================================

SELECT
    e.employee_name,
    d.department_name,
    lt.leave_type_name,
    lr.start_date,
    lr.end_date,
    lr.status
FROM leave_request lr
JOIN employee e
    ON lr.employee_id = e.employee_id
JOIN department d
    ON e.department_id = d.department_id
JOIN leave_type lt
    ON lr.leave_type_id = lt.leave_type_id;