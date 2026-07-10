from celery import Celery
from celery.schedules import crontab

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker="redis://localhost:6379/0",
        backend="redis://localhost:6379/0",
        include=[
            "tasks.reminders",
            "tasks.monthly_rem",
            "tasks.export_csv"
        ]
    )

    celery.conf.update(
        broker_url="redis://localhost:6379/0",        # ← add this
        result_backend="redis://localhost:6379/0",    # ← add this
        broker_transport="redis",                     # ← add this
        timezone="Asia/Kolkata",
        beat_schedule={
            "daily-deadline-reminders": {
                "task": "tasks.reminders.send_deadline_reminders",
                "schedule": crontab(hour=9, minute=0),
            },
            "monthly-activity-report": {
                "task": "tasks.monthly_rem.send_monthly_report",
                "schedule": crontab(day_of_month=1, hour=8, minute=0),
            },
        }
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery