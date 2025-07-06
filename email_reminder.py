import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import json

USERS_FILE = "users.json"

# Send email
def send_email_reminder(user_email, task_msg):
    sender = "yourgmail@gmail.com"
    password = "your-app-password"  # Use Gmail App Password if 2FA is enabled

    msg = MIMEText(task_msg)
    msg['Subject'] = 'To-Do Reminder: Task Due Tomorrow!'
    msg['From'] = sender
    msg['To'] = user_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        print(f"Reminder sent to {user_email}")
    except Exception as e:
        print(f"Failed to send email to {user_email}: {e}")

# Check for upcoming tasks
def check_upcoming_tasks(current_user):
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    try:
        with open(USERS_FILE) as f:
            users = json.load(f)
            if current_user in users:
                user_data = users[current_user]
                email = user_data.get("email")
                for task in user_data.get("tasks", []):
                    if not task.get("completed") and task.get("due_date") == tomorrow:
                        send_email_reminder(email, f"Reminder: '{task['task']}' is due tomorrow!")
    except Exception as e:
        print(f"Error checking tasks: {e}")
