# Simple LMS Platform

A lightweight Learning Management System built with Flask and SQLite.

## Features

- **Course Management**: Upload and view courses
- **Lessons**: Each course can have multiple lessons
- **Quizzes**: Interactive quizzes for each course
- **User Progress**: Track completion status for courses
- **Simple Interface**: Clean and easy-to-use web interface

## Setup

1. Install Python dependencies:
   ```bash
   pip install flask
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. Open your browser and go to: http://127.0.0.1:5000

## Usage

1. **View Courses**: The homepage shows all available courses
2. **Upload Course**: Click "Upload New Course" to add a new course
3. **View Course Details**: Click on any course to see its lessons and quizzes
4. **Take Quizzes**: Click on any quiz to test your knowledge
5. **Track Progress**: The system automatically tracks your quiz results

## Database

The application uses SQLite and automatically creates the database with the following tables:
- `courses`: Stores course information
- `lessons`: Stores lesson content for each course
- `quizzes`: Stores quiz questions and answers
- `user_progress`: Tracks user completion status

## API Endpoints

- `GET /`: List all courses
- `GET /course/<course_id>`: View course details
- `GET /upload`: Upload form for new courses
- `POST /upload`: Process course upload
- `GET /quiz/<quiz_id>`: Take a quiz
- `POST /quiz/<quiz_id>`: Submit quiz answers
- `POST /progress/<user_id>/<course_id>`: Update user progress

## File Structure

```
.
├── app.py              # Main Flask application
├── templates/          # HTML templates
│   ├── index.html      # Course list
│   ├── course_detail.html # Course details
│   ├── upload_course.html # Course upload form
│   ├── take_quiz.html  # Quiz interface
│   └── quiz_result.html # Quiz results
├── lms.db             # SQLite database (created automatically)
└── README.md          # This file
```

## Optional Features

The application includes stubs for optional payment integration that can be extended with payment gateway APIs like Stripe or PayPal.
