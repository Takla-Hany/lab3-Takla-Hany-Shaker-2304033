import os
from flask import Flask, render_template, request, redirect, url_for, session
import bcrypt
import pymysql
from db import get_db_connection, get_library_connection

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "fallback_dev_key")

@app.route('/register', methods=['GET', 'POST'])
def register():
    # recive the register form information
    if request.method == 'POST':
        name = request.form.get('name').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validation
        if not name:
            return render_template('register.html', error="Name is required")
        if not email:
            return render_template('register.html', error="Email is required")
        if not password:
            return render_template('register.html', error="Password is required")
        if not confirm_password:
            return render_template('register.html', error="Confirm password is required")
        if password != confirm_password:
            return render_template('register.html', error="Passwords do not match")

        # password Hashing
        hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        connection = get_db_connection()
        try:
            # add register info to database
            with connection.cursor() as cursor:
                sql = "INSERT INTO users (email, name, password_hash) VALUES (%s, %s, %s)"
                cursor.execute(sql, (email, name, hash.decode('utf-8')))
            connection.commit()

            # let user log-in
            with connection.cursor() as cursor:
                cursor.execute("SELECT user_id FROM users WHERE email = %s", (email))
                user = cursor.fetchone()
                session['user_id'] = user['user_id']
                session['user_name'] = name
            
            return redirect(url_for('index'))

        except:
            return render_template('register.html', error="Email Already Exists")
        finally:
            connection.close()

    # Render register Page
    return render_template('register.html')

@app.route('/')
def index():
    # check the session
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    connection = get_db_connection()
    todos = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT todo_id, title, is_done, created_at FROM todos WHERE user_id = %s ORDER BY todo_id DESC", (session['user_id']))
            todos = cursor.fetchall()
    finally:
        connection.close()
        
    # BONUS
    open_count = sum(1 for todo in todos if todo['is_done'] == 0)
        
    return render_template('index.html', todos=todos, user_name=session.get('user_name', 'User'), open_count=open_count)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # recive log-in data
    if request.method == 'POST':
        email = request.form.get('email').strip()
        password = request.form.get('password')

        # Validation
        if not email:
            return render_template('login.html', error="Email is required")
        if not password:
            return render_template('login.html', error="Password is required")

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # check for user data
                cursor.execute("SELECT user_id, name, password_hash FROM users WHERE email = %s", (email))
                user = cursor.fetchone()

                # if the user exists and the password matches:
                if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                    session['user_id'] = user['user_id']
                    session['user_name'] = user['name']
                    return redirect(url_for('index'))
                else:
                    # wrong e-mail or wrong password
                    return render_template('login.html', error="Invalid email or password")
        finally:
            connection.close()

    # render login page
    return render_template('login.html')

@app.route('/logout')
def logout():
    # clear the session
    session.clear()
    return redirect(url_for('login'))


@app.route('/add', methods=['POST'])
def add_todo():
    # chech the session
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    title = request.form.get('title').strip()
    
    # Validation
    if not title or len(title) > 200:
        error = "Title is required" if not title else "Title is too long (200 characters at most)"
        connection = get_db_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT todo_id, title, is_done, created_at FROM todos WHERE user_id = %s ORDER BY todo_id DESC", (session['user_id']))
                todos = cursor.fetchall()
            return render_template('index.html', todos=todos, user_name=session.get('user_name'), error=error)
        finally:
            connection.close()

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # add to-do
            cursor.execute("INSERT INTO todos (user_id, title) VALUES (%s, %s)", (session['user_id'], title))
        connection.commit()
    finally:
        connection.close()

    return redirect(url_for('index'))

@app.route('/edit/<int:todo_id>', methods=['POST'])
def edit_todo(todo_id):
    # chech the session
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    new_title = request.form.get('title').strip()
    
    if not new_title or len(new_title) > 200:
        error = "Title is required" if not new_title else "Title is too long (200 characters at most)"
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT todo_id, title, is_done, created_at FROM todos WHERE user_id = %s ORDER BY todo_id DESC", (session['user_id']))
                todos = cursor.fetchall()
            return render_template('index.html', todos=todos, user_name=session.get('user_name', 'User'), error=error)
        finally:
            connection.close()

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # update to-do
            cursor.execute("UPDATE todos SET title = %s WHERE todo_id = %s AND user_id = %s", (new_title, todo_id, session['user_id']))
        connection.commit()

    finally:
        connection.close()

    return redirect(url_for('index'))

