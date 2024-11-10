import sqlite3
import base64

#Izveidot tabulas#
def createTables():
  conn = sqlite3.connect('database.sql',timeout=10)
  c = conn.cursor()
  
  SQL_statement1 = """
  CREATE TABLE IF NOT EXISTS Users(
  User_ID INTEGER PRIMARY KEY,
  Username VARCHAR(50) NOT NULL,
  Password VARCHAR(50) NOT NULL,
  Email VARCHAR(50),
  Class INT,
  SubClass VARCHAR(10),
  BirthDate DATE,
  Description VARCHAR(500),
  XP INTEGER DEFAULT 0,
  ProfilePicture BLOB
  );

  """
  
  SQL_statement2 = """
  CREATE TABLE IF NOT EXISTS Courses (
  Course_ID INTEGER PRIMARY KEY,
  Course_Name VARCHAR(100) NOT NULL,
  Hours INT,
  Level VARCHAR(50),
  Description VARCHAR(500),
  Color VARCHAR(6),
  TColor VARCHAR(6),
  Icon BLOB
  );

  """

  SQL_statement3 = """
  CREATE TABLE IF NOT EXISTS Lessons (
  Lesson_ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Course_ID INTEGER,
  Title TEXT NOT NULL,
  Description TEXT,
  Content TEXT,
  FOREIGN KEY (Course_ID) REFERENCES Courses(Course_ID)
  );
  """

  SQL_statement4 = """
  CREATE TABLE IF NOT EXISTS Progress(
  Progress_ID INTEGER PRIMARY KEY,
  User_ID INTEGER,
  Lesson_ID INTEGER,
  Description VARCHAR(500),
  Status VARCHAR(50) DEFAULT 'not started',
  FOREIGN KEY (User_ID) REFERENCES Users(User_ID),
  FOREIGN KEY (Lesson_ID) REFERENCES Lessons(Lesson_ID)
  );
  """

  c.execute(SQL_statement1)
  c.execute(SQL_statement2)
  c.execute(SQL_statement3)
  c.execute(SQL_statement4)
  conn.commit()
  c.close()
  conn.close()

#Papildināt tabulas#

def populateUsers():
  conn = sqlite3.connect('database.sql', timeout=10)
  c = conn.cursor()

  SQL_statement1 = """
  INSERT INTO Users VALUES (NULL, '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'admin@gmail.com', 12, 'b', '2006-04-12', 'Esmu admins', 100, '');
  """
  SQL_statement2 = """
  INSERT INTO Users VALUES (NULL, 'OskorkSister', 'f4b19f1f1a4d80054a55c850840d283ee4f12c59146f0ffef8c2c1dce9559517', 'oskars@gmail.com', 19, 'b', '1997-10-03', 'Maņi apbižo skolā', 50,'');
  """
  SQL_statement3 = """
  INSERT INTO Users VALUES (NULL, 'admin', '2bd4514cc641566b6bca97f0299e73aab9bd12bebc766fe4f0b8ca811da5d463', 'admin@inbox.lv', 10, 'c', '2007-11-22', 'esmu fake admins', 30,'');
  """

  c.execute(SQL_statement1)
  c.execute(SQL_statement2)
  c.execute(SQL_statement3)
  conn.commit()
  c.close()
  conn.close()

def populateCourses():
  conn = sqlite3.connect('database.sql', timeout=10)
  c = conn.cursor()

  SQL_statement1 = """
  INSERT INTO Courses VALUES (NULL, 'Python', 10, 'Iesācējiem', 'Ideāls kurss bez iepriekšējām zināšanām.', '161B30', 'fff', NULL);
  """
  SQL_statement2 = """
  INSERT INTO Courses VALUES (NULL, 'JavaScript', 12, 'Vidējam līmenim', 'Padziļināta mācīšanās par JavaScript.', 'FBC933', '000', NULL);
  """
  SQL_statement3 = """
  INSERT INTO Courses VALUES (NULL, 'SQL', 8, 'Iesācējiem', 'Ievads datubāzu pārvaldībā.', '2B355F',  'fff', NULL);
  """

  c.execute(SQL_statement1)
  c.execute(SQL_statement2)
  c.execute(SQL_statement3)
  conn.commit()
  c.close()
  conn.close()

