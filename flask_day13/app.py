from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create table if not exists
def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_table()

@app.route('/')
def home():
    return "SQLite CRUD API Running"

# CREATE
@app.route('/api/user', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({"error": "Name required"}), 400

    conn = get_db_connection()
    conn.execute('INSERT INTO users (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()

    return jsonify({"message": "User added successfully"}), 201

# READ ALL
@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()

    user_list = [dict(user) for user in users]
    return jsonify(user_list)

# UPDATE
@app.route('/api/user/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    name = data.get('name')

    conn = get_db_connection()
    conn.execute('UPDATE users SET name=? WHERE id=?', (name, id))
    conn.commit()
    conn.close()

    return jsonify({"message": "User updated"})

# DELETE
@app.route('/api/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id=?', (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "User deleted"})

if __name__ == '__main__':
    app.run(debug=True)
