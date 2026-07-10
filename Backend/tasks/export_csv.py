from celery import shared_task
from flask_mail import Message
from model import Application, Student, User
from extensions import mail
import csv, io

@shared_task(name="tasks.export_csv.export_applications", bind=True)
def export_applications(self, student_id):
    student = Student.query.get(student_id)
    user = User.query.get(student.user_id)

    applications = Application.query.filter_by(student_id=student_id).all()

    # Build CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Student ID", "Company Name", "Drive Title", "Status", "Applied At", "Interview Date"])

    for app in applications:
        writer.writerow([
            student_id,
            app.drive.company.company_name,
            app.drive.job_title,
            app.status,
            app.applied_at.strftime("%d %b %Y") if app.applied_at else "N/A",
            app.interview_date.strftime("%d %b %Y") if app.interview_date else "Not Scheduled"
        ])

    csv_content = output.getvalue().encode("utf-8")

    msg = Message(
        subject="📁 Your Application History Export",
        recipients=[user.email],
        body=f"Hi {user.name}, please find your application history attached.",
    )
    msg.attach("applications.csv", "text/csv", csv_content)
    mail.send(msg)

    return {"status": "done", "email": user.email}