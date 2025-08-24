from flask import Flask, render_template, request, redirect, url_for, jsonify
import logging
import sqlite3
import os

# Set up logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('lms.db')
    c = conn.cursor()
    
    # Create tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER,
            title TEXT NOT NULL,
            content TEXT,
            FOREIGN KEY (course_id) REFERENCES courses (id)
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            FOREIGN KEY (course_id) REFERENCES courses (id)
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            course_id INTEGER,
            completed BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (course_id) REFERENCES courses (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Routes
@app.route('/')
def index():
    conn = sqlite3.connect('lms.db')
    c = conn.cursor()
    c.execute('SELECT * FROM courses')
    courses = c.fetchall()
    conn.close()
    return render_template('index.html', courses=courses)

@app.route('/course/<int:course_id>')
def course_detail(course_id):
    conn = sqlite3.connect('lms.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM courses WHERE id = ?', (course_id,))
    course = c.fetchone()
    
    c.execute('SELECT * FROM lessons WHERE course_id = ?', (course_id,))
    lessons = c.fetchall()
    
    c.execute('SELECT * FROM quizzes WHERE course_id = ?', (course_id,))
    quizzes = c.fetchall()
    
    conn.close()
    
    return render_template('course_detail.html', course=course, lessons=lessons, quizzes=quizzes)

@app.route('/upload', methods=['GET', 'POST'])
def upload_course():
    logging.debug("Upload course route accessed.")
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        
        conn = sqlite3.connect('lms.db')
        c = conn.cursor()
        c.execute('INSERT INTO courses (title, description) VALUES (?, ?)', (title, description))
        conn.commit()
        conn.close()
        
        logging.debug("Course uploaded successfully.")
        return redirect(url_for('index'))
    
    return render_template('upload_course.html')

@app.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
def take_quiz(quiz_id):
    conn = sqlite3.connect('lms.db')
    c = conn.cursor()
    
    if request.method == 'POST':
        user_answer = request.form['answer']
        c.execute('SELECT answer FROM quizzes WHERE id = ?', (quiz_id,))
        correct_answer = c.fetchone()[0]
        
        is_correct = user_answer.lower() == correct_answer.lower()
        
        conn.close()
        return render_template('quiz_result.html', is_correct=is_correct, correct_answer=correct_answer)
    
    c.execute('SELECT * FROM quizzes WHERE id = ?', (quiz_id,))
    quiz = c.fetchone()
    conn.close()
    
    return render_template('take_quiz.html', quiz=quiz)

@app.route('/progress/<int:user_id>/<int:course_id>', methods=['POST'])
def track_progress(user_id, course_id):
    completed = request.json.get('completed', False)
    
    conn = sqlite3.connect('lms.db')
    c = conn.cursor()
    
    # Check if progress already exists
    c.execute('SELECT * FROM user_progress WHERE user_id = ? AND course_id = ?', (user_id, course_id))
    existing = c.fetchone()
    
    if existing:
        c.execute('UPDATE user_progress SET completed = ? WHERE user_id = ? AND course_id = ?', 
                 (completed, user_id, course_id))
    else:
        c.execute('INSERT INTO user_progress (user_id, course_id, completed) VALUES (?, ?, ?)',
                 (user_id, course_id, completed))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
