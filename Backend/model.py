from db import db
from sqlalchemy.orm import relationship
import datetime


# -------------------- USER --------------------
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
   

    is_active = db.Column(db.Boolean, default=True)
    is_blacklisted = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    # RELATIONSHIPS
    student = relationship("Student", back_populates="user", uselist=False)
    company = relationship("Company", back_populates="user", uselist=False)












# -------------------- STUDENT --------------------
class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    branch = db.Column(db.String(100), nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    passing_year = db.Column(db.Integer, nullable=False)

    skills = db.Column(db.Text)
    resume = db.Column(db.String(300))
    phone = db.Column(db.String(20))


  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)


    
    user = relationship("User", back_populates="student")
    applications = relationship("Application", back_populates="student", lazy='dynamic')













# -------------------- COMPANY --------------------
class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)

    company_name = db.Column(db.String(200), nullable=False)

    hr_name = db.Column(db.String(100))

    hr_contact = db.Column(db.String(20))

    website = db.Column(db.String(200))

    description = db.Column(db.Text)

    approval_status = db.Column(db.String(20), default='Pending')
    


    # FOREIGN KEY
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        unique=True, nullable=False)


   
    user = relationship("User", back_populates="company")
    placement_drives = relationship("PlacementDrive", back_populates="company", lazy='dynamic')














# -------------------- PLACEMENT DRIVE --------------------
class PlacementDrive(db.Model):
    __tablename__ = 'placement_drive'

    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(200), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    eligibility_branch = db.Column(db.String(200))
    min_cgpa = db.Column(db.Float)
    passing_year = db.Column(db.Integer)

    package = db.Column(db.String(100))

    location = db.Column(db.String(100))
    application_deadline = db.Column(db.Date, nullable=False)
    drive_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='Pending')
    


    created_at = db.Column(db.DateTime,default=datetime.datetime.utcnow)


    # FOREIGN KEY
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)


    # RELATIONSHIPS
    company = relationship("Company", back_populates="placement_drives")
    applications = relationship("Application", back_populates="drive",lazy='dynamic')














# -------------------- APPLICATION --------------------
class Application(db.Model):
    __tablename__ = 'application'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), default='Applied')

    applied_at = db.Column(db.DateTime,default=datetime.datetime.utcnow)
    interview_date = db.Column(db.DateTime)
    remarks = db.Column(db.Text)


    
    student_id = db.Column(db.Integer,db.ForeignKey('student.id'),nullable=False)

    drive_id = db.Column(db.Integer,db.ForeignKey('placement_drive.id'),nullable=False)



    student = relationship("Student", back_populates="applications")

    drive = relationship("PlacementDrive",
                         back_populates="applications")