def populateLessons():
  conn = sqlite3.connect('database.sql', timeout=10)
  c = conn.cursor()

  SQL_statement1 = """
  INSERT INTO Lessons VALUES (NULL, 1, 'Python pamati', 'Šajā stundā tiks apgūtas Python pamatfunkcijas.', 'cccccccccccccc');
  """
  SQL_statement2 = """
  INSERT INTO Lessons VALUES (NULL, 1, 'OOP Python', 'Ievads objektorientētā programmēšanā Python.', 'bbbbbbbbb');
  """
  SQL_statement3 = """
  INSERT INTO Lessons VALUES (NULL, 2, 'JavaScript pamati', 'JavaScript sintakse un pamatkoncepcijas.', 'aaaaaaaaaaaaa');
  """

  c.execute(SQL_statement1)
  c.execute(SQL_statement2)
  c.execute(SQL_statement3)
  conn.commit()
  c.close()
  conn.close()

def populateProgress():
    conn = sqlite3.connect('database.sql', timeout=10)
    c = conn.cursor()

    SQL_statement1 = """
    INSERT INTO Progress (User_ID, Lesson_ID, Description, Status) 
    VALUES (1, 1, 'Izpildīti 13/14', 'progresā');
    """
    SQL_statement2 = """
    INSERT INTO Progress (User_ID, Lesson_ID, Description, Status) 
    VALUES (2, 2, 'Izpildīti 0/10', 'nav uzsākts');
    """
    SQL_statement3 = """
    INSERT INTO Progress (User_ID, Lesson_ID, Description, Status) 
    VALUES (3, 3, 'Izpildīti 8/8', 'pabeigts');
    """

    c.execute(SQL_statement1)
    c.execute(SQL_statement2)
    c.execute(SQL_statement3)
    conn.commit()
    c.close()
    conn.close()

#Lietotaja parbaude#

def checkIfUserExists(email, password):
    userExists = False
    conn = sqlite3.connect('database.sql', timeout=10)
    c = conn.cursor()
    SQL_statement1 = """
        SELECT User_ID FROM Users WHERE Email = ? AND Password = ?;
    """
    c.execute(SQL_statement1, (email, password))
    result = c.fetchone()
    c.close()
    conn.close()
    if result:
        userExists = True
        return userExists, result[0]
    return userExists, None

#Lietotaja reģistrēšana#

def register(username, password, email, class_num, subclass, birthdate, description):
    conn = sqlite3.connect('database.sql', timeout=10)
    c = conn.cursor()
    SQL_statement = """
        INSERT INTO Users (Username, Password, Email, Class, SubClass, BirthDate, Description, XP)
        VALUES (?, ?, ?, ?, ?, ?, ?, 0);
    """
    c.execute(SQL_statement, (username, password, email, class_num, subclass, birthdate, description))
    conn.commit()
    c.close()
    conn.close()
    return True





#Funkcijas, kuras atlasa VISUS lietotājus/kursus/stundas/progressu no DB

def showAllUsers():
  conn = sqlite3.connect('database.sql',timeout=10)
  c = conn.cursor()
  SQL_statement1 = """
    SELECT * FROM Users;
  """
  c.execute(SQL_statement1)
  result = c.fetchall()
  c.close()
  conn.close()
  return result
    

