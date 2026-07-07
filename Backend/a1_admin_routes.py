from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token

from model import User, Student, Company, PlacementDrive, Application
from db import db


admin_bp = Blueprint("admin", __name__)   # Create blueprint for admin routes















# ===================== DASHBOARD =====================

@admin_bp.route("/api/admin/dashboard", methods=["GET"])
def get_dashboard():

    student_count = Student.query.count() or 0

    company_count = Company.query.count() or 0

    drive_count = PlacementDrive.query.count() or 0

    application_count = Application.query.count() or 0


    return jsonify({
        "student_count": student_count,
        "company_count": company_count,
        "drive_count": drive_count,
        "application_count": application_count
    })

















# ===================== COMPANY MANAGEMENT =====================

@admin_bp.route("/api/admin/companies", methods=["GET"])
def get_companies():

    companies = Company.query.all()

    return jsonify([{
        "id": c.id,
        "company_name": c.company_name,
        "hr_name": c.hr_name,
        "hr_contact": c.hr_contact,
        "website": c.website,
        "approval_status": c.approval_status,
        "email": c.user.email
    } for c in companies])









@admin_bp.route("/api/admin/company/<int:id>/approve", methods=["PUT"])
def approve_company(id):

    company = Company.query.get_or_404(id)

    company.approval_status = "Approved"

    db.session.commit()

    return jsonify({
        "message": "Company approved successfully"
    })








@admin_bp.route("/api/admin/company/<int:id>/reject", methods=["PUT"])
def reject_company(id):

    company = Company.query.get_or_404(id)

    company.approval_status = "Rejected"

    db.session.commit()

    return jsonify({
        "message": "Company rejected"
    })








@admin_bp.route("/api/admin/company/<int:id>/blacklist", methods=["PUT"])
def blacklist_company(id):

    company = Company.query.get_or_404(id)

    company.user.is_blacklisted = True

    db.session.commit()

    return jsonify({
        "message": "Company blacklisted"
    })








@admin_bp.route("/api/admin/company/<int:id>", methods=["DELETE"])
def delete_company(id):

    company = Company.query.get_or_404(id)

    db.session.delete(company)

    db.session.commit()

    return jsonify({
        "message": "Company deleted successfully"
    })

















# ===================== STUDENT MANAGEMENT =====================

@admin_bp.route("/api/admin/students", methods=["GET"])
def get_students():

    students = Student.query.all()

    return jsonify([{
        "id": s.id,
        "name": s.user.name,
        "email": s.user.email,
        "branch": s.branch,
        "cgpa": s.cgpa,
        "passing_year": s.passing_year,
        "phone": s.phone
    } for s in students])









@admin_bp.route("/api/admin/student/<int:id>/blacklist", methods=["PUT"])
def blacklist_student(id):

    student = Student.query.get_or_404(id)

    student.user.is_blacklisted = True

    db.session.commit()

    return jsonify({
        "message": "Student blacklisted"
    })








@admin_bp.route("/api/admin/student/<int:id>", methods=["DELETE"])
def delete_student(id):

    student = Student.query.get_or_404(id)

    db.session.delete(student)

    db.session.commit()

    return jsonify({
        "message": "Student deleted successfully"
    })

















# ===================== PLACEMENT DRIVE MANAGEMENT =====================

@admin_bp.route("/api/admin/drives", methods=["GET"])
def get_drives():

    drives = PlacementDrive.query.all()

    return jsonify([{
        "id": d.id,
        "job_title": d.job_title,
        "company_name": d.company.company_name,
        "min_cgpa": d.min_cgpa,
        "deadline": d.application_deadline,
        "status": d.status
    } for d in drives])









@admin_bp.route("/api/admin/drive/<int:id>/approve", methods=["PUT"])
def approve_drive(id):

    drive = PlacementDrive.query.get_or_404(id)

    drive.status = "Approved"

    db.session.commit()

    return jsonify({
        "message": "Placement drive approved"
    })








@admin_bp.route("/api/admin/drive/<int:id>/reject", methods=["PUT"])
def reject_drive(id):

    drive = PlacementDrive.query.get_or_404(id)

    drive.status = "Rejected"

    db.session.commit()

    return jsonify({
        "message": "Placement drive rejected"
    })








@admin_bp.route("/api/admin/drive/<int:id>/close", methods=["PUT"])
def close_drive(id):

    drive = PlacementDrive.query.get_or_404(id)

    drive.status = "Closed"

    db.session.commit()

    return jsonify({
        "message": "Placement drive closed"
    })

















# ===================== APPLICATION MANAGEMENT =====================

@admin_bp.route("/api/admin/applications", methods=["GET"])
def get_all_applications():

    applications = Application.query.all()

    return jsonify([{
        "id": a.id,
        "student_name": a.student.user.name,
        "student_email": a.student.user.email,
        "company_name": a.drive.company.company_name,
        "job_title": a.drive.job_title,
        "status": a.status,
        "applied_at": a.applied_at
    } for a in applications])

















# ===================== SEARCH =====================

@admin_bp.route("/api/admin/search/students", methods=["GET"])
def search_students():

    query = request.args.get("query")

    students = Student.query.join(User).filter(
        User.name.ilike(f"%{query}%")
    ).all()

    return jsonify([{
        "id": s.id,
        "name": s.user.name,
        "email": s.user.email,
        "branch": s.branch
    } for s in students])









@admin_bp.route("/api/admin/search/companies", methods=["GET"])
def search_companies():

    query = request.args.get("query")

    companies = Company.query.filter(
        Company.company_name.ilike(f"%{query}%")
    ).all()

    return jsonify([{
        "id": c.id,
        "company_name": c.company_name,
        "website": c.website,
        "approval_status": c.approval_status
    } for c in companies])