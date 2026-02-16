from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Initialize Database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Home
@app.route('/')
def home():
    return redirect('/login')

# Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']  # admin or user

        hashed_password = generate_password_hash(password)

        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
                (username, email, hashed_password, role)
            )
            conn.commit()
            conn.close()
            flash("Registration Successful! Please Login.", "success")
            return redirect('/login')
        except:
            flash("Username or Email already exists!", "danger")
            return redirect('/register')
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            session['user'] = username
            session['role'] = user[4]  # Save role in session
            flash("Login Successful!", "success")
            # Redirect based on role
            if user[4] == 'admin':
                return redirect('/admin_dashboard')
            else:
                return redirect('/user_dashboard')
        else:
            flash("Invalid Username or Password!", "danger")
            return redirect('/login')

    return render_template('login.html')

# Admin Dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user' in session and session.get('role') == 'admin':
        return render_template('admin_dashboard.html', username=session['user'])
    else:
        flash("Access Denied!", "danger")
        return redirect('/login')

# User Dashboard
@app.route('/user_dashboard')
def user_dashboard():
    if 'user' in session and session.get('role') == 'user':
        return render_template('user_dashboard.html', username=session['user'])
    else:
        flash("Access Denied!", "danger")
        return redirect('/login')

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('role', None)
    flash("Logged Out Successfully!", "success")
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
