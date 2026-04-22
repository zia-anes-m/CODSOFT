import tkinter as tk
import random
import winsound  # Windows only

choices = ["rock", "paper", "scissors"]

# Game state
user_score = 0
computer_score = 0
round_count = 0
max_rounds = 5
is_waiting = False


# ---------------- GAME LOGIC ---------------- #

def play(user_choice):
    global is_waiting, round_count

    if is_waiting or round_count >= max_rounds:
        return

    is_waiting = True

    round_label.config(text=f"Round {round_count + 1} of {max_rounds}")
    result_label.config(text="Computer is choosing...", fg="gray")

    disable_buttons()

    root.after(600, lambda: show_result(user_choice))


def show_result(user_choice):
    global user_score, computer_score, round_count, is_waiting

    computer_choice = random.choice(choices)
    round_count += 1

    user_label.config(text=f"You: {user_choice.capitalize()}")
    comp_label.config(text=f"Computer: {computer_choice.capitalize()}")

    if user_choice == computer_choice:
        result = "Draw"
        color = "#f1c40f"

    elif (user_choice == "rock" and computer_choice == "scissors") or \
         (user_choice == "paper" and computer_choice == "rock") or \
         (user_choice == "scissors" and computer_choice == "paper"):

        result = "You Win"
        color = "#2ecc71"
        user_score += 1

    else:
        result = "You Lose"
        color = "#e74c3c"
        computer_score += 1

    # Sound
    try:
        winsound.Beep(1000, 150)
    except:
        pass

    flash_result(f"{result} (Round {round_count})", color)

    score_label.config(text=f"{user_score} : {computer_score}")
    update_progress()

    if round_count == max_rounds:
        end_game()
    else:
        action_label.config(text=f"👉 Select your move for Round {round_count + 1}")
        enable_buttons()

    is_waiting = False


def end_game():
    if user_score > computer_score:
        final = "🏆 YOU WON!"
    elif user_score < computer_score:
        final = "💻 COMPUTER WON"
    else:
        final = "🤝 MATCH DRAW"

    result_label.config(text=final, fg="cyan", font=("Arial", 18, "bold"))
    action_label.config(text="Click Reset to play again")
    disable_buttons()


def reset():
    global user_score, computer_score, round_count, is_waiting

    user_score = 0
    computer_score = 0
    round_count = 0
    is_waiting = False

    user_label.config(text="You:")
    comp_label.config(text="Computer:")
    result_label.config(text="")
    score_label.config(text="0 : 0")
    round_label.config(text="Round 1 of 5")
    action_label.config(text="👉 Select your move for Round 1")

    update_progress()
    enable_buttons()


# ---------------- UI EFFECTS ---------------- #

def disable_buttons():
    rock_btn.config(state="disabled")
    paper_btn.config(state="disabled")
    scissors_btn.config(state="disabled")


def enable_buttons():
    rock_btn.config(state="normal")
    paper_btn.config(state="normal")
    scissors_btn.config(state="normal")


def flash_result(text, color, count=0):
    if count < 6:
        result_label.config(text=text if count % 2 == 0 else "", fg=color)
        root.after(150, lambda: flash_result(text, color, count + 1))
    else:
        result_label.config(text=text, fg=color)


def update_progress():
    progress.delete("all")
    width = (round_count / max_rounds) * 300
    progress.create_rectangle(0, 0, width, 20, fill="#00ffcc")


# Hover effects
def on_enter(e):
    e.widget['bg'] = "#555"


def on_leave(e):
    e.widget['bg'] = e.widget.default_bg


# Keyboard controls
def key_play(event):
    key = event.char.lower()
    if key == 'r':
        play("rock")
    elif key == 'p':
        play("paper")
    elif key == 's':
        play("scissors")


# ---------------- UI ---------------- #

root = tk.Tk()
root.title("Rock Paper Scissors Pro")
root.geometry("450x550")
root.configure(bg="#121212")

root.bind("<Key>", key_play)

tk.Label(root, text="Rock Paper Scissors",
         font=("Arial", 18, "bold"),
         bg="#121212", fg="white").pack(pady=10)

round_label = tk.Label(root, text="Round 1 of 5",
                       font=("Arial", 12),
                       bg="#121212", fg="lightblue")
round_label.pack()

user_label = tk.Label(root, text="You:", font=("Arial", 14),
                      bg="#121212", fg="white")
user_label.pack(pady=5)

comp_label = tk.Label(root, text="Computer:", font=("Arial", 14),
                      bg="#121212", fg="white")
comp_label.pack(pady=5)

result_label = tk.Label(root, text="",
                        font=("Arial", 15, "bold"),
                        bg="#121212")
result_label.pack(pady=15)

score_label = tk.Label(root, text="0 : 0",
                        font=("Arial", 22, "bold"),
                        bg="#121212", fg="white")
score_label.pack()

# Progress bar
progress = tk.Canvas(root, width=300, height=20, bg="gray", highlightthickness=0)
progress.pack(pady=10)

# Action label (highlighted)
action_label = tk.Label(root,
                        text="👉 Select your move for Round 1",
                        font=("Arial", 13, "bold"),
                        bg="#121212",
                        fg="#00ffcc")
action_label.pack(pady=10)

frame = tk.Frame(root, bg="#121212")
frame.pack(pady=20)

btn_style = {
    "font": ("Arial", 11, "bold"),
    "width": 10,
    "height": 2,
    "bd": 0
}

rock_btn = tk.Button(frame, text="Rock", bg="#27ae60", fg="white",
                     command=lambda: play("rock"), **btn_style)
rock_btn.grid(row=0, column=0, padx=10)

paper_btn = tk.Button(frame, text="Paper", bg="#2980b9", fg="white",
                      command=lambda: play("paper"), **btn_style)
paper_btn.grid(row=0, column=1, padx=10)

scissors_btn = tk.Button(frame, text="Scissors", bg="#c0392b", fg="white",
                         command=lambda: play("scissors"), **btn_style)
scissors_btn.grid(row=0, column=2, padx=10)

# Hover binding
for btn in [rock_btn, paper_btn, scissors_btn]:
    btn.default_bg = btn['bg']
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

tk.Button(root, text="Reset Game",
          font=("Arial", 11),
          bg="gray", fg="white",
          command=reset).pack(pady=15)

update_progress()

root.mainloop()