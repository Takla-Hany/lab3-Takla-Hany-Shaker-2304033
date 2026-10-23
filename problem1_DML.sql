USE company;

-- Insert Employees
INSERT INTO EMPLOYEE (ssn, fname, lname, bdate, address, gender, salary, Dno) VALUES
(1, 'fname 1', 'lname 1', '1999-09-09', 'address 1', 'M', 5000.00, NULL),
(2, 'fname 2', 'lname 2', '1999-09-09', 'address 2', 'F', 6000.00, NULL),
(3, 'fname 3', 'lname 3', '1999-09-09', 'address 3', 'M', 5500.00, NULL);

-- Insert Departments
INSERT INTO DEPARTMENT (Dnumber, Dname, mgr_ssn, mgr_start_date) VALUES
(10, 'Dname 1', 1, '1999-09-09'),
(20, 'Dname 2', 2, '1999-09-09'),
(30, 'Dname 3', 3, '1999-09-09');

-- Update Employees to assign Departments
UPDATE EMPLOYEE SET Dno = 10 WHERE ssn = 1;
UPDATE EMPLOYEE SET Dno = 20 WHERE ssn = 2;
UPDATE EMPLOYEE SET Dno = 30 WHERE ssn = 3;

-- Insert Projects 
INSERT INTO PROJECT (Pnumber, Pname, Plocation, Dno) VALUES
(100, 'Pname 1', 'Plocation 1', 10),
(200, 'Pname 2', 'Plocation 2', 20),
(300, 'Pname 3', 'Plocation 3', 30);