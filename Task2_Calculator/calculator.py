import tkinter as tk
import re

# Store history
history = []

# ---------------- EVALUATION ----------------
def evaluate_expression(expr):
    try:
        expr = expr.replace("×", "*").replace("÷", "/")

        pattern = r'(\d+\.?\d*)([\+\-\*/])(\d+\.?\d*)%'

        while re.search(pattern, expr):
            match = re.search(pattern, expr)
            num1 = float(match.group(1))
            operator = match.group(2)
            num2 = float(match.group(3))

            if operator in ['+', '-']:
                percent_value = (num1 * num2) / 100
            else:
                percent_value = num2 / 100

            expr = expr[:match.start()] + str(num1) + operator + str(percent_value) + expr[match.end():]

        expr = re.sub(r'(\d+\.?\d*)%', r'(\1/100)', expr)

        return eval(expr)

    except:
        return "Error"

# ---------------- BUTTON CLICK ----------------
def click(value):
    current = entry_var.get()

    if value == "=":
        result = evaluate_expression(current)
        entry_var.set(result)

        if result != "Error":
            history.append(f"{current} = {result}")

    elif value == "C":
        entry_var.set("")

    elif value == "⌫":
        entry_var.set(current[:-1])

    else:
        entry.insert(tk.END, value)   # FIXED cursor issue

# ---------------- HISTORY WINDOW ----------------
def show_history():
    win = tk.Toplevel(root)
    win.title("History")
    win.geometry("250x300")
    win.configure(bg="#1e1e1e")

    listbox = tk.Listbox(win, bg="#2d2d2d", fg="white")
    listbox.pack(expand=True, fill="both", padx=10, pady=10)

    for item in history:
        listbox.insert(tk.END, item)

# ---------------- KEYBOARD ----------------
def key_press(event):
    key = event.char

    if key in "0123456789+-*/.%()":
        entry.insert(tk.END, key)
    elif event.keysym == "Return":
        click("=")
    elif event.keysym == "BackSpace":
        click("⌫")

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Calculator")
root.geometry("300x480")
root.configure(bg="#1e1e1e")

entry_var = tk.StringVar()
entry = tk.Entry(root, textvariable=entry_var, font=("Arial", 22),
                 bd=10, relief=tk.FLAT, justify="right",
                 bg="#2d2d2d", fg="white", insertbackground="white")
entry.pack(fill=tk.BOTH, padx=10, pady=10)

# Top buttons (History)
top_frame = tk.Frame(root, bg="#1e1e1e")
top_frame.pack(fill="x")

history_btn = tk.Button(top_frame, text="History",
                        command=show_history,
                        bg="#3c3f41", fg="white")
history_btn.pack(side="right", padx=10, pady=5)

# Buttons layout
buttons = [
    ["C", "⌫", "(", ")"],
    ["7", "8", "9", "÷"],
    ["4", "5", "6", "×"],
    ["1", "2", "3", "-"],
    ["0", ".", "%", "+"]
]

frame = tk.Frame(root, bg="#1e1e1e")
frame.pack(expand=True, fill="both")

# Create buttons
for r, row in enumerate(buttons):
    for c, val in enumerate(row):
        btn = tk.Button(frame, text=val, font=("Arial", 14),
                        command=lambda v=val: click(v),
                        bg="#3c3f41", fg="white")

        btn.grid(row=r, column=c, sticky="nsew", ipadx=10, ipady=15)

# "=" button
equals_btn = tk.Button(frame, text="=", font=("Arial", 14),
                       command=lambda: click("="),
                       bg="#3c3f41", fg="white")

equals_btn.grid(row=5, column=0, columnspan=4,
                sticky="nsew", ipadx=10, ipady=15)

# Grid config
for i in range(6):
    frame.grid_rowconfigure(i, weight=1)
for i in range(4):
    frame.grid_columnconfigure(i, weight=1)

# Keyboard binding
root.bind("<Key>", key_press)

root.mainloop()