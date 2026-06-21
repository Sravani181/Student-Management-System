from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        course TEXT
    )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('students.db')
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()

    return render_template('index.html', students=students)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    email = request.form['email']
    course = request.form['course']

    conn = sqlite3.connect('students.db')
    conn.execute(
        'INSERT INTO students(name,email,course) VALUES (?,?,?)',
        (name, email, course)
    )
    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)