from celery import Celery

celery_app = Celery("tasks", broker="redis://localhost:6379/0")

@celery_app.task
def send_task_reminder(task_id, user_email):
    print(f"Reminder: Task {task_id} is due soon! Sending email to {user_email}")
