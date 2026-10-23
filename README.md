# Database Lab 3

## Team Members
* Takla Hany Shaker Said - ID: 2304033

## Technology Stack
* **Back End:** Python (Flask)
* **Front End:** HTML, CSS, JavaScript
* **Database:** MySQL (PyMySQL)

## Deliverables Structure
* `problem1_DDL.sql` & `problem1_DML.sql`: COMPANY database schema and seed data.
* `problem1_Answers.txt`: SQL queries and error explanations for Q1.1 - Q1.3.
* `problem2_DDL.sql` & `problem2_DML.sql`: Library database schema (with ON DELETE CASCADE) and seed data.
* `website/`: Flask application containing the combined Lab 2 (To-Do) and Lab 3 (Library) features.

## How to Run the Website
1. Navigate to the project root folder.
2. Create and activate the Conda environment: `conda create -n lab3-flask python=3.11 -y` and `conda activate lab3-flask`.
3. Install dependencies: `pip install -r requirements.txt`.
4. Run the Lab 2 database script `database/registration.sql` from the previous lab to build the `registration` database.
5. Run the Lab 3 database script `database/library.sql` to build the `library` database.
6. Navigate into the `website/` folder.
7. Copy `.env.example` to `.env` and configure your MySQL credentials.
8. Start the server: `flask run`.
9. Open `http://127.0.0.1:5000` in your web browser.

## Features Built
* **Problem 1:** Implemented the COMPANY schema with circular foreign key dependencies using `ALTER TABLE`.
* **Problem 2 (F2.1 - F2.5):** Implemented the Library relational schema. and edited the web application to view, add, edit, and delete Authors and Books using SQL `SELECT`, `INSERT`, `UPDATE`, and `DELETE` statements.
* **Problem 2 (Bonus):** Implemented Image Upload Feature.