from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# -----------------------------------------------------------------

class Authentication(db.Model):
    __bind_key__ = "login"
    __tablename__ = "authenticate"
    login_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25))
    last_name = db.Column(db.String(25))
    username = db.Column(db.String(25))
    password = db.Column(db.String(25))

class SelectedCohort(db.Model):
    __bind_key__ = "login"
    __tablename__ = "cohort_selected"
    record_id = db.Column(db.Integer, primary_key=True)
    cohort_id = db.Column(db.Integer)



# ----------------------------------------------------------------- 
class Cohort(db.Model):
    __bind_key__ = "gradebook"
    __tablename__ = "cohort"
    cohort_id = db.Column(db.Integer, primary_key=True)
    cohort_name = db.Column(db.String(25))
    location = db.Column(db.String(50))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    #current_unit or units_complete                      # is this needed???

    
class Person(db.Model):
    __bind_key__ = "gradebook"
    __tablename__ = "person"
    person_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    role = db.Column(db.String(50))                     # TA, SSM, Instructor, Student

    
class Email(db.Model):
    __bind_key__ = "gradebook"
    __tablename__ = "email"
    email_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("person.person_id"))
    email = db.Column(db.String(50))
    date_added = db.Column(db.Date)

    
class Github(db.Model):              #merge github with person?
    __bind_key__ = "gradebook"
    __tablename__ = "github"
    # github_id = Column(Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'), primary_key=True)           # foreign key
    github_username = db.Column(db.String(50))

    
class Student(db.Model):
    __bind_key__ = "gradebook"
    __tablename__ = "student"
    student_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'), primary_key=True)
    cohort_id = db.Column(db.Integer, db.ForeignKey('cohort.cohort_id'), primary_key=True)


# -----------------------------------------------------------------

class Unit(db.Model):
    __bind_key__ = "gradebook"
    __tablename__ = "unit"
    unit_id = db.Column(db.Integer, primary_key=True)
    cohort_id = db.Column(db.Integer, db.ForeignKey('cohort.cohort_id'), primary_key=True)
    unit_number = db.Column(db.Integer)
    unit_name = db.Column(db.String(50))
    unit_start = db.Column(db.Date)
    unit_due = db.Column(db.Date)
    hw_submissions = db.Column(db.Integer)
    students_enrolled = db.Column(db.Integer)
    unit_required = db.Column(db.Boolean)
    context_code = db.Column(db.String)
    career_assignment_bool = db.Column(db.Boolean)
    graded_assignments = db.Column(db.String)


    
# from session_details api  
# do I connect this to the unit_id
class Session(db.Model):
    __bind_key__ = "gradebook"
    __tablename__ = 'session'
    session_id = db.Column(db.Integer, primary_key=True)
    cohort_id = db.Column(db.Integer, db.ForeignKey('cohort.cohort_id'), primary_key=True) 
    session_name = db.Column(db.String(25))
    unit_id = db.Column(db.Integer)     
    session_number = db.Column(db.Integer)
    session_chapter = db.Column(db.String(10))
    session_start = db.Column(db.Date)
    zoom_url = db.Column(db.String(50))
    

# ------------------------------------------------------------------------

# how to set this up so I can have a list of updated questions    
class Survey(db.Model):
    __bind_key__ = "gradebook"
    __tablename__ = "survey"
    question_id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(200))
    date_added = db.Column(db.Date)

    
class SurveySet(db.Model):
    __bind_key__ = "gradebook"
    __tablename__ = "surveyset"
    feedback_id = db.Column(db.Integer, primary_key=True)             # foreign key
    question_id = db.Column(db.Integer, db.ForeignKey('survey.question_id'), primary_key=True)             # foreign key
    question_number = db.Column(db.Integer)
    

class Week(db.Model):
    __bind_key__ = "gradebook"
    __tablename__="week"
    week_id = db.Column(db.Integer, primary_key=True)
    cohort_id = db.Column(db.Integer, db.ForeignKey('cohort.cohort_id'), primary_key=True)
    week_end_date = db.Column(db.Date)
    current_unit = db.Column(db.Integer, db.ForeignKey('unit.unit_id'))
    previous_session = db.Column(db.Integer, db.ForeignKey('session.session_id'))


# Maybe add student_name to this table  
# why is this by email address and not student name or ID
class Feedback(db.Model):
    __bind_key__ = "gradebook"
    __tablename__ = 'feedback'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    feedback_id = db.Column(db.Integer, db.ForeignKey('surveyset.feedback_id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), primary_key=True)             # foreign key     
    week = db.Column(db.Integer, db.ForeignKey('week.week_id'), primary_key=True)                   # is this the same as unit?
    submission_date = db.Column(db.Date)
    overall_satisfaction = db.Column(db.Integer)
    pace = db.Column(db.Integer)
    academic_support = db.Column(db.Integer)
    outside_class_productivity = db.Column(db.Integer)
    instructor_engagement = db.Column(db.Integer)
    instructor_clarity = db.Column(db.Integer)
    instructor_knowledge = db.Column(db.Integer)
    homework_feedback = db.Column(db.Integer)
    outside_class_time_spent = db.Column(db.Integer)
    class_comments = db.Column(db.String(250))
    instructional_support_comments = db.Column(db.String(250))
    

    
# from attendance api, no sessions, one table
# maybe make compound key from session and name
class Attendance(db.Model):
    __bind_key__ = "gradebook"
    __tablename__ = "attendance"
    session_id = db.Column(db.Integer, db.ForeignKey('session.session_id'), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), primary_key=True)
    present = db.Column(db.Boolean)
    pending = db.Column(db.Boolean)

    
# from grade api
# no sessions, one table
# unit_name could come from unit table and this be a foreign key
class Grade(db.Model):
    __bind_key__ = "gradebook"
    __tablename__ = 'grade'
#    grade_id = Column(Integer, primary_key=True)                           # probably not needed
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.unit_id'), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), primary_key=True)
    hw_submitted = db.Column(db.Boolean)
    hw_grade = db.Column(db.String(10))
    

# from session details api
# why is this by student ID an not name????
class Arrival(db.Model):
    __bind_key__ = "gradebook"
    __tablename__ = "arrival"
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.session_id'), primary_key=True)
    arrival_time = db.Column(db.Integer)

    
class Submissions(db.Model):
    __bind_key__ = "gradebook"
    __tablename__ = "submission"
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.unit_id'), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    # email = Column(String)
    submission_status = db.Column(db.Boolean)
    submission_date = db.Column(db.Date)
    submission_notes = db.Column(db.String)
    grade = db.Column(db.String)
    feedback = db.Column(db.String)
    plagiarism = db.Column(db.Boolean)


class AttendanceStatus(db.Model):
    __bind_key__ = "gradebook"
    __tablename__ = 'attendance_status'
    bin = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String)