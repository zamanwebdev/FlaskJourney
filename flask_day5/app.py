from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database initialize
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# Home Page (Read + Create Form)
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    conn.close()

    return render_template('index.html', notes=notes)

# Create Note
@app.route('/add', methods=['POST'])
def add_note():
    title = request.form['title']
    content = request.form['content']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
    conn.commit()
    conn.close()

    return redirect('/')

# Delete Note
@app.route('/delete/<int:id>')
def delete_note(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/')

# Edit Page
@app.route('/edit/<int:id>')
def edit_note(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE id=?", (id,))
    note = cursor.fetchone()
    conn.close()

    return render_template('edit.html', note=note)

# Update Note
@app.route('/update/<int:id>', methods=['POST'])
def update_note(id):
    title = request.form['title']
    content = request.form['content']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE notes SET title=?, content=? WHERE id=?", (title, content, id))
    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
