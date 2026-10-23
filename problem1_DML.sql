USE company;

-- Insert Employees
INSERT INTO EMPLOYEE (ssn, fname, lname, bdate, address, gender, salary, Dno) VALUES
(1, 'Ahmed', 'Ali', '1990-01-01', 'Alexandria', 'M', 5000.00, NULL),
(2, 'Sara', 'Kamal', '1992-05-15', 'Cairo', 'F', 6000.00, NULL),
(3, 'Omar', 'Hassan', '1988-11-20', 'Giza', 'M', 5500.00, NULL);

-- Insert Departments
INSERT INTO DEPARTMENT (Dnumber, Dname, mgr_ssn, mgr_start_date) VALUES
(10, 'IT', 1, '2020-01-01'),
(20, 'HR', 2, '2021-03-15'),
(30, 'Sales', 3, '2019-07-20');

-- Update Employees to assign Departments
UPDATE EMPLOYEE SET Dno = 10 WHERE ssn = 1;
UPDATE EMPLOYEE SET Dno = 20 WHERE ssn = 2;
UPDATE EMPLOYEE SET Dno = 30 WHERE ssn = 3;

-- Insert Projects 
INSERT INTO PROJECT (Pnumber, Pname, Plocation, Dno) VALUES
(100, 'Web App', 'Alexandria', 10),
(200, 'Recruitment', 'Cairo', 20),
(300, 'Marketing', 'Giza', 30);