def showAllCourses():
    conn = sqlite3.connect('database.sql')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Course_ID, Course_Name, Hours, Level, Description, Color, TColor, Icon 
        FROM Courses
    """)
    courses = cursor.fetchall()
    conn.close()
    return courses


  
def showAllLessons():
  conn = sqlite3.connect('database.sql',timeout=10)
  c = conn.cursor()
  SQL_statement1 = """
    SELECT * FROM Lessons;
  """
  c.execute(SQL_statement1)
  result = c.fetchall()
  c.close()
  conn.close()
  return result
  
def showAllProgress():
  conn = sqlite3.connect('database.sql',timeout=10)
  c = conn.cursor()
  SQL_statement1 = """
    SELECT * FROM Progress;
  """
  c.execute(SQL_statement1)
  result = c.fetchall()
  c.close()
  conn.close()
  return result      

######### Pievienot/Dzest/Labot #########

#Pievienot/Dzest/Labot User#

def getUser(userID):
    conn = sqlite3.connect('database.sql', timeout=10)
    c = conn.cursor()
    SQL_statement1 = """
        SELECT * FROM Users WHERE User_ID = ?;
    """
    c.execute(SQL_statement1, (userID,))
    result = c.fetchone()
    c.close()
    conn.close()
    return result

def updateUser(userid,username,password,email,klase,subclass,date,desc, xp):
  conn = sqlite3.connect('database.sql',timeout=10)
  c = conn.cursor()
  SQL_statement1 = """
    UPDATE Users SET Username = ?, Password = ?, Email = ?, Class = ?, SubClass = ?, BirthDate = ?, Description = ?, XP = ? WHERE User_ID = ?;
  """
  c.execute(SQL_statement1,(username,password,email,klase,subclass,date,desc,xp,userid))
  conn.commit()
  c.close()
  conn.close()
  return True

def deleteUserByID(userID):
  conn = sqlite3.connect('database.sql',timeout=10)
  c = conn.cursor()
  SQL_statement1 = """
    DELETE FROM Users WHERE User_ID = ?;
  """
  c.execute(SQL_statement1,(userID))
  conn.commit()
  c.close()
  conn.close()
  return True

def adduser(username, password, email, klase, subclass, date, desc, xp):
    conn = sqlite3.connect('database.sql', timeout=10)
    c = conn.cursor()
    SQL_statement1 = """
        INSERT INTO Users (Username, Password, Email, Class, SubClass, BirthDate, Description, XP)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """
    c.execute(SQL_statement1, (username, password, email, klase, subclass, date, desc, xp))
    conn.commit()
    c.close()
    conn.close()
    return True

#Pievienot/Dzest/Labot Course#

def getCourse(courseID):
    conn = sqlite3.connect('database.sql', timeout=10)
    c = conn.cursor()
    
    SQL_statement2 = """
        SELECT * FROM Courses WHERE Course_ID = ?;
    """

    
    c.execute(SQL_statement2, (courseID,)) 
    
    result = c.fetchone()  
    conn.close()

    return result



def updatecourse(courseid,name,count,level,desc,color,tcolor, img):
  conn = sqlite3.connect('database.sql',timeout=10)
  c = conn.cursor()
  SQL_statement2 = """
    UPDATE Courses SET Course_Name = ?, Hours = ?, Level = ?, Description = ?, Color = ?, Tcolor = ?, Icon = ? WHERE Course_ID = ?;
  """
  c.execute(SQL_statement2,(name,count,level,desc,color,tcolor,img,courseid))
  conn.commit()
  c.close()
  conn.close()
  return True

def deleteCourseByID(sweetsID):
  conn = sqlite3.connect('database.sql',timeout=10)
  c = conn.cursor()
  SQL_statement2 = """
    DELETE FROM Courses WHERE Course_ID = ?;
  """
  c.execute(SQL_statement2,(sweetsID))
  conn.commit()
  c.close()
  conn.close()
  return True

def addcourse(name, count, level, desc, color, tcolor, img):
    img_blob = None
    if img: 
        with open(img, 'rb') as file:
            img_blob = file.read() 

    conn = sqlite3.connect('database.sql')
    c = conn.cursor()
    c.execute("""
        INSERT INTO Courses (Course_Name, Hours, Level, Description, Color, TColor, Icon)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, count, level, desc, color, tcolor, img_blob))
    
    conn.commit()
    conn.close()



#Pievienot/Dzest/Labot Lesson#

