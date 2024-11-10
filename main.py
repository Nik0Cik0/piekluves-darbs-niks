from datetime import date
from flask import Flask, render_template, request, url_for, redirect, jsonify, session, flash
import dbMethods
import hashlib
import sqlite3
from werkzeug.utils import secure_filename
import os
from flask import session
import subprocess
import tempfile

app = Flask('app')
app.secret_key = 'Niks_megina_saprast_flask_login'

#pamatlapa - lapa, ko lietotājs satiek uzsākot lietot produktu

@app.route('/')
def index():
  #dbMethods.createTables()
  #dbMethods.populateCourses()
  #dbMethods.populateLessons()
  #dbMethods.populateProgress()
  #dbMethods.populateUsers() #// šito populatot tikai debugging nolūkos
  return render_template ("index.html")

#autorizēšanās lapa

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        email_hash = hashlib.sha256(email.encode()).hexdigest()
        passwd = request.form['password']
        passwd2 = hashlib.sha256(passwd.encode())
        password = passwd2.hexdigest()

        userExists, userID = dbMethods.checkIfUserExists(email_hash, password)
        if userExists:
            session['userID'] = userID
            # Check if user has profile picture
            user = dbMethods.getUser(userID)
            if user and user[9]:
                session['profile_picture'] = True
            return redirect(url_for('user_page'))
        else:
            return render_template("login.html")
    return render_template("login.html")

#reģistrēšanās lapa

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        email = hashlib.sha256(request.form['email'].encode()).hexdigest()
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        username = request.form['username']
        class_num = request.form['class']
        subclass = request.form['subclass']
        birthdate = request.form['birthdate']
        description = request.form['description']
        
        dbMethods.register(username, password, email, class_num, subclass, birthdate, description)
        return redirect(url_for('login'))
        
    return render_template("register.html")
  
#lietotāja skata lapa

@app.route('/page')
def user_page():
    if 'userID' not in session:
        return redirect(url_for('login'))
    
    courses = dbMethods.showAllCourses()
    processed_courses = []
    
    for course in courses:
        total_lessons = dbMethods.countLessonsInCourse(course[0])
        completed_lessons = dbMethods.countCompletedLessons(session['userID'], course[0])
        progress_percentage = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
        
        # Create new course tuple with all the original data plus the lessons ratio
        processed_course = list(course)
        processed_course[2] = f"{completed_lessons}/{total_lessons}"  # Replace Hours with ratio
        processed_course.append(progress_percentage)  # Add progress percentage
        processed_courses.append(tuple(processed_course))
    
    return render_template('page.html', p2=processed_courses)
    
#administrātora skata lapa/admina panelis

@app.route('/mainpage')
def mainpage():
    courseID = request.args.get('courseid')
    userID = request.args.get('id')
    lessonID = request.args.get('lessonid')
    progressID = request.args.get('progressid')  
    #dzest lietotaju ar noteiktu ID
    if userID is not None:
        dbMethods.deleteUserByID(userID)
        return redirect('mainpage')
    #dzest kursu ar noteiktu ID
    elif courseID is not None:
        dbMethods.deleteCourseByID(courseID)
        return redirect('mainpage')
    #dzest stundu ar noteiktu ID
    elif lessonID is not None:
        dbMethods.deleteLessonByID(lessonID)
        return redirect('mainpage')
    #dzest progresu ar noteiktu ID
    elif progressID is not None:
        dbMethods.deleteProgressByID(progressID)  
        return redirect('mainpage')
    else:
        users = dbMethods.showAllUsers()
        courses = dbMethods.showAllCourses()
        lessons = dbMethods.showAllLessons()
        progress = dbMethods.showAllProgress()  
        return render_template("mainpage.html", p1=users, p2=courses, p3=lessons, p4=progress)

#lietotāja sesijas pārtraukšana

@app.route('/logout')
def logout():
    session.pop('userID', None)
    session.pop('profile_picture', None)
    return redirect(url_for('login'))  

######### Editot, dzēst vai labot ____ #########