@app.route('/toggle/<int:todo_id>', methods=['POST'])
def toggle_todo(todo_id):
    # chech the session
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    is_done = request.form.get('is_done')
    new_status = 1 if is_done == '1' else 0
    
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # update to-do
            cursor.execute("UPDATE todos SET is_done = %s WHERE todo_id = %s AND user_id = %s", (new_status, todo_id, session['user_id']))
        connection.commit()

    finally:
        connection.close()

    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    # chech the session
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # update to-do
            cursor.execute("DELETE FROM todos WHERE todo_id = %s AND user_id = %s", (todo_id, session['user_id']))
        connection.commit()
    finally:
        connection.close()

    return redirect(url_for('index'))




# LAB 3

# F2.1 Show a table of the books (with the author_id of each book) and a table of the authors.
@app.route('/library')
def library():
    connection = get_library_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM AUTHOR")
            authors = cursor.fetchall()
            cursor.execute("SELECT * FROM BOOK")
            books = cursor.fetchall()
    finally:
        connection.close()
    return render_template('library.html', authors=authors, books=books)

#F2.2 Add a book.
@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form.get('title')
    price = request.form.get('price')
    author_id = request.form.get('author_id')
    connection = get_library_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO BOOK (title, price, author_id) VALUES (%s, %s, %s)", (title, price, author_id))
        connection.commit()
    finally:
        connection.close()
    return redirect(url_for('library'))

#F2.2 add an author.
@app.route('/add_author', methods=['POST'])
def add_author():
    name = request.form.get('name')
    country = request.form.get('country')
    connection = get_library_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO AUTHOR (name, country) VALUES (%s, %s)", (name, country))
        connection.commit()
    finally:
        connection.close()
    return redirect(url_for('library'))

#F2.3 Edit a book.
@app.route('/edit_book/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    connection = get_library_connection()
    try:
        if request.method == 'POST':
            title = request.form.get('title')
            price = request.form.get('price')
            author_id = request.form.get('author_id')
            with connection.cursor() as cursor:
                cursor.execute("UPDATE BOOK SET title=%s, price=%s, author_id=%s WHERE book_id=%s", (title, price, author_id, id))
            connection.commit()
            return redirect(url_for('library'))
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM BOOK WHERE book_id = %s", (id))
            book = cursor.fetchone()
            cursor.execute("SELECT * FROM AUTHOR")
            authors = cursor.fetchall()
    finally:
        connection.close()
    return render_template('edit_book.html', book=book, authors=authors)

# F2.3 edit an author.
@app.route('/edit_author/<int:id>', methods=['GET', 'POST'])
def edit_author(id):
    connection = get_library_connection()
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            country = request.form.get('country')
            with connection.cursor() as cursor:
                cursor.execute("UPDATE AUTHOR SET name=%s, country=%s WHERE author_id=%s", (name, country, id))
            connection.commit()
            return redirect(url_for('library'))
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM AUTHOR WHERE author_id = %s", (id))
            author = cursor.fetchone()
    finally:
        connection.close()
    return render_template('edit_author.html', author=author)


# F2.4 Remove a book.
@app.route('/delete_book/<int:id>', methods=['POST'])
def delete_book(id):
    connection = get_library_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM BOOK WHERE book_id = %s", (id))
        connection.commit()
    finally:
        connection.close()
    return redirect(url_for('library'))

# F2.5 Remove an author.
@app.route('/delete_author/<int:id>', methods=['POST'])
def delete_author(id):
    connection = get_library_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM AUTHOR WHERE author_id = %s", (id))
        connection.commit()
    finally:
        connection.close()
    return redirect(url_for('library'))


if __name__ == '__main__':
    app.run(debug=True)