def getLesson(lessonID):  
    conn = sqlite3.connect('database.sql', timeout=10)
    c = conn.cursor()
    SQL_statement3 = """
        SELECT * FROM Lessons WHERE Lesson_ID = ?;
    """
    c.execute(SQL_statement3, (lessonID,))
    result = c.fetchone()
    c.close()
    conn.close()
    return result

def updatelesson(lessonid, courseid, title, description, content):  
    conn = sqlite3.connect('database.sql')
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Lessons 
        SET Course_ID = ?, Title = ?, Description = ?, Content = ? 
        WHERE Lesson_ID = ?
    """, (courseid, title, description, content, lessonid))
    conn.commit()
    conn.close()
    return True

def deleteLessonByID(lessonID):  
    conn = sqlite3.connect('database.sql', timeout=10)
    c = conn.cursor()
    SQL_statement3 = """
        DELETE FROM Lessons WHERE Lesson_ID = ?;
    """
    c.execute(SQL_statement3, (lessonID,))
    conn.commit()
    c.close()
    conn.close()
    return True

def addlesson(courseid, title, description, content):
    conn = sqlite3.connect('database.sql')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Lessons (Course_ID, Title, Description, Content) 
        VALUES (?, ?, ?, ?)
    """, (courseid, title, description, content))
    conn.commit()
    conn.close()

#Pievienot/Dzest/Labot Progress#

def getProgress(progressID):  
    conn = sqlite3.connect('database.sql', timeout=10)
    c = conn.cursor()
    SQL_statement4 = """
        SELECT * FROM Progress WHERE Progress_ID = ?;
    """
    c.execute(SQL_statement4, (progressID,))
    result = c.fetchone()
    c.close()
    conn.close()
    return result


def updateprogress(progressid, userid, lessonid, description, status):  
    conn = sqlite3.connect('database.sql', timeout=10)
    c = conn.cursor()
    SQL_statement4 = """
        UPDATE Progress SET User_ID = ?, Lesson_ID = ?, Description = ?, Status = ? WHERE Progress_ID = ?;
    """
    c.execute(SQL_statement4, (userid, lessonid, description, status, progressid))
    conn.commit()
    c.close()
    conn.close()
    return True


def deleteProgressByID(progressID):  
    conn = sqlite3.connect('database.sql', timeout=10)
    c = conn.cursor()
    SQL_statement4 = """
        DELETE FROM Progress WHERE Progress_ID = ?;
    """
    c.execute(SQL_statement4, (progressID,))
    conn.commit()
    c.close()
    conn.close()
    return True


def addprogress(userid, lessonid, description, status):  
    conn = sqlite3.connect('database.sql', timeout=10)
    c = conn.cursor()
    SQL_statement4 = """
        INSERT INTO Progress (User_ID, Lesson_ID, Description, Status) VALUES (?, ?, ?, ?);
    """
    c.execute(SQL_statement4, (userid, lessonid, description, status))
    conn.commit()
    c.close()
    conn.close()
    return True


#funkcija, kas izvēlas visu informāciju par lietotāja , kurš ir autorizējies.
def getUserData(userID):
    conn = sqlite3.connect('database.sql', timeout=10)
    c = conn.cursor()
    SQL_statement1 = 'SELECT * FROM Users WHERE User_ID = '+userID+";"
    c.execute(SQL_statement1)
    user = c.fetchone()
    conn.commit()
    c.close()
    conn.close()
    if user is None:
        return None
    else:
        return user

#funkcija, kas izvēlas visas stundas noteiktam kursam.

def getLessonsByCourse(courseID, userID):
    conn = sqlite3.connect('database.sql', timeout=10)
    c = conn.cursor()
    
    SQL_statement = """
        SELECT l.Lesson_ID, l.Course_ID, l.Title, l.Description, l.Content, 
               IFNULL(p.Status, 'not started') as Status
        FROM Lessons l
        LEFT JOIN Progress p ON l.Lesson_ID = p.Lesson_ID AND p.User_ID = ?
        WHERE l.Course_ID = ?;
    """
    
    c.execute(SQL_statement, (userID, courseID))
    result = c.fetchall()
    c.close()
    conn.close()
    return result
    
