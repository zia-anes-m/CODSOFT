import json
import os
import tkinter as tk
from tkinter import messagebox

FILE_NAME = "tasks.json"


# ---------- FILE ----------
def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return []


def save_tasks():
    with open(FILE_NAME, "w") as f:
        json.dump(tasks, f, indent=4)


# ---------- DISPLAY ----------
def display(filtered_tasks=None):
    listbox.delete(0, tk.END)

    data = filtered_tasks if filtered_tasks is not None else tasks

    for i, task in enumerate(data):
        status = "✔ completed" if task["done"] else "pending"
        text = f"{i+1}. {task['title']} [{task['priority']}] - {status}"

        listbox.insert(tk.END, text)

        # color
        if task["done"]:
            listbox.itemconfig(i, fg="green")
        elif task["priority"] == "High":
            listbox.itemconfig(i, fg="red")
        elif task["priority"] == "Medium":
            listbox.itemconfig(i, fg="orange")
        else:
            listbox.itemconfig(i, fg="blue")


def refresh_list():
    display()


# ---------- CORE ----------
def add_task():
    title = entry.get().strip()
    priority = priority_var.get()

    if not title:
        messagebox.showwarning("Warning", "Task cannot be empty")
        return

    tasks.append({"title": title, "done": False, "priority": priority})
    save_tasks()
    refresh_list()
    entry.delete(0, tk.END)


def get_selected_index():
    selected = listbox.curselection()
    if not selected:
        return None
    return selected[0]


def mark_done():
    i = get_selected_index()
    if i is None:
        messagebox.showwarning("Warning", "Select a task")
        return

    tasks[i]["done"] = True
    save_tasks()
    refresh_list()


def delete_task():
    i = get_selected_index()
    if i is None:
        messagebox.showwarning("Warning", "Select a task")
        return

    removed = tasks.pop(i)
    save_tasks()
    refresh_list()
    messagebox.showinfo("Deleted", removed["title"])


def edit_task():
    i = get_selected_index()
    if i is None:
        messagebox.showwarning("Warning", "Select a task")
        return

    new = entry.get().strip()
    if not new:
        messagebox.showwarning("Warning", "Enter new text")
        return

    tasks[i]["title"] = new
    save_tasks()
    refresh_list()
    entry.delete(0, tk.END)


def change_priority():
    i = get_selected_index()
    if i is None:
        messagebox.showwarning("Warning", "Select a task")
        return

    tasks[i]["priority"] = priority_var.get()
    save_tasks()
    refresh_list()


def move_up():
    i = get_selected_index()
    if i is None or i == 0:
        return

    tasks[i], tasks[i - 1] = tasks[i - 1], tasks[i]
    save_tasks()
    refresh_list()
    listbox.select_set(i - 1)


def move_down():
    i = get_selected_index()
    if i is None or i == len(tasks) - 1:
        return

    tasks[i], tasks[i + 1] = tasks[i + 1], tasks[i]
    save_tasks()
    refresh_list()
    listbox.select_set(i + 1)


def clear_all():
    if not tasks:
        return

    if messagebox.askyesno("Confirm", "Delete all tasks?"):
        tasks.clear()
        save_tasks()
        refresh_list()


# ---------- FILTER ----------
def filter_tasks(mode):
    if mode == "all":
        display()
    elif mode == "pending":
        display([t for t in tasks if not t["done"]])
    elif mode == "completed":
        display([t for t in tasks if t["done"]])


# ---------- SEARCH ----------
def search_task():
    key = entry.get().lower()
    display([t for t in tasks if key in t["title"].lower()])


# ---------- SORT ----------
def sort_tasks():
    order = {"High": 1, "Medium": 2, "Low": 3}
    tasks.sort(key=lambda x: order[x["priority"]])
    save_tasks()
    refresh_list()


# ---------- GUI ----------
root = tk.Tk()
root.title("Advanced To-Do Manager")
root.geometry("500x650")

tasks = load_tasks()

tk.Label(root, text="TO-DO MANAGER", font=("Arial", 16, "bold")).pack(pady=10)

entry = tk.Entry(root, width=30)
entry.pack(pady=5)

priority_var = tk.StringVar(value="Medium")
tk.OptionMenu(root, priority_var, "High", "Medium", "Low").pack()

tk.Button(root, text="Add Task", command=add_task).pack(pady=5)

listbox = tk.Listbox(root, width=60, height=15)
listbox.pack(pady=10)

# filter
f = tk.Frame(root)
f.pack()
tk.Button(f, text="All", command=lambda: filter_tasks("all")).grid(row=0, column=0, padx=5)
tk.Button(f, text="Pending", command=lambda: filter_tasks("pending")).grid(row=0, column=1, padx=5)
tk.Button(f, text="Completed", command=lambda: filter_tasks("completed")).grid(row=0, column=2, padx=5)

# main buttons
frame = tk.Frame(root)
frame.pack()

tk.Button(frame, text="Done", width=12, command=mark_done).grid(row=0, column=0)
tk.Button(frame, text="Delete", width=12, command=delete_task).grid(row=0, column=1)

tk.Button(frame, text="Edit", width=12, command=edit_task).grid(row=1, column=0)
tk.Button(frame, text="Priority", width=12, command=change_priority).grid(row=1, column=1)

tk.Button(frame, text="Up", width=12, command=move_up).grid(row=2, column=0)
tk.Button(frame, text="Down", width=12, command=move_down).grid(row=2, column=1)

tk.Button(frame, text="Clear All", width=25, command=clear_all).grid(row=3, column=0, columnspan=2)

tk.Button(root, text="Search", command=search_task).pack(pady=5)
tk.Button(root, text="Sort by Priority", command=sort_tasks).pack(pady=5)

refresh_list()
root.mainloop()