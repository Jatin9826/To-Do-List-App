<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/d71b3e2f-e61d-4257-b65b-4f23fadc724c" />

# 📝 Advanced To-Do List App with Email Reminders

This is a feature-rich **To-Do List Desktop Application** built using **Python and Tkinter**, designed to help users manage tasks efficiently with a beautiful GUI. The app supports user login, task management, reminders via desktop notifications and **email alerts**, theme switching, Excel export, and more.

## 🔧 Features

- ✅ **Multi-User Login System** with email registration
- ⏰ **Automatic Email Reminders** for tasks due the next day
- 📅 **Date Picker** for task due dates
- 🔔 **System Notification** for today's tasks
- 📂 **Category and Priority** tagging
- 🗃️ **Search and Sort** functionality
- 📤 **Export tasks to Excel**
- 🌗 **Light/Dark Mode** toggle
- 📝 **Add, Edit, Delete, Complete tasks**
- 📬 Email notifications sent using **Gmail SMTP**
- 🔐 User tasks stored securely in JSON files

---

## 🚀 Getting Started

### 🔨 Prerequisites
📦advanced-todo-app
 ┣ 📄 enhanced_todo_app.py         # Main GUI Application
 ┣ 📄 email_reminder.py            # Sends reminder emails for tasks due tomorrow
 ┣ 📄 enhanced_todo_tasks.json     # Stores tasks for all users
 ┣ 📄 users.json                   # Stores user login and email data
 ┣ 📄 todo_export.xlsx             # Excel export file (generated at runtime)
 ┗ 📄 README.md                    # You're here!


- Python 3.8 or above
- Required libraries:

```bash
pip install tkcalendar plyer pandas openpyxl