#labot, pievienot user#
@app.route('/edituser',methods=["GET","POST"])
def edituser():
  if request.method == 'POST':
    userid = request.form['id']
    username = request.form['username']
    passwd = request.form['password']
    passwd2 = hashlib.sha256(passwd.encode())
    password = passwd2.hexdigest()
    eml = request.form['email']
    eml2 = hashlib.sha256(eml.encode())
    email = eml2.hexdigest()
    klase = request.form['klase']
    subclass = request.form['subclass']
    date = request.form['date']
    desc = request.form['desc']
    xp = request.form['xp']
    dbMethods.updateUser(userid,username,password,email,klase,subclass,date,desc,xp)
    return redirect("mainpage")
  else:
    userID = request.args.get('id')
    user = dbMethods.getUser(userID)
    return render_template("edituser.html",p1=user)

@app.route('/adduser',methods=["GET","POST"])
def adduser():
  if request.method == 'POST':
    usrnm = request.form['username']
    passwd = request.form['password']
    passwd2 = hashlib.sha256(passwd.encode())
    password = passwd2.hexdigest()
    email = request.form['email']
    email_hash = hashlib.sha256(email.encode()).hexdigest()
    klase = request.form['klase']
    subclass = request.form['subclass']
    date = request.form['date']
    desc = request.form['desc']
    xp = request.form.get('xp', 0)  # Default to 0 if not provided
    
    dbMethods.adduser(usrnm, password, email_hash, klase, subclass, date, desc, xp)
    return redirect("mainpage")
  else:
    return render_template("adduser.html")


#labot, pievienot course#
@app.route('/editcourse', methods=["GET", "POST"])
def editcourse():
    if request.method == 'POST':
        courseid = request.form['courseid']
        name = request.form['name']
        count = request.form['count']
        level = request.form['level']
        desc = request.form['desc']
        color = request.form['color']
        tcolor = request.form['tcolor']
        
        img_file = request.files.get('img')
        img_blob = img_file.read() if img_file else None
    
        dbMethods.updatecourse(courseid, name, count, level, desc, color, tcolor, img_blob)
        return redirect(url_for('mainpage'))
    
    else:
        courseID = request.args.get('courseid')
        if courseID:
            course = dbMethods.getCourse(courseID)
            if course:
                return render_template("editcourse.html", p2=course)
        
        return render_template("error.html", message="Kurss nav atrasts"), 404

@app.route('/addcourse', methods=["GET", "POST"])
def addcourse():
    if request.method == 'POST':
        name = request.form['name']
        count = request.form['count']
        level = request.form['level']
        desc = request.form['desc']
        color = request.form['color']
        tcolor = request.form['tcolor']
        
        img_file = request.files.get('img')
        
        if img_file and img_file.filename:
            img_filename = secure_filename(img_file.filename)
            img_path = os.path.join('static/images', img_filename)
            img_file.save(img_path)  
            dbMethods.addcourse(name, count, level, desc, color, tcolor, img_path)
        else:
            dbMethods.addcourse(name, count, level, desc, color, tcolor, None)
        
        return redirect("mainpage")
    return render_template("addcourse.html")

#labot, pievienot lesson#
@app.route('/editlesson', methods=["GET", "POST"])
def editlesson():
    if request.method == 'POST':
        lessonid = request.form['lessonid']
        courseid = request.form['courseid']
        title = request.form['name']
        description = request.form['desc']
        
        # Handle content from either textarea or file
        content_file = request.files.get('content_file')
        if content_file and content_file.filename:
            # Read content from uploaded file
            content = content_file.read().decode('utf-8')
        else:
            # Use content from textarea
            content = request.form['saturs']
            
        dbMethods.updatelesson(lessonid, courseid, title, description, content)
        return redirect(url_for('mainpage'))
    else:
        lessonID = request.args.get('lessonid')
        lesson = dbMethods.getLesson(lessonID)
        return render_template("editlesson.html", p3=lesson)

@app.route('/addlesson', methods=["GET", "POST"])
def addlesson():
    if request.method == 'GET':
        return render_template("addlesson.html")
    else:
        courseid = request.form['courseid']
        title = request.form['name']
        description = request.form['desc']
        
        # Handle content from either textarea or file
        content_file = request.files.get('content_file')
        if content_file and content_file.filename:
            # Read content from uploaded file
            content = content_file.read().decode('utf-8')
        else:
            # Use content from textarea
            content = request.form['saturs']
            
        dbMethods.addlesson(courseid, title, description, content)
        return redirect("mainpage")


