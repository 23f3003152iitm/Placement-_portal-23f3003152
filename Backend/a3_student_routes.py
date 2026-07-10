from flask import Blueprint, request, jsonify
from model import Student, PlacementDrive, Application
from tasks.export_csv import export_applications
from db import db
import datetime
from tasks.export_csv import export_applications

student_bp = Blueprint("student", __name__)


@student_bp.route("/api/student/check/<int:user_id>", methods=["GET"])
def check_student(user_id):
    student = Student.query.filter_by(user_id=user_id).first()
    if student:
        return jsonify({
            "exists": True,
            "student_id": student.id
        }), 200
    else:
        return jsonify({"exists": False}), 200
    


@student_bp.route("/api/student_profile/<int:id>", methods=["POST"])
def register(id):

    data = request.get_json() # request.get_json() is used to parse the incoming JSON data from the request body.
    # Returns a Python dictionary (or None if the request body isn’t valid JSON).


    branch= data.get("branch")
    cgpa = data.get("cgpa")
    resume = data.get("resume")
   
    skills = data.get("skills")
    phone = data.get("phone")
    passing_year = data.get("passing_year")
    user_id = id




    new_student = Student(
        branch = branch,
        cgpa = cgpa,
        resume = resume,
        skills = skills,
        phone = phone,
        passing_year = passing_year,
        user_id = user_id

    )

    db.session.add(new_student)
    db.session.commit()

    return jsonify({"message": "User registered successfully",
                    "student_id": new_student.id  # ← add this
                    }), 201






@student_bp.route("/api/student/export/<int:student_id>", methods=["POST"])
def export_csv(student_id):
    from app import celery
    from tasks.export_csv import export_applications
    task = celery.send_task(
        "tasks.export_csv.export_applications",
        args=[student_id]
    )
    return jsonify({
        "message": "Export started! You'll receive an email shortly.",
        "task_id": task.id
    }), 202





# ===================== STUDENT DASHBOARD =====================

@student_bp.route("/api/student/dashboard/<int:student_id>", methods=["GET"])
def student_dashboard(student_id):

    student = Student.query.get_or_404(student_id)

    applied_count = Application.query.filter_by(
        student_id=student_id
    ).count()

    approved_drives = PlacementDrive.query.filter_by(
        status="Approved"
    ).count()

    return jsonify({
        "student_name": student.user.name,
        "branch": student.branch,
        "cgpa": student.cgpa,
        "applied_count": applied_count,
        "approved_drives": approved_drives
    })

















# ===================== GET APPROVED DRIVES =====================

@student_bp.route("/api/student/drives", methods=["GET"])
def get_approved_drives():

    drives = PlacementDrive.query.filter_by(
        status="Approved"
    ).all()

    return jsonify([{
        "id": d.id,
        "job_title": d.job_title,
        "company_name": d.company.company_name,
        "package": d.package,
        "location": d.location,
        "min_cgpa": d.min_cgpa,
        "deadline": d.application_deadline
    } for d in drives])

















# ===================== APPLY FOR DRIVE =====================

@student_bp.route("/api/student/apply", methods=["POST"])
def apply_drive():

    data = request.get_json()

    student = Student.query.get(data["student_id"])

    drive = PlacementDrive.query.get(data["drive_id"])


    if not drive:
        return jsonify({
            "message": "Drive not found"
        }), 404


    # CHECK ELIGIBILITY
    if student.cgpa < drive.min_cgpa:
        return jsonify({
            "message": "Not eligible due to CGPA"
        }), 400


    already_applied = Application.query.filter_by(
        student_id=student.id,
        drive_id=drive.id
    ).first()


    if already_applied:
        return jsonify({
            "message": "Already applied"
        }), 400


    application = Application(
        student_id=student.id,
        drive_id=drive.id
    )

    db.session.add(application)
    db.session.commit()

    return jsonify({
        "message": "Applied successfully"
    })

















# ===================== VIEW APPLICATION STATUS =====================

@student_bp.route("/api/student/applications/<int:student_id>", methods=["GET"])
def get_student_applications(student_id):

    applications = Application.query.filter_by(
        student_id=student_id
    ).all()

    return jsonify([{
        "application_id": a.id,
        "job_title": a.drive.job_title,
        "company_name": a.drive.company.company_name,
        "status": a.status,
        "interview_date": a.interview_date
    } for a in applications])

















# ===================== PLACEMENT HISTORY =====================

@student_bp.route("/api/student/history/<int:student_id>", methods=["GET"])
def placement_history(student_id):

    applications = Application.query.filter_by(
        student_id=student_id,
        status="Selected"
    ).all()

    return jsonify([{
        "company_name": a.drive.company.company_name,
        "job_title": a.drive.job_title,
        "package": a.drive.package,
        "selected_date": a.applied_at
    } for a in applications])

















# ===================== UPDATE PROFILE =====================

@student_bp.route("/api/student/profile/<int:id>", methods=["PUT"])
def update_profile(id):

    student = Student.query.get_or_404(id)

    data = request.get_json()

    student.branch = data["branch"]
    student.cgpa = data["cgpa"]
    student.passing_year = data["passing_year"]
    student.skills = data["skills"]
    student.phone = data["phone"]

    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully"
    })