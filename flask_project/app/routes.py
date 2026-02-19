from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import get_db_connection

main = Blueprint('main', __name__)

# Register
@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    hashed_password = generate_password_hash(password)

    conn = get_db_connection()
    try:
        conn.execute(
            'INSERT INTO users (username, password) VALUES (?, ?)',
            (username, hashed_password)
        )
        conn.commit()
    except:
        return jsonify({"error": "User already exists"}), 400
    finally:
        conn.close()

    return jsonify({"message": "User registered successfully"}), 201

# Login
@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE username=?',
        (username,)
    ).fetchone()
    conn.close()

    if user and check_password_hash(user['password'], password):
        session['user'] = username
        return jsonify({"message": "Login successful"})

    return jsonify({"error": "Invalid credentials"}), 401

# Protected Route
@main.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({"message": f"Welcome {session['user']}!"})
