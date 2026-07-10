from celery import shared_task
from flask_mail import Message
from datetime import datetime
from model import PlacementDrive, Application, Student, User
from db import db
from extensions import mail
import calendar

@shared_task(name="tasks.monthly_report.send_monthly_report")
def send_monthly_report():
    now = datetime.utcnow()
    last_month = now.month - 1 if now.month > 1 else 12
    year = now.year if now.month > 1 else now.year - 1
    month_name = calendar.month_name[last_month]

    drives = PlacementDrive.query.filter(
        db.extract("month", PlacementDrive.created_at) == last_month,
        db.extract("year", PlacementDrive.created_at) == year
    ).all()

    applications = Application.query.filter(
        db.extract("month", Application.applied_at) == last_month,
        db.extract("year", Application.applied_at) == year
    ).all()

    selected = [a for a in applications if a.status == "Selected"]

    drive_rows = "".join([
        f"<tr><td>{d.job_title}</td><td>{d.company.company_name}</td><td>{d.status}</td></tr>"  # ← fixed
        for d in drives
    ])

    html_body = f"""
    <html><body style="font-family:Arial,sans-serif;">
      <h2>📊 Monthly Placement Report — {month_name} {year}</h2>
      <table border="1" cellpadding="8" style="border-collapse:collapse;margin-bottom:20px;">
        <tr><td><b>Total Drives Conducted</b></td><td>{len(drives)}</td></tr>
        <tr><td><b>Total Applications</b></td><td>{len(applications)}</td></tr>
        <tr><td><b>Students Selected</b></td><td>{len(selected)}</td></tr>
      </table>

      <h3>Drive Details</h3>
      <table border="1" cellpadding="8" style="border-collapse:collapse;">
        <tr style="background:#f0f0f0;">
          <th>Job Title</th><th>Company</th><th>Status</th>
        </tr>
        {drive_rows}
      </table>

      <p style="color:#888;font-size:12px;">
        Auto-generated on {now.strftime('%d %b %Y')}
      </p>
    </body></html>
    """

    admin = User.query.filter_by(role="admin").first()
    if not admin:
        return "No admin found"

    msg = Message(
        subject=f"📊 Monthly Placement Report — {month_name} {year}",
        recipients=[admin.email],
        html=html_body
    )
    mail.send(msg)

    return f"Monthly report sent to {admin.email}"