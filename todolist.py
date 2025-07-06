# Enhanced To-Do List App with 11 Features (including Email Reminder)
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import DateEntry
import json, os
from datetime import datetime, timedelta
from plyer import notification
import pandas as pd
from email_reminder import check_upcoming_tasks

FILENAME = "enhanced_todo_tasks.json"
USERS_FILE = "users.json"
THEMES = {"Light": {"bg": "#ffffff", "fg": "#000000"}, "Dark": {"bg": "#2c2c2c", "fg": "#ffffff"}}

# Load/save JSON data
def load_data(filename):
    if os.path.exists(filename):
        with open(filename) as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    return {}

def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Authentication
current_user = None
user_email = ""

def login():
    global current_user, user_email
    users = load_data(USERS_FILE)
    username = simpledialog.askstring("Login", "Enter username")
    if username:
        if username not in users:
            email = simpledialog.askstring("Email", "Enter your email for reminders")
            users[username] = {"email": email, "tasks": []}
        current_user = username
        user_email = users[username]["email"]
        save_data(USERS_FILE, users)
        return users[username]["tasks"]
    return []

def save_user_tasks(tasks):
    users = load_data(USERS_FILE)
    if current_user:
        users[current_user]["tasks"] = tasks
        save_data(USERS_FILE, users)

# GUI Setup
app = tk.Tk()
app.title("Advanced To-Do List App")
app.geometry("700x600")

style = ttk.Style()
style.theme_use('clam')

# Initial theme
theme_mode = "Light"
def apply_theme():
    theme = THEMES[theme_mode]
    app.configure(bg=theme["bg"])
    for widget in app.winfo_children():
        try:
            widget.configure(bg=theme["bg"], fg=theme["fg"])
        except:
            pass

def toggle_theme():
    global theme_mode
    theme_mode = "Dark" if theme_mode == "Light" else "Light"
    apply_theme()

# Widgets
tk.Label(app, text="Task").pack()
task_entry = tk.Entry(app, width=50)
task_entry.pack()

priority_var = tk.StringVar(value="Medium")
ttk.Combobox(app, textvariable=priority_var, values=["Low", "Medium", "High"]).pack()

due_date = DateEntry(app, width=12, background='darkblue', foreground='white', borderwidth=2)
due_date.pack()

category_entry = tk.Entry(app, width=30)
category_entry.insert(0, "General")
category_entry.pack()

task_listbox = tk.Listbox(app, width=80, height=15)
task_listbox.pack(pady=10)

search_entry = tk.Entry(app, width=40)
search_entry.pack()

# Core functions
tasks = login()

# Call email reminder check on login
check_upcoming_tasks(current_user)

def refresh_list():
    task_listbox.delete(0, tk.END)
    for t in tasks:
        line = f"[{t['priority']}] {t['task']} - {t['category']} - Due: {t['due_date']} - {'Done' if t['completed'] else 'Pending'}"
        task_listbox.insert(tk.END, line)

def add_task():
    task = task_entry.get().strip()
    if task:
        tasks.append({"task": task, "completed": False, "priority": priority_var.get(), "due_date": due_date.get(), "category": category_entry.get()})
        save_user_tasks(tasks)
        refresh_list()
        task_entry.delete(0, tk.END)

def toggle_task():
    sel = task_listbox.curselection()
    if sel:
        i = sel[0]
        tasks[i]["completed"] = not tasks[i]["completed"]
        save_user_tasks(tasks)
        refresh_list()

def delete_task():
    sel = task_listbox.curselection()
    if sel:
        tasks.pop(sel[0])
        save_user_tasks(tasks)
        refresh_list()

def edit_task():
    sel = task_listbox.curselection()
    if sel:
        i = sel[0]
        new_task = simpledialog.askstring("Edit Task", "New Task Description", initialvalue=tasks[i]['task'])
        if new_task:
            tasks[i]['task'] = new_task
            save_user_tasks(tasks)
            refresh_list()

def search_tasks():
    keyword = search_entry.get().lower()
    task_listbox.delete(0, tk.END)
    for t in tasks:
        if keyword in t['task'].lower():
            line = f"[{t['priority']}] {t['task']} - {t['category']} - Due: {t['due_date']} - {'Done' if t['completed'] else 'Pending'}"
            task_listbox.insert(tk.END, line)

def sort_tasks():
    tasks.sort(key=lambda x: (x['due_date'], x['priority']))
    refresh_list()

def notify_reminders():
    for t in tasks:
        if not t['completed'] and t['due_date'] == datetime.now().strftime('%Y-%m-%d'):
            notification.notify(title="Task Reminder", message=f"{t['task']} is due today!", timeout=5)

def export_to_excel():
    df = pd.DataFrame(tasks)
    df.to_excel("todo_export.xlsx", index=False)
    messagebox.showinfo("Exported", "Tasks exported to todo_export.xlsx")

# Buttons
tk.Button(app, text="Add Task", command=add_task).pack()
tk.Button(app, text="Toggle Complete", command=toggle_task).pack()
tk.Button(app, text="Edit Task", command=edit_task).pack()
tk.Button(app, text="Delete Task", command=delete_task).pack()
tk.Button(app, text="Search", command=search_tasks).pack()
tk.Button(app, text="Sort by Due Date & Priority", command=sort_tasks).pack()
tk.Button(app, text="Remind Today", command=notify_reminders).pack()
tk.Button(app, text="Export to Excel", command=export_to_excel).pack()
tk.Button(app, text="Toggle Theme", command=toggle_theme).pack()

refresh_list()
apply_theme()
app.mainloop()