#funkcija, kas atjauno stundas statusu.

def update_lesson_progress(user_id, lesson_id, status):
    conn = sqlite3.connect('database.sql')
    c = conn.cursor()
    c.execute('SELECT * FROM Progress WHERE User_ID = ? AND Lesson_ID = ?', (user_id, lesson_id))
    progress = c.fetchone()
    if progress:
        c.execute('UPDATE Progress SET Status = ? WHERE User_ID = ? AND Lesson_ID = ?', (status, user_id, lesson_id))
    else:
        c.execute('INSERT INTO Progress (User_ID, Lesson_ID, Status) VALUES (?, ?, ?)', (user_id, lesson_id, status))

    conn.commit()
    c.close()
    conn.close()

#funkcija, kas izvēlas kursu noteiktai stundai.

def get_course_by_lesson(lesson_id):
    conn = sqlite3.connect('database.sql')
    c = conn.cursor()
    c.execute('SELECT Course_ID FROM Lessons WHERE Lesson_ID = ?', (lesson_id,))
    course_id = c.fetchone()[0]
    conn.close()
    return course_id

#funkcija, kas izvēlas visu informāciju par lietotāja progresu, balstoties uz lietotāja un stundas id.

def getProgressByLessonAndUser(lesson_id, user_id):
    conn = sqlite3.connect('database.sql')
    c = conn.cursor()
    c.execute('SELECT * FROM Progress WHERE Lesson_ID = ? AND User_ID = ?', (lesson_id, user_id))
    progress = c.fetchone()
    conn.close()
    return progress

def countLessonsInCourse(course_id):
    conn = sqlite3.connect('database.sql')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Lessons WHERE Course_ID = ?", (course_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def countCompletedLessons(user_id, course_id):
    conn = sqlite3.connect('database.sql')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM Progress 
        WHERE User_ID = ? 
        AND Lesson_ID IN (SELECT Lesson_ID FROM Lessons WHERE Course_ID = ?)
        AND Status = 'pabeigts'
    """, (user_id, course_id))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def checkTableStructure():
    conn = sqlite3.connect('database.sql')
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(Courses)")
    columns = cursor.fetchall()
    conn.close()
    print("Course table columns:", columns)
    return columns

def add_xp_for_lesson(user_id, xp_amount=10):
    conn = sqlite3.connect('database.sql')
    c = conn.cursor()
    c.execute('UPDATE Users SET XP = XP + ? WHERE User_ID = ?', (xp_amount, user_id))
    conn.commit()
    conn.close()

def get_top_users(limit=10):
    conn = sqlite3.connect('database.sql', timeout=10)
    c = conn.cursor()
    SQL_statement = """
        SELECT Username, XP, ProfilePicture IS NOT NULL as has_picture, User_ID 
        FROM Users 
        ORDER BY XP DESC 
        LIMIT ?;
    """
    c.execute(SQL_statement, (limit,))
    result = c.fetchall()
    conn.close()
    return result

def updateUserWithPicture(userid, username, password, email, klase, subclass, date, desc, xp, picture_data):
    conn = sqlite3.connect('database.sql', timeout=10)
    c = conn.cursor()
    SQL_statement = """
        UPDATE Users 
        SET Username=?, Password=?, Email=?, Class=?, SubClass=?, 
            BirthDate=?, Description=?, XP=?, ProfilePicture=?
        WHERE User_ID=?;
    """
    c.execute(SQL_statement, (username, password, email, klase, subclass, 
                            date, desc, xp, picture_data, userid))
    conn.commit()
    c.close()
    conn.close()
    return True

def get_profile_picture(user_id):
    conn = sqlite3.connect('database.sql', timeout=10)
    c = conn.cursor()
    c.execute('SELECT ProfilePicture FROM Users WHERE User_ID = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result and result[0] else None