#labot, pievienot Progress#

@app.route('/editprogress', methods=["GET", "POST"])  
def editprogress():
    if request.method == 'POST':
        progressid = request.form['progressid']  
        userid = request.form['userid']
        lessonid = request.form['lessonid']
        description = request.form['description']
        status = request.form['status']
        dbMethods.updateprogress(progressid, userid, lessonid, description, status)  
        return redirect("mainpage")
    else:
        progressID = request.args.get('progressid')  
        progress = dbMethods.getProgress(progressID)  
        return render_template("editprogress.html", p4=progress)


@app.route('/addprogress', methods=["GET", "POST"])  
def addprogress():
    if request.method == 'GET':
        return render_template("addprogress.html")
    else:
        userid = request.form['userid']
        lessonid = request.form['lessonid']
        description = request.form['description']
        status = request.form['status']
        dbMethods.addprogress(userid, lessonid, description, status)  
        return redirect("mainpage")

#labot profila informāciju (lietotājiem)

@app.route('/editprofile', methods=["GET", "POST"])
def editprofile():
    if 'userID' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        userid = request.form['id']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        klase = request.form['klase']
        subclass = request.form['subclass']
        date = request.form['birthdate']
        desc = request.form['description']
        xp = request.form['xp']
        
        # Handle profile picture upload
        profile_picture = request.files.get('profile_picture')
        if profile_picture and allowed_file(profile_picture.filename):
            if len(profile_picture.read()) <= MAX_FILE_SIZE:
                profile_picture.seek(0)
                picture_data = profile_picture.read()
                dbMethods.updateUserWithPicture(userid, username, password, email, 
                                              klase, subclass, date, desc, xp, picture_data)
                session['profile_picture'] = True
            else:
                flash('File size too large. Maximum size is 5MB.')
                return redirect(request.url)
        else:
            dbMethods.updateUser(userid, username, password, email, 
                               klase, subclass, date, desc, xp)
            
        return redirect(url_for("user_page"))
    else:
        userID = request.args.get('id')
        user = dbMethods.getUser(userID)
        # Check if user has profile picture and update session
        if user and user[9]:
            session['profile_picture'] = True
        return render_template("editprofile.html", p1=user)

#Kursa pieejamo stundu apskatīšana

@app.route('/course/<int:course_id>/lessons')
def view_lessons(course_id):    
    course_id = int(course_id)
    course = dbMethods.getCourse(course_id)
    user_id = session.get('userID')
    lessons = dbMethods.getLessonsByCourse(course_id, user_id)
    
    return render_template('course_lessons.html', course=course, lessons=lessons)

#stundas status maiņa uz "progresā"

@app.route('/update_progress/<int:lesson_id>', methods=['GET'])
def update_lesson_progress(lesson_id):
    user_id = session.get('userID')  
    if user_id:
        dbMethods.update_lesson_progress(user_id, lesson_id, 'progresā') 
        course_id = dbMethods.get_course_by_lesson(lesson_id)
        return redirect(url_for('view_lesson', course_id=course_id, lesson_id=lesson_id))
    else:
        return redirect(url_for('login'))

#stundas status maiņa uz "pabeigts"

@app.route('/complete_lesson/<int:lesson_id>', methods=['POST'])
def complete_lesson(lesson_id):
    user_id = session.get('userID') 
    if user_id:
        dbMethods.update_lesson_progress(user_id, lesson_id, 'pabeigts')
        dbMethods.add_xp_for_lesson(user_id)  # Add XP when completing lesson
        course_id = dbMethods.get_course_by_lesson(lesson_id)
        return redirect(url_for('view_lessons', course_id=course_id))
    else:
        return redirect(url_for('login'))

#stundas satura apmeklēšana

@app.route('/course/<int:course_id>/lessons/<int:lesson_id>')
def view_lesson(course_id, lesson_id):
    user_id = session.get('userID')
    lesson = dbMethods.getLesson(lesson_id)
    course = dbMethods.getCourse(course_id)
    progress = dbMethods.getProgressByLessonAndUser(lesson_id, user_id)

    if lesson and course:
        return render_template('view_lesson.html', lesson=lesson, course=course, progress=progress)
    else:
        return render_template('error.html', message="Lesson or course not found."), 404

