from flask import Blueprint, request, jsonify
from model import Company, PlacementDrive, Application, Student
from db import db
import datetime


company_bp = Blueprint("company", __name__)




@company_bp.route("/api/company/check/<int:user_id>", methods=["GET"])
def check_company(user_id):
    company = Company.query.filter_by(user_id=user_id).first()
    if company:
        return jsonify({
            "exists": True,
            "company_id": company.id
        }), 200
    else:
        return jsonify({"exists": False}), 200


@company_bp.route("/api/company_profile/<int:id>", methods=["POST"])
def register(id):

    data = request.get_json() # request.get_json() is used to parse the incoming JSON data from the request body.
    # Returns a Python dictionary (or None if the request body isn’t valid JSON).


    company_name= data.get("name")
    hr_name = data.get("hr_name")
    website = data.get("web")
   
    description = data.get("description")
    hr_contact = data.get("contact")
    
    user_id = id




    new_company = Company(

        company_name= company_name,
        hr_name = hr_name,
        website = website,
    
        description = description,
        hr_contact = hr_contact,
    
        user_id = user_id

    )

    db.session.add(new_company)
    db.session.commit()

    return jsonify({"message": "company registered successfully",
                    "company_id": new_company.id  # ← add this
                    }), 201












# ===================== COMPANY DASHBOARD =====================

@company_bp.route("/api/company/dashboard/<int:company_id>", methods=["GET"])
def company_dashboard(company_id):

    company = Company.query.get_or_404(company_id)

    drive_count = PlacementDrive.query.filter_by(
        company_id=company_id
    ).count()

    application_count = 0

    drives = PlacementDrive.query.filter_by(
        company_id=company_id
    ).all()

    for drive in drives:
        application_count += Application.query.filter_by(
            drive_id=drive.id
        ).count()


    return jsonify({
        "company_name": company.company_name,
        "approval_status": company.approval_status,
        "drive_count": drive_count,
        "application_count": application_count
    })

















# ===================== CREATE PLACEMENT DRIVE =====================

@company_bp.route("/api/company/drives", methods=["POST"])
def create_drive():

    data = request.get_json()

    company = Company.query.get(data["company_id"])


    if company.approval_status != "Approved":
        return jsonify({
            "message": "Company not approved by admin"
        }), 403


    drive = PlacementDrive(
        job_title=data["job_title"],
        job_description=data["job_description"],
        eligibility_branch=data["eligibility_branch"],
        min_cgpa=data["min_cgpa"],
        passing_year=data["passing_year"],
        package=data["package"],
        location=data["location"],
        application_deadline=datetime.datetime.strptime(
            data["application_deadline"],
            "%Y-%m-%d"
        ),
        drive_date=datetime.datetime.strptime(
            data["drive_date"],
            "%Y-%m-%d"
        ),
        company_id=data["company_id"]
    )

    db.session.add(drive)
    db.session.commit()

    return jsonify({
        "message": "Placement drive created successfully"
    })

















# ===================== GET COMPANY DRIVES =====================

@company_bp.route("/api/company/drives/<int:company_id>", methods=["GET"])
def get_company_drives(company_id):

    drives = PlacementDrive.query.filter_by(
        company_id=company_id
    ).all()

    return jsonify([{
        "id": d.id,
        "job_title": d.job_title,
        "status": d.status,
        "deadline": d.application_deadline,
        "drive_date": d.drive_date
    } for d in drives])

















# ===================== UPDATE DRIVE =====================

@company_bp.route("/api/company/drive/<int:id>", methods=["PUT"])
def update_drive(id):

    drive = PlacementDrive.query.get_or_404(id)

    data = request.get_json()

    drive.job_title = data["job_title"]
    drive.job_description = data["job_description"]
    drive.min_cgpa = data["min_cgpa"]
    drive.package = data["package"]
    drive.location = data["location"]

    db.session.commit()

    return jsonify({
        "message": "Drive updated successfully"
    })


















# ===================== DELETE DRIVE =====================

@company_bp.route("/api/company/drive/<int:id>", methods=["DELETE"])
def delete_drive(id):

    drive = PlacementDrive.query.get_or_404(id)

    db.session.delete(drive)

    db.session.commit()

    return jsonify({
        "message": "Drive deleted successfully"
    })

















# ===================== VIEW APPLICATIONS =====================

@company_bp.route("/api/company/applications/<int:drive_id>", methods=["GET"])
def get_drive_applications(drive_id):

    applications = Application.query.filter_by(
        drive_id=drive_id
    ).all()

    return jsonify([{
        "application_id": a.id,
        "student_name": a.student.user.name,
        "student_email": a.student.user.email,
        "branch": a.student.branch,
        "cgpa": a.student.cgpa,
        "status": a.status
    } for a in applications])

















# ===================== UPDATE APPLICATION STATUS =====================

@company_bp.route("/api/company/application/<int:id>/status", methods=["PUT"])
def update_application_status(id):

    application = Application.query.get_or_404(id)

    data = request.get_json()

    application.status = data["status"]

    application.remarks = data.get("remarks")

    db.session.commit()

    return jsonify({
        "message": "Application status updated"
    })

















# ===================== SCHEDULE INTERVIEW =====================

@company_bp.route("/api/company/application/<int:id>/interview", methods=["PUT"])
def schedule_interview(id):

    application = Application.query.get_or_404(id)

    data = request.get_json()

    application.interview_date = datetime.datetime.strptime(
        data["interview_date"],
        "%Y-%m-%d %H:%M:%S"
    )

    application.status = "Interview Scheduled"

    db.session.commit()

    return jsonify({
        "message": "Interview scheduled successfully"
    })