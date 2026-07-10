from celery import shared_task
from flask_mail import Message
from datetime import datetime, timedelta
from model import Student, PlacementDrive, User
from db import db
from extensions import mail

@shared_task(name="tasks.reminders.send_deadline_reminders")
def send_deadline_reminders():
    today = datetime.utcnow().date()
    upcoming = today + timedelta(days=3)

    drives = PlacementDrive.query.filter(
        PlacementDrive.application_deadline >= today,    # ← fixed
        PlacementDrive.application_deadline <= upcoming, # ← fixed
        PlacementDrive.status == "Approved"
    ).all()

    if not drives:
        return "No upcoming deadlines"

    students = Student.query.all()

    for student in students:
        user = User.query.get(student.user_id)
        if not user or not user.email:
            continue

        drive_rows = ""
        for drive in drives:
            days_left = (drive.application_deadline - today).days  # ← fixed
            drive_rows += f"""
                <tr>
                  <td>{drive.job_title}</td>
                  <td>{drive.company.company_name}</td>
                  <td>{drive.application_deadline.strftime('%d %b %Y')}</td>
                  <td><b>{days_left} day(s) left</b></td>
                </tr>
            """

        html_body = f"""
        <h2>📢 Upcoming Placement Deadlines</h2>
        <p>Hi {user.name}, don't miss these upcoming drives:</p>
        <table border="1" cellpadding="8" style="border-collapse:collapse;">
          <tr><th>Job Title</th><th>Company</th><th>Deadline</th><th>Time Left</th></tr>
          {drive_rows}
        </table>
        <p>Login to apply now!</p>
        """

        msg = Message(
            subject="⏰ Placement Deadline Reminder",
            recipients=[user.email],
            html=html_body
        )
        mail.send(msg)

    return f"Reminders sent to {len(students)} students"