#kursu attēlu attēlošana

@app.route('/course_icon/<int:course_id>')
def course_icon(course_id):
   conn = sqlite3.connect('database.sql')
   c = conn.cursor()
   c.execute("SELECT Icon FROM Courses WHERE Course_ID = ?", (course_id,))
   img_data = c.fetchone()[0]
   conn.close()

   return app.response_class(img_data, mimetype='image/png')

@app.route('/courses')
def courses():
    # ... existing code ...
    
    # For each course, calculate progress
    courses_with_progress = []
    for course in courses:
        # Get total lessons in course
        cursor.execute("SELECT COUNT(*) FROM lessons WHERE course_id = ?", (course[0],))
        total_lessons = cursor.fetchone()[0]
        
        # Get completed lessons for this user and course
        cursor.execute("""
            SELECT COUNT(*) FROM completed_lessons 
            WHERE user_id = ? AND lesson_id IN 
                (SELECT id FROM lessons WHERE course_id = ?)
        """, (session['userID'], course[0]))
        completed_lessons = cursor.fetchone()[0]
        
        # Calculate progress percentage
        progress = round((completed_lessons / total_lessons * 100) if total_lessons > 0 else 0)
        
        # Add progress to course data
        courses_with_progress.append(course + (progress,))
    
    return render_template('page.html', p2=courses_with_progress)

@app.route('/debug')
def debug():
    conn = sqlite3.connect('database.sql')
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(Courses)")
    columns = cursor.fetchall()
    conn.close()
    return str(columns)

# Sandbox routes
@app.route('/sandbox')
def sandbox():
    if 'userID' not in session:
        return redirect(url_for('login'))
    
    # Pass the session user ID to the template
    return render_template('sandbox.html', session=session)

@app.route('/run-code', methods=['POST'])
def run_code():
    if 'userID' not in session:
        return jsonify({'output': 'Please login first'})
        
    data = request.get_json()
    code = data.get('code')
    language = data.get('language')
    
    try:
        # Create a temporary directory for our files
        with tempfile.TemporaryDirectory() as temp_dir:
            process = None  # Initialize process variable
            
            if language == 'python':
                file_path = os.path.join(temp_dir, 'code.py')
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(code)
                
                process = subprocess.run(
                    ['python', file_path],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
            elif language == 'javascript':
                file_path = os.path.join(temp_dir, 'code.js')
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(code)
                
                process = subprocess.run(
                    ['node', file_path],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
            
            else:
                return jsonify({'output': 'Unsupported language'})
            
            # Check if process was executed
            if process is None:
                return jsonify({'output': 'Error: Code execution failed'})
                
            # Return the output
            if process.returncode == 0:
                return jsonify({'output': process.stdout})
            else:
                return jsonify({'output': f'Runtime Error:\n{process.stderr}'})
                
    except subprocess.TimeoutExpired:
        return jsonify({'output': 'Code execution timed out (5 second limit)'})
    except Exception as e:
        return jsonify({'output': f'Error: {str(e)}'})

# Simplified requirements check
def check_requirements():
    requirements = {
        'python': 'python --version',
        'node': 'node --version'
    }
    
    missing = []
    for req, cmd in requirements.items():
        try:
            subprocess.run(cmd.split(), capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing.append(req)
    
    if missing:
        print(f"Warning: The following requirements are missing: {', '.join(missing)}")
        print("Some language features may not be available.")

# Add this to your app initialization

@app.route('/lideri')
def lideri():
    if 'userID' not in session:
        return redirect(url_for('login'))
    leaders = dbMethods.get_top_users(10)  # Get top 10 users
    return render_template('lideri.html', leaders=leaders)

# Add these constants at the top of your file, after the imports
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB limit

# Add this function before your routes
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/get_profile_picture/<int:user_id>')
def get_profile_picture(user_id):
    picture_data = dbMethods.get_profile_picture(user_id)
    if picture_data:
        return app.response_class(picture_data, mimetype='image/jpeg')
    return redirect(url_for('static', filename='images/default_profile.png'))

if __name__ == "__main__":
    check_requirements()
    app.run(host='0.0.0.0', port=8080)