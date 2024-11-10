# CodeLatvian Learning Platform

## Overview
CodeLatvian is a web-based learning platform designed to help users learn programming through structured courses. The platform features user authentication, course management, progress tracking, and an XP-based leaderboard system, all in Latvian language.

## Features

### User Management
- User registration and authentication with SHA-256 encryption
- Profile customization with profile pictures
- Progress tracking and XP system
- Admin panel for user administration
- Secure session management

### Course System
- Structured programming courses
- Progress tracking for each course
- Visual progress indicators
- Course difficulty levels
- Custom course icons and styling
- Interactive lessons

### Learning Features
- Interactive code editor with syntax highlighting
- Support for multiple programming languages (Python, JavaScript)
- Real-time code execution environment
- Live preview for HTML/CSS/JS code
- Progress tracking per lesson
- XP rewards system
- Leaderboard rankings

### Admin Features
- Comprehensive user management
- Course content management
- Lesson creation and editing
- Progress monitoring
- System administration tools

## Technical Stack
- Backend: Python Flask
- Database: SQLite
- Frontend: HTML, CSS, JavaScript
- Code Editor: CodeMirror
- Authentication: SHA-256 encryption
- Code Execution: Python & Node.js support

## Database Structure

### Users Table
```sql
CREATE TABLE Users(
    User_ID INTEGER PRIMARY KEY,
    Username VARCHAR(50) NOT NULL,
    DisplayName VARCHAR(50) NOT NULL,
    Password VARCHAR(64) NOT NULL,
    Email VARCHAR(64) NOT NULL,
    Class INT,
    SubClass VARCHAR(10),
    BirthDate DATE,
    Description VARCHAR(500),
    XP INTEGER DEFAULT 0,
    ProfilePicture BLOB
);
```

### Courses Table
```sql
CREATE TABLE Courses (
    Course_ID INTEGER PRIMARY KEY,
    Course_Name VARCHAR(100) NOT NULL,
    Hours INT,
    Level VARCHAR(50),
    Description VARCHAR(500),
    Color VARCHAR(6),
    TColor VARCHAR(6),
    Icon BLOB
);
```

### Lessons Table
```sql
CREATE TABLE Lessons (
    Lesson_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Course_ID INTEGER,
    Title TEXT NOT NULL,
    Description TEXT,
    Content TEXT,
    FOREIGN KEY (Course_ID) REFERENCES Courses(Course_ID)
);
```

### Progress Table
```sql
CREATE TABLE Progress(
    Progress_ID INTEGER PRIMARY KEY,
    User_ID INTEGER,
    Lesson_ID INTEGER,
    Description VARCHAR(500),
    Status VARCHAR(50) DEFAULT 'not started',
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (Lesson_ID) REFERENCES Lessons(Lesson_ID)
);
```

## Setup Instructions

1. Clone the repository
```bash
git clone https://github.com/yourusername/codelatvian.git
cd codelatvian
```

2. Create and activate virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install required dependencies
```bash
pip install flask hashlib werkzeug
```

4. Initialize the database
```python
# Run these commands in Python console or uncomment in main.py
dbMethods.createTables()
dbMethods.populateCourses()
dbMethods.populateLessons()
dbMethods.populateProgress()
dbMethods.populateUsers()
```

5. Run the application
```bash
python main.py
```

The application will be available at `http://localhost:8080`

## Routes

### Public Routes
- `/` - Landing page
- `/login` - User login
- `/register` - New user registration

### Authenticated Routes
- `/page` - User dashboard
- `/course/<course_id>/lessons/<lesson_id>` - View lesson
- `/lideri` - Leaderboard
- `/editprofile` - Edit user profile
- `/sandbox` - Code testing environment

### Admin Routes
- `/mainpage` - Admin dashboard
- `/edituser` - Edit user details
- `/adduser` - Add new user
- `/editcourse` - Edit course details
- `/addcourse` - Add new course
- `/editlesson` - Edit lesson content
- `/addlesson` - Add new lesson

## Security Features
- Password encryption using SHA-256
- Email address encryption
- Session-based authentication
- Secure file upload handling
- XSS protection
- CSRF protection
- Secure code execution environment

## Requirements
- Python 3.8+
- Node.js (for JavaScript code execution)
- Modern web browser
- Internet connection (for external resources)

## License
This project is licensed under the MIT License.

## Author
- Niks Kristiāns Karpovs

## Acknowledgments
- Flask framework
- CodeMirror editor
- SQLite database
- Font Awesome icons
