import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
import hashlib
import time
from datetime import datetime

STYLE = {
    "BG": "#F0F2F5",  # Light grey, less stark than pure white
    "PRIMARY": "#007BFF",
    "SECONDARY": "#0056b3",
    "HOVER": "#004085",
    "SUCCESS": "#28a745",
    "SUCCESS_HOVER": "#218838",
    "DISABLED_BG": "#6C757D",
    "DISABLED_HOVER": "#5a6268",
    "ACCENT": "#17A2B8", # A nice teal/cyan
    "TEXT": "#212529",
    "TEXT_LIGHT": "#FFFFFF",
    "DISABLED_FG": "#CED4DA",
    "CORRECT": "#4CAF50",
    "INCORRECT": "#F44336",
    "FONT_TITLE": ("Arial", 32, "bold"),
    "FONT_HEADER": ("Arial", 16, "bold"),
    "FONT_BODY": ("Arial", 12),
    "FONT_BUTTON": ("Arial", 14, "bold"),
}

SECURITY_QUESTIONS = [
    "What was your first pet's name?",
    "What is your mother's maiden name?",
    "What was the name of your elementary school?",
    "In what city were you born?",
    "What is your favorite book?"
]

class CustomButton(tk.Frame):
    def __init__(self, parent, text, command, padx=20, pady=10, font=None, bg_color=None, fg_color=None, hover_color=None, radius=25):
        parent_bg = parent.cget("bg")
        super().__init__(parent, bg=parent_bg)

        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.radius = radius

        test_label = tk.Label(self, text=text, font=font, padx=padx, pady=pady)
        width = test_label.winfo_reqwidth()
        height = test_label.winfo_reqheight()
        test_label.destroy()

        self.canvas = tk.Canvas(self, width=width, height=height, bg=parent_bg, highlightthickness=0)
        self.canvas.pack()

        self.rect = self._round_rectangle(0, 0, width, height, radius=self.radius, fill=self.bg_color, outline=self.bg_color)
        self.text_id = self.canvas.create_text(width/2, height/2, text=text, font=font, fill=fg_color)

        self.canvas.tag_bind(self.rect, "<Enter>", self._on_enter)
        self.canvas.tag_bind(self.text_id, "<Enter>", self._on_enter)
        self.canvas.tag_bind(self.rect, "<Leave>", self._on_leave)
        self.canvas.tag_bind(self.text_id, "<Leave>", self._on_leave)
        self.canvas.tag_bind(self.rect, "<Button-1>", self._on_click)
        self.canvas.tag_bind(self.text_id, "<Button-1>", self._on_click)

    def _round_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]
        return self.canvas.create_polygon(points, **kwargs, smooth=True)

    def _on_enter(self, event):
        self.canvas.itemconfig(self.rect, fill=self.hover_color, outline=self.hover_color)

    def _on_leave(self, event):
        self.canvas.itemconfig(self.rect, fill=self.bg_color, outline=self.bg_color)

    def _on_click(self, event):
        if self.command:
            self.command()

class ChoiceButton(tk.Frame):
    def __init__(self, parent, text, value, variable):
        super().__init__(parent, bg="#FFFFFF", highlightbackground="#CCCCCC", highlightthickness=1)
        
        self.value = value
        self.variable = variable
        
        # Using a wraplength that is less than the parent width to avoid text touching edges
        self.label = tk.Label(self, text=text, font=STYLE["FONT_BODY"], bg="#FFFFFF", fg=STYLE["TEXT"], justify="left", anchor="w", wraplength=580)
        self.label.pack(padx=15, pady=10, fill="x", expand=True)

        self.bind_all("<Enter>", self._on_enter)
        self.bind_all("<Leave>", self._on_leave)
        self.bind_all("<Button-1>", self._on_click)

    def bind_all(self, sequence, func):
        self.bind(sequence, func)
        self.label.bind(sequence, func)
    
    def unbind_all(self, sequence):
        self.unbind(sequence)
        self.label.unbind(sequence)

    def _on_enter(self, event):
        if self.variable.get() != self.value:
            self.config(bg="#E9ECEF") # A light grey hover
            self.label.config(bg="#E9ECEF")

    def _on_leave(self, event):
        if self.variable.get() != self.value:
            self.config(bg="#FFFFFF")
            self.label.config(bg="#FFFFFF")

    def _on_click(self, event):
        self.variable.set(self.value)

    def set_selected(self, is_selected):
        if is_selected:
            self.config(bg=STYLE["PRIMARY"], highlightbackground=STYLE["SECONDARY"], highlightthickness=2)
            self.label.config(bg=STYLE["PRIMARY"], fg=STYLE["TEXT_LIGHT"])
        else:
            self.config(bg="#FFFFFF", highlightbackground="#CCCCCC", highlightthickness=1)
            self.label.config(bg="#FFFFFF", fg=STYLE["TEXT"])
            
    def set_feedback(self, is_correct, is_user_choice):
        self.unbind_all("<Enter>")
        self.unbind_all("<Leave>")
        self.unbind_all("<Button-1>")
        
        if is_correct:
            self.config(bg=STYLE["CORRECT"], highlightbackground=STYLE["SUCCESS_HOVER"], highlightthickness=2)
            self.label.config(bg=STYLE["CORRECT"], fg=STYLE["TEXT_LIGHT"])
        elif is_user_choice:
            self.config(bg=STYLE["INCORRECT"], highlightbackground="#c82333", highlightthickness=2) # A darker red for border
            self.label.config(bg=STYLE["INCORRECT"], fg=STYLE["TEXT_LIGHT"])
        else:
            self.config(bg="#FFFFFF", highlightbackground="#DDDDDD", highlightthickness=1)
            self.label.config(bg="#FFFFFF", fg="#AAAAAA") # Dim the text

class ToggleSwitch(tk.Frame):
    def __init__(self, parent, variable):
        super().__init__(parent, bg=parent.cget("bg"))
        self.variable = variable
        self.width = 50
        self.height = 26
        self.radius = self.height / 2
        
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg=parent.cget("bg"), highlightthickness=0)
        self.canvas.pack()
        
        self.track = self.canvas.create_line(self.radius, self.radius, self.width - self.radius, self.radius, width=self.height, capstyle="round")
        self.thumb = self.canvas.create_oval(3, 3, self.height-3, self.height-3, width=0)
        
        self.canvas.tag_bind(self.track, "<Button-1>", self._on_click)
        self.canvas.tag_bind(self.thumb, "<Button-1>", self._on_click)
        
        self.variable.trace_add("write", self._update_visuals)
        self._update_visuals()

    def _on_click(self, event):
        self.variable.set(not self.variable.get())

    def _update_visuals(self, *args):
        if self.variable.get():
            self.canvas.itemconfig(self.track, fill=STYLE["SUCCESS"])
            self.canvas.coords(self.thumb, self.width - self.height + 3, 3, self.width - 3, self.height - 3)
            self.canvas.itemconfig(self.thumb, fill="#FFFFFF")
        else:
            self.canvas.itemconfig(self.track, fill="#CCCCCC")
            self.canvas.coords(self.thumb, 3, 3, self.height - 3, self.height - 3)
            self.canvas.itemconfig(self.thumb, fill="#FFFFFF")

class QuizApp:
    def __init__(self):
        self.root = tk.Tk()
        self.current_user = None
        self.current_user_role = None
        self.setup_window()
        self.configure_styles()
        self.load_data()
        self.reset_quiz()
        self.create_login_page()
        
    def setup_window(self):
        self.root.title("Enhanced Quiz App")
        self.root.geometry("800x650")
        self.root.configure(bg=STYLE["BG"])
        self.root.resizable(False, False)

    def configure_styles(self):
        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')
        self.style.configure("TCombobox",
                             fieldbackground="#FFFFFF",
                             background="#FFFFFF",
                             foreground=STYLE["TEXT"],
                             arrowcolor=STYLE["TEXT"],
                             padding=5)
        self.style.configure("TProgressbar",
                             thickness=10,
                             background=STYLE["PRIMARY"],
                             troughcolor="#E9ECEF")

    def load_data(self):
        self.questions_file = "questions.json"
        try:
            with open(self.questions_file, "r") as f:
                self.categories = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.categories = self.get_default_questions()
            self._save_questions()

        self._load_users()

        try:
            with open("scores.json", "r") as f:
                self.high_scores = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.high_scores = []
    
    def save_scores(self):
        with open("scores.json", "w") as f:
            json.dump(self.high_scores, f, indent=4)

    def _load_users(self):
        self.users_file = "users.json"
        try:
            with open(self.users_file, "r") as f:
                self.users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.users = {}

        users_updated = False

        # Ensure the root admin user "sai kiran" exists and has the correct role.
        root_admin_user = "sai kiran"
        if root_admin_user not in self.users or self.users[root_admin_user].get("role") != "root_admin":
            root_admin_password = "sai123@R"
            password_hash = hashlib.sha256(root_admin_password.encode()).hexdigest()
            if root_admin_user not in self.users:
                self.users[root_admin_user] = {}
            self.users[root_admin_user]["password"] = password_hash
            self.users[root_admin_user]["role"] = "root_admin"
            users_updated = True

        # Ensure a default demo user exists for testing.
        demo_user_name = "demo"
        if demo_user_name not in self.users:
            demo_user_password = "demo"
            password_hash = hashlib.sha256(demo_user_password.encode()).hexdigest()
            self.users[demo_user_name] = {
                "password": password_hash, "role": "user"
            }
            users_updated = True

        if users_updated:
            self._save_users()

    def _save_users(self):
        with open(self.users_file, "w") as f:
            json.dump(self.users, f, indent=4)

    def _save_questions(self):
        with open(self.questions_file, "w") as f:
            json.dump(self.categories, f, indent=4)
    
    def reset_quiz(self):
        self.current_category = None
        self.difficulty = "Medium"
        self.current_questions = []
        self.current_choices = []
        self.current_answers = []
        self.choice_widgets = []
        self.user_answers = []
        self.question_index = 0
        self.score = 0
        self.start_time = None
        self.time_limit = 0
        self.timer_running = False
        self.current_user_role = None

    def create_login_page(self):
        self.clear_window()
        login_frame = tk.Frame(self.root, bg=STYLE["BG"])
        login_frame.pack(expand=True)

        # Icon and Title
        icon_canvas = tk.Canvas(login_frame, width=100, height=100, bg=STYLE["BG"], highlightthickness=0)
        icon_canvas.pack(pady=(10, 0))
        icon_canvas.create_oval(5, 5, 95, 95, fill=STYLE["PRIMARY"], outline="")
        icon_canvas.create_text(50, 55, text="?", font=("Arial", 50, "bold"), fill=STYLE["TEXT_LIGHT"])
        tk.Label(login_frame, text="QUIZ APP LOGIN", font=STYLE["FONT_TITLE"], bg=STYLE["BG"], fg=STYLE["TEXT"]).pack(pady=(5, 40))

        # Entry fields
        username_var = tk.StringVar()
        password_var = tk.StringVar()

        tk.Label(login_frame, text="Username", font=STYLE["FONT_HEADER"], bg=STYLE["BG"], fg=STYLE["TEXT"]).pack()
        tk.Entry(login_frame, textvariable=username_var, font=STYLE["FONT_BODY"], width=30, relief="solid", bd=1).pack(pady=(5, 20))

        tk.Label(login_frame, text="Password", font=STYLE["FONT_HEADER"], bg=STYLE["BG"], fg=STYLE["TEXT"]).pack()
        tk.Entry(login_frame, textvariable=password_var, show="*", font=STYLE["FONT_BODY"], width=30, relief="solid", bd=1).pack(pady=5)

        # Buttons
        btn_frame = tk.Frame(login_frame, bg=STYLE["BG"])
        btn_frame.pack(pady=40)

        CustomButton(btn_frame, text="LOGIN", command=lambda: self._attempt_login(username_var.get(), password_var.get()), font=STYLE["FONT_BUTTON"],
                     bg_color=STYLE["PRIMARY"], fg_color=STYLE["TEXT_LIGHT"], hover_color=STYLE["SECONDARY"]).pack(side=tk.LEFT, padx=10)
        
        CustomButton(btn_frame, text="SIGN UP", command=self._show_signup_page, font=STYLE["FONT_BUTTON"],
                     bg_color=STYLE["SUCCESS"], fg_color=STYLE["TEXT_LIGHT"], hover_color=STYLE["SUCCESS_HOVER"]).pack(side=tk.LEFT, padx=10)

        # Forgot Password Link
        forgot_label = tk.Label(login_frame, text="Forgot Password?", font=("Arial", 10, "underline"), bg=STYLE["BG"], fg=STYLE["PRIMARY"], cursor="hand2")
        forgot_label.pack(pady=(10,0))
        forgot_label.bind("<Button-1>", lambda e: self._show_forgot_password_flow())

    def _attempt_login(self, username, password):

        if not username or not password:
            messagebox.showerror("Login Failed", "Please enter both username and password.")
            return

        user_data = self.users.get(username)
        if user_data:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if password_hash == user_data["password"]:
                self.current_user = username
                self.current_user_role = user_data.get("role", "user")
                self.create_main_menu()
            else:
                messagebox.showerror("Login Failed", "Incorrect password.")
        else:
            messagebox.showerror("Login Failed", "Username not found.")

    def _show_signup_page(self):
        signup_window = tk.Toplevel(self.root)
        signup_window.title("Sign Up")
        signup_window.geometry("450x550")
        signup_window.configure(bg=STYLE["BG"])
        signup_window.resizable(False, False)
        signup_window.transient(self.root)
        signup_window.grab_set()

        tk.Label(signup_window, text="Create Account", font=("Arial", 20, "bold"), bg=STYLE["BG"], fg=STYLE["TEXT"]).pack(pady=20)

        username_var = tk.StringVar()
        password_var = tk.StringVar()
        confirm_var = tk.StringVar()
        sq_var = tk.StringVar(value=SECURITY_QUESTIONS[0])
        sa_var = tk.StringVar()

        tk.Label(signup_window, text="Username", font=STYLE["FONT_BODY"], bg=STYLE["BG"], fg=STYLE["TEXT"]).pack()
        tk.Entry(signup_window, textvariable=username_var, font=STYLE["FONT_BODY"], width=30, relief="solid", bd=1).pack(pady=(5, 15))

        tk.Label(signup_window, text="Password (min. 6 chars)", font=STYLE["FONT_BODY"], bg=STYLE["BG"], fg=STYLE["TEXT"]).pack()
        tk.Entry(signup_window, textvariable=password_var, show="*", font=STYLE["FONT_BODY"], width=30, relief="solid", bd=1).pack(pady=5)

        tk.Label(signup_window, text="Confirm Password", font=STYLE["FONT_BODY"], bg=STYLE["BG"], fg=STYLE["TEXT"]).pack()
        tk.Entry(signup_window, textvariable=confirm_var, show="*", font=STYLE["FONT_BODY"], width=30, relief="solid", bd=1).pack(pady=5)

        tk.Label(signup_window, text="Security Question", font=STYLE["FONT_BODY"], bg=STYLE["BG"], fg=STYLE["TEXT"]).pack(pady=(15, 5))
        ttk.Combobox(signup_window, textvariable=sq_var, values=SECURITY_QUESTIONS, 
                     state="readonly", width=40, font=("Arial", 10)).pack()

        tk.Label(signup_window, text="Security Answer", font=STYLE["FONT_BODY"], bg=STYLE["BG"], fg=STYLE["TEXT"]).pack(pady=(15, 5))
        tk.Entry(signup_window, textvariable=sa_var, font=STYLE["FONT_BODY"], width=30, relief="solid", bd=1).pack(pady=5)

        CustomButton(signup_window, text="CREATE ACCOUNT", 
                     command=lambda: self._create_account(username_var.get(), password_var.get(), confirm_var.get(), sq_var.get(), sa_var.get(), signup_window),
                     font=STYLE["FONT_BUTTON"], bg_color=STYLE["SUCCESS"], fg_color=STYLE["TEXT_LIGHT"], 
                     hover_color=STYLE["SUCCESS_HOVER"]).pack(pady=30)

    def _create_account(self, username, password, confirm, sq_text, sa, window):
        error_message = self._create_user_logic(username, password, confirm, sq_text, sa)
        if error_message:
            messagebox.showerror("Error", error_message, parent=window)
        else:
            messagebox.showinfo("Success", "Account created successfully! You can now log in.", parent=window)
            window.destroy()

    def _create_user_logic(self, username, password, confirm, sq_text, sa):
        """Core logic for creating a user. Returns an error message string or None on success."""
        if not all([username, password, confirm, sq_text, sa]):
            return "Please fill all fields."

        if username in self.users:
            return "Username already exists."

        if password != confirm:
            return "Passwords do not match."
        
        if len(password) < 6:
            return "Password must be at least 6 characters long."

        # If all validation passes, create the user
        sq_idx = SECURITY_QUESTIONS.index(sq_text)
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        sa_hash = hashlib.sha256(sa.lower().encode()).hexdigest()
        self.users[username] = {
            "password": password_hash, 
            "role": "user",
            "security_question_idx": sq_idx,
            "security_answer_hash": sa_hash
        }
        self._save_users()
        return None # Indicates success

    def create_main_menu(self):
        self.clear_window()

        # --- Header with Welcome and Logout ---
        header_frame = tk.Frame(self.root, bg=STYLE["BG"])
        header_frame.pack(fill="x", padx=20, pady=(10, 0))
        tk.Label(header_frame, text=f"Welcome, {self.current_user}!", font=STYLE["FONT_BODY"], bg=STYLE["BG"], fg=STYLE["TEXT"]).pack(side="left")
        CustomButton(header_frame, text="Logout", command=self._logout, font=("Arial", 10), 
                     bg_color=STYLE["DISABLED_BG"], fg_color=STYLE["TEXT_LIGHT"], hover_color=STYLE["DISABLED_HOVER"],
                     padx=15, pady=5, radius=15).pack(side="right")

        # Main container frame
        main_frame = tk.Frame(self.root, bg=STYLE["BG"])
        main_frame.pack(expand=True, fill="both", padx=60, pady=0)

        # --- Icon and Title ---
        icon_canvas = tk.Canvas(main_frame, width=100, height=100, bg=STYLE["BG"], highlightthickness=0)
        icon_canvas.pack(pady=(10, 0))
        icon_canvas.create_oval(5, 5, 95, 95, fill=STYLE["PRIMARY"], outline="")
        icon_canvas.create_text(50, 55, text="?", font=("Arial", 50, "bold"), fill=STYLE["TEXT_LIGHT"])
        
        tk.Label(main_frame, text="QUIZ APP", font=STYLE["FONT_TITLE"], bg=STYLE["BG"], fg=STYLE["TEXT"]).pack(pady=(5, 25))

        # --- Settings Frame ---
        settings_frame = tk.Frame(main_frame, bg=STYLE["BG"])
        settings_frame.pack(pady=10, fill="x")
        settings_frame.columnconfigure(0, weight=1)
        settings_frame.columnconfigure(1, weight=1)

        # Category
        tk.Label(settings_frame, text="Category", font=STYLE["FONT_HEADER"], bg=STYLE["BG"], fg=STYLE["TEXT"]).grid(row=0, column=0, sticky="w", pady=10)
        self.category_var = tk.StringVar(value=list(self.categories.keys())[0])
        ttk.Combobox(settings_frame, textvariable=self.category_var, values=list(self.categories.keys()), font=STYLE["FONT_BODY"], state="readonly", width=30).grid(row=0, column=1, sticky="e", pady=10)

        # Difficulty
        tk.Label(settings_frame, text="Difficulty", font=STYLE["FONT_HEADER"], bg=STYLE["BG"], fg=STYLE["TEXT"]).grid(row=1, column=0, sticky="w", pady=10)
        self.difficulty_var = tk.StringVar(value="Medium")
        difficulties = ["Easy", "Medium", "Hard"]
        diff_frame = tk.Frame(settings_frame, bg=STYLE["BG"])
        diff_frame.grid(row=1, column=1, sticky="e", pady=10)
        for diff in difficulties:
            rb = tk.Radiobutton(diff_frame, text=diff, variable=self.difficulty_var, value=diff,
                                indicatoron=0, padx=20, pady=8, font=("Arial", 11, "bold"),
                                bg=STYLE["DISABLED_BG"], fg=STYLE["TEXT_LIGHT"],
                                activebackground=STYLE["DISABLED_BG"], activeforeground=STYLE["TEXT_LIGHT"],
                                selectcolor=STYLE["PRIMARY"], relief="flat", bd=0, borderwidth=0)
            rb.pack(side="left")

        # Timer
        tk.Label(settings_frame, text="Enable Timer", font=STYLE["FONT_HEADER"], bg=STYLE["BG"], fg=STYLE["TEXT"]).grid(row=2, column=0, sticky="w", pady=10)
        self.timer_var = tk.BooleanVar(value=True)
        ToggleSwitch(settings_frame, self.timer_var).grid(row=2, column=1, sticky="e", pady=10)

        # --- Action Buttons ---
        bottom_container = tk.Frame(main_frame, bg=STYLE["BG"])
        bottom_container.pack(side="bottom", pady=(30, 10))
        action_frame = tk.Frame(bottom_container, bg=STYLE["BG"])
        action_frame.pack()
        
        buttons = []
        buttons.append(CustomButton(action_frame, text="START QUIZ", command=self.start_quiz, font=STYLE["FONT_BUTTON"],
                     bg_color=STYLE["PRIMARY"], fg_color=STYLE["TEXT_LIGHT"], hover_color=STYLE["SECONDARY"]))
        
        buttons.append(CustomButton(action_frame, text="HIGH SCORES", command=self.show_high_scores, font=STYLE["FONT_BUTTON"],
                     bg_color=STYLE["DISABLED_BG"], fg_color=STYLE["TEXT_LIGHT"], hover_color=STYLE["DISABLED_HOVER"]))
        
        # Conditionally show admin buttons
        if self.current_user_role in ['root_admin', 'admin']:
            buttons.append(CustomButton(action_frame, text="ADD QUESTIONS", command=self.add_questions, font=STYLE["FONT_BUTTON"],
                         bg_color=STYLE["SUCCESS"], fg_color=STYLE["TEXT_LIGHT"], hover_color=STYLE["SUCCESS_HOVER"]))
            
        # The root admin is the only one who can manage other users
        if self.current_user_role == 'root_admin':
             buttons.append(CustomButton(action_frame, text="MANAGE ADMINS", command=self.show_user_management_page, font=STYLE["FONT_BUTTON"],
                          bg_color=STYLE["ACCENT"], fg_color=STYLE["TEXT_LIGHT"], hover_color=STYLE["SECONDARY"]))

        if len(buttons) == 4:
            # Use a 2x2 grid for 4 buttons to make them more visible and aligned
            action_frame.columnconfigure((0, 1), weight=1)
            action_frame.rowconfigure((0, 1), weight=1)
            buttons[0].grid(row=0, column=0, padx=10, pady=10)
            buttons[1].grid(row=0, column=1, padx=10, pady=10)
            buttons[2].grid(row=1, column=0, padx=10, pady=10)
            buttons[3].grid(row=1, column=1, padx=10, pady=10)
        else:
            # Use pack for 2 or 3 buttons, which looks fine
            for btn in buttons:
                btn.pack(side=tk.LEFT, padx=10)
    
    def _logout(self):
        self.current_user = None
        self.current_user_role = None
        self.reset_quiz()
        self.create_login_page()
    
    def start_quiz(self):
        self.current_category = self.category_var.get()
        self.difficulty = self.difficulty_var.get()
        category_data = self.categories[self.current_category]
        
        # Shuffle all questions for variety each time
        all_questions = list(zip(
            category_data["questions"],
            category_data["choices"],
            category_data["answers"]
        ))
        random.shuffle(all_questions)

        # Determine number of questions based on difficulty
        num_questions_map = {"Easy": 5, "Medium": 10, "Hard": len(all_questions)}
        num_questions = min(num_questions_map.get(self.difficulty, 10), len(all_questions))

        if not all_questions:
            messagebox.showerror("Error", "No questions available in this category.")
            self.create_main_menu()
            return

        # Unpack the selected number of questions
        selected_questions = all_questions[:num_questions]
        q, c, a = zip(*selected_questions)
        self.current_questions, self.current_choices, self.current_answers = list(q), list(c), list(a)
        
        self.question_index = 0
        self.score = 0
        self.user_answers = []
        
        if self.timer_var.get():
            time_per_question = {"Easy": 45, "Medium": 30, "Hard": 15}
            self.time_limit = num_questions * time_per_question.get(self.difficulty, 30)
            self.start_time = time.time()
            self.timer_running = True
        
        self.show_question()
    
    def show_question(self):
        num_questions = len(self.current_questions)
        if self.question_index >= num_questions:
            self.show_results()
            return
            
        self.clear_window()
        
        # Timer display
        if self.timer_var.get():
            self.timer_label = tk.Label(self.root, text="", font=(STYLE["FONT_BODY"][0], 14, "bold"),
                                       bg=STYLE["BG"], fg=STYLE["PRIMARY"])
            self.timer_label.pack(pady=10)
            self.update_timer()
        
        # Progress bar
        progress = (self.question_index / num_questions) * 100
        tk.Label(self.root, text=f"Question {self.question_index + 1} of {num_questions}",
                font=STYLE["FONT_BODY"], bg=STYLE["BG"], fg=STYLE["TEXT"]).pack(pady=10)
        
        progress_bar = ttk.Progressbar(self.root, length=400, mode='determinate')
        progress_bar['value'] = progress
        progress_bar.pack(pady=10)
        
        # Question
        question_text = self.current_questions[self.question_index]
        tk.Label(self.root, text=question_text, font=(STYLE["FONT_BODY"][0], 14), 
                bg=STYLE["BG"], fg=STYLE["TEXT"], wraplength=700, justify="center").pack(pady=30)
        
        # Answer choices
        self.answer_var = tk.IntVar(value=-1)
        self.answer_var.trace_add("write", self._update_choice_visuals)
        choices = self.current_choices[self.question_index]
        self.choice_widgets = []

        for i, choice in enumerate(choices):
            choice_btn = ChoiceButton(self.root, text=f"{chr(65+i)}) {choice}", value=i, variable=self.answer_var)
            choice_btn.pack(pady=4, padx=100, fill="x")
            self.choice_widgets.append(choice_btn)
        
        # Submit button
        CustomButton(self.root, text="SUBMIT", command=self.submit_answer, font=(STYLE["FONT_BODY"][0], 12, "bold"),
                     bg_color=STYLE["PRIMARY"], fg_color=STYLE["TEXT_LIGHT"], hover_color=STYLE["SECONDARY"], padx=30, pady=10).pack(pady=30)
    
    def update_timer(self):
        if not self.timer_running:
            return
            
        elapsed = time.time() - self.start_time
        remaining = max(0, self.time_limit - elapsed)
        
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        
        if remaining <= 0:
            self.timer_running = False
            messagebox.showwarning("Time Up!", "Time's up! Quiz will end now.")
            self.show_results()
            return
        
        self.timer_label.config(text=f"Time Remaining: {minutes:02d}:{seconds:02d}")
        
        if remaining <= 60:  # Last minute - red warning
            self.timer_label.config(fg=STYLE["INCORRECT"])
        
        self.root.after(1000, self.update_timer)
    
    def submit_answer(self):
        if self.answer_var.get() == -1:
            messagebox.showwarning("No Answer", "Please select an answer!")
            return
        
        self.user_answers.append(self.answer_var.get())
        
        if self.user_answers[-1] == self.current_answers[self.question_index]:
            self.score += 1

        # Provide visual feedback
        correct_idx = self.current_answers[self.question_index]
        user_idx = self.user_answers[-1]

        for i, widget in enumerate(self.choice_widgets):
            is_correct = (i == correct_idx)
            is_user_choice = (i == user_idx)
            widget.set_feedback(is_correct, is_user_choice)

        # Wait a moment before showing the next question
        self.root.after(1500, self._next_question)

    def _next_question(self):
        self.question_index += 1
        self.show_question()
    
    def _update_choice_visuals(self, *args):
        selected_value = self.answer_var.get()
        for i, widget in enumerate(self.choice_widgets):
            widget.set_selected(i == selected_value)
    
    def show_results(self):
        self.timer_running = False
        self.clear_window()
        
        # Calculate score percentage
        total_questions = len(self.current_questions)
        percentage = (self.score / total_questions) * 100 if total_questions > 0 else 0
        
        # Result display
        tk.Label(self.root, text="QUIZ COMPLETED!", 
                font=(STYLE["FONT_TITLE"][0], 28, "bold"), bg=STYLE["BG"], fg=STYLE["TEXT"]).pack(pady=50)
        
        tk.Label(self.root, text=f"Score: {self.score}/{total_questions} ({percentage:.1f}%)",
                font=(STYLE["FONT_BODY"][0], 20), bg=STYLE["BG"], fg=STYLE["PRIMARY"]).pack(pady=20)
        
        # Performance message
        if percentage >= 90:
            message = "OUTSTANDING! 🏆"
            color = "#FFD700"
        elif percentage >= 80:
            message = "EXCELLENT! 🌟"
            color = "#32CD32"
        elif percentage >= 70:
            message = "GOOD JOB! 👍"
            color = "#FFA500"
        elif percentage >= 60:
            message = "KEEP PRACTICING! 📚"
            color = "#FF6347"
        else:
            message = "NEED MORE STUDY! 💪"
            color = "#FF4500"
        
        tk.Label(self.root, text=message, font=("Arial", 18, "bold"),
                bg=STYLE["BG"], fg=color).pack(pady=20)
        
        # Save high score
        player_name = self.current_user
        if player_name:
            score_entry = {
                "name": player_name,
                "score": self.score,
                "total": total_questions,
                "percentage": percentage,
                "category": self.current_category,
                "difficulty": self.difficulty,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            self.high_scores.append(score_entry)
            self.high_scores.sort(key=lambda x: x["percentage"], reverse=True)
            self.high_scores = self.high_scores[:10]  # Keep top 10
            self.save_scores()
        
        # Buttons
        btn_frame = tk.Frame(self.root, bg=STYLE["BG"])
        btn_frame.pack(pady=40)
        
        CustomButton(btn_frame, text="PLAY AGAIN", command=self.create_main_menu, font=(STYLE["FONT_BODY"][0], 12, "bold"),
                     bg_color=STYLE["PRIMARY"], fg_color=STYLE["TEXT_LIGHT"], hover_color=STYLE["SECONDARY"], padx=20, pady=10).pack(side=tk.LEFT, padx=10)
        
        CustomButton(btn_frame, text="VIEW ANSWERS", command=self.show_review, font=(STYLE["FONT_BODY"][0], 12, "bold"),
                     bg_color=STYLE["DISABLED_BG"], fg_color=STYLE["TEXT_LIGHT"], hover_color=STYLE["DISABLED_HOVER"], padx=20, pady=10).pack(side=tk.LEFT, padx=10)
    
    def show_review(self):
        review_window = tk.Toplevel(self.root)
        review_window.title("Answer Review")
        review_window.geometry("700x500")
        review_window.configure(bg=STYLE["BG"])
        
        # Scrollable frame
        canvas = tk.Canvas(review_window, bg=STYLE["BG"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(review_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=STYLE["BG"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Review content
        for i, question in enumerate(self.current_questions):
            frame = tk.Frame(scrollable_frame, bg="#FFFFFF", relief="solid", bd=1)
            frame.pack(fill="x", padx=10, pady=5)
            
            tk.Label(frame, text=f"Q{i+1}: {question}", font=(STYLE["FONT_BODY"][0], 10, "bold"),
                    bg="#FFFFFF", fg=STYLE["TEXT"], wraplength=600, justify="left").pack(anchor="w", padx=10, pady=5)
            
            correct_choice = self.current_choices[i][self.current_answers[i]]
            user_choice = self.current_choices[i][self.user_answers[i]] if i < len(self.user_answers) else "No answer (Time up?)"
            
            tk.Label(frame, text=f"Correct Answer: {correct_choice}", font=(STYLE["FONT_BODY"][0], 9),
                    bg="#FFFFFF", fg=STYLE["CORRECT"]).pack(anchor="w", padx=20)
            
            is_correct = i < len(self.user_answers) and self.user_answers[i] == self.current_answers[i]
            color = STYLE["CORRECT"] if is_correct else STYLE["INCORRECT"]
            tk.Label(frame, text=f"Your Answer: {user_choice}", font=(STYLE["FONT_BODY"][0], 9),
                    bg="#FFFFFF", fg=color).pack(anchor="w", padx=20, pady=(0, 5))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def show_high_scores(self):
        scores_window = tk.Toplevel(self.root)
        scores_window.title("High Scores")
        scores_window.geometry("600x450")
        scores_window.configure(bg=STYLE["BG"])
        
        tk.Label(scores_window, text="HIGH SCORES", font=("Arial", 20, "bold"),
                bg=STYLE["BG"], fg=STYLE["TEXT"]).pack(pady=20)
        
        if not self.high_scores:
            tk.Label(scores_window, text="No scores yet!", font=("Arial", 14),
                    bg=STYLE["BG"], fg=STYLE["PRIMARY"]).pack(pady=50)
        else:
            for i, score in enumerate(self.high_scores[:10]):
                rank_color = ["#FFD700", "#C0C0C0", "#CD7F32"][i] if i < 3 else STYLE["TEXT"]
                score_text = f"{i+1}. {score['name']} - {score['percentage']:.1f}% ({score['category']} - {score.get('difficulty', 'N/A')})"
                tk.Label(scores_window, text=score_text, font=("Arial", 12),
                        bg=STYLE["BG"], fg=rank_color).pack(pady=3)
    
    def add_questions(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Questions")
        add_window.geometry("600x550")
        add_window.configure(bg=STYLE["BG"])
        
        tk.Label(add_window, text="Add New Question", font=("Arial", 16, "bold"),
                bg=STYLE["BG"], fg=STYLE["TEXT"]).pack(pady=20)
        
        # Category selection
        tk.Label(add_window, text="Category (select existing or type a new one):", bg=STYLE["BG"], fg=STYLE["TEXT"]).pack()
        category_var = tk.StringVar()
        ttk.Combobox(add_window, textvariable=category_var, width=58,
                    values=list(self.categories.keys())).pack(pady=5)
        
        # Question input
        tk.Label(add_window, text="Question:", bg=STYLE["BG"], fg=STYLE["TEXT"]).pack(pady=(20, 5))
        question_entry = tk.Text(add_window, height=3, width=60, bg="#FFFFFF", fg=STYLE["TEXT"], insertbackground=STYLE["TEXT"], relief="solid", bd=1)
        question_entry.pack(pady=5)
        
        # Answer choices
        choice_entries = []
        for i in range(4):
            tk.Label(add_window, text=f"Choice {chr(65+i)}:", bg=STYLE["BG"], fg=STYLE["TEXT"]).pack()
            entry = tk.Entry(add_window, width=60, bg="#FFFFFF", fg=STYLE["TEXT"], insertbackground=STYLE["TEXT"], relief="solid", bd=1)
            entry.pack(pady=2)
            choice_entries.append(entry)
        
        # Correct answer
        tk.Label(add_window, text="Correct Answer (A/B/C/D):", bg=STYLE["BG"], fg=STYLE["TEXT"]).pack(pady=(10, 5))
        correct_var = tk.StringVar(value="A")
        ttk.Combobox(add_window, textvariable=correct_var, values=["A", "B", "C", "D"]).pack()
        
        def save_question():
            question = question_entry.get("1.0", tk.END).strip()
            choices = [entry.get().strip() for entry in choice_entries]
            correct_idx = ord(correct_var.get()) - ord('A')
            category = category_var.get().strip()
            
            if not all([question, category] + choices):
                messagebox.showerror("Error", "Please fill all fields!")
                return

            if category not in self.categories:
                self.categories[category] = {"questions": [], "choices": [], "answers": []}

            try:
                self.categories[category]["questions"].append(question)
                self.categories[category]["choices"].append(choices)
                self.categories[category]["answers"].append(correct_idx)
                self._save_questions()
                messagebox.showinfo("Success", "Question added successfully!")
                self.create_main_menu() # Refresh main menu to show new category
                add_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Could not save question: {e}")
        
        CustomButton(add_window, text="Save Question", command=save_question, font=STYLE["FONT_BODY"],
                     bg_color=STYLE["SUCCESS"], fg_color=STYLE["TEXT_LIGHT"], hover_color=STYLE["SUCCESS_HOVER"]).pack(pady=20)
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def get_default_questions(self):
        return {
            "Python Basics": {
                "questions": [
                    "What is the output of: print(2 ** 3)",
                    "Which keyword is used to define a function in Python?",
                    "What does len([1, 2, 3]) return?",
                    "Which of the following is a mutable data type?",
                    "What is the correct way to create a list?"
                ],
                "choices": [
                    ["6", "8", "9", "5"],
                    ["function", "def", "define", "func"],
                    ["2", "3", "4", "Error"],
                    ["tuple", "string", "list", "int"],
                    ["list = []", "list = ()", "list = {}", "All correct"]
                ],
                "answers": [1, 1, 1, 2, 0]
            },
            "Python Advanced": {
                "questions": [
                    "What is a lambda function?",
                    "Which module is used for regular expressions?",
                    "What does 'self' represent in a class?",
                    "Which decorator is used for static methods?",
                    "What is list comprehension?"
                ],
                "choices": [
                    ["Named function", "Anonymous function", "Class method", "Built-in function"],
                    ["regex", "re", "regexp", "regular"],
                    ["Class name", "Instance reference", "Method name", "Variable"],
                    ["@static", "@staticmethod", "@classmethod", "@property"],
                    ["Loop syntax", "Compact way to create lists", "Function type", "Class feature"]
                ],
                "answers": [1, 1, 1, 1, 1]
            }
        }

    def show_user_management_page(self):
        manage_window = tk.Toplevel(self.root)
        manage_window.title("Manage Admins")
        manage_window.geometry("500x400")
        manage_window.configure(bg=STYLE["BG"])
        manage_window.transient(self.root)
        manage_window.grab_set()

        tk.Label(manage_window, text="Manage Admin Roles", font=STYLE["FONT_HEADER"], bg=STYLE["BG"], fg=STYLE["TEXT"]).pack(pady=20)

        # Scrollable frame
        canvas = tk.Canvas(manage_window, bg=STYLE["BG"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(manage_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=STYLE["BG"])
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for username, data in sorted(self.users.items()):
            user_frame = tk.Frame(scrollable_frame, bg="#FFFFFF", relief="solid", bd=1)
            user_frame.pack(fill="x", padx=10, pady=4)

            role = data.get('role', 'user')
            label_text = f"{username} (Role: {role.capitalize()})"
            tk.Label(user_frame, text=label_text, bg="#FFFFFF", fg=STYLE["TEXT"], font=STYLE["FONT_BODY"]).pack(side="left", padx=10, pady=10)

            # Super admin cannot be demoted by themselves
            if username == self.current_user:
                continue

            if role == 'user':
                CustomButton(user_frame, text="Promote", command=lambda u=username: self._update_user_role(u, 'admin', manage_window),
                             font=("Arial", 10), padx=10, pady=5, radius=15,
                             bg_color=STYLE["SUCCESS"], fg_color=STYLE["TEXT_LIGHT"], hover_color=STYLE["SUCCESS_HOVER"]).pack(side="right", padx=10)
            else: # role == 'admin'
                CustomButton(user_frame, text="Demote", command=lambda u=username: self._update_user_role(u, 'user', manage_window),
                             font=("Arial", 10), padx=10, pady=5, radius=15,
                             bg_color=STYLE["DISABLED_BG"], fg_color=STYLE["TEXT_LIGHT"], hover_color=STYLE["DISABLED_HOVER"]).pack(side="right", padx=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add a button for the root admin to add new users
        add_user_btn_frame = tk.Frame(manage_window, bg=STYLE["BG"])
        add_user_btn_frame.pack(pady=10)
        CustomButton(add_user_btn_frame, text="Add New User", command=lambda: self._show_add_user_by_admin_page(manage_window),
                     font=("Arial", 11, "bold"), bg_color=STYLE["SUCCESS"], fg_color=STYLE["TEXT_LIGHT"], hover_color=STYLE["SUCCESS_HOVER"]).pack()

    def _update_user_role(self, username, new_role, window):
        if username in self.users:
            self.users[username]['role'] = new_role
            self._save_users()
            messagebox.showinfo("Success", f"User '{username}' has been updated to '{new_role}'.", parent=window)
            # Refresh the window
            window.destroy()
            self.show_user_management_page()
        else:
            messagebox.showerror("Error", f"User '{username}' not found.", parent=window)

    def _show_add_user_by_admin_page(self, parent_window):
        add_user_window = tk.Toplevel(self.root)
        add_user_window.title("Add New User")
        add_user_window.geometry("450x550")
        add_user_window.configure(bg=STYLE["BG"])
        add_user_window.resizable(False, False)
        add_user_window.transient(self.root)
        add_user_window.grab_set()

        tk.Label(add_user_window, text="Create Account", font=("Arial", 20, "bold"), bg=STYLE["BG"], fg=STYLE["TEXT"]).pack(pady=20)

        username_var = tk.StringVar()
        password_var = tk.StringVar()
        confirm_var = tk.StringVar()
        sq_var = tk.StringVar(value=SECURITY_QUESTIONS[0])
        sa_var = tk.StringVar()

        tk.Label(add_user_window, text="Username", font=STYLE["FONT_BODY"], bg=STYLE["BG"], fg=STYLE["TEXT"]).pack()
        tk.Entry(add_user_window, textvariable=username_var, font=STYLE["FONT_BODY"], width=30, relief="solid", bd=1).pack(pady=(5, 15))

        tk.Label(add_user_window, text="Password (min. 6 chars)", font=STYLE["FONT_BODY"], bg=STYLE["BG"], fg=STYLE["TEXT"]).pack()
        tk.Entry(add_user_window, textvariable=password_var, show="*", font=STYLE["FONT_BODY"], width=30, relief="solid", bd=1).pack(pady=5)

        tk.Label(add_user_window, text="Confirm Password", font=STYLE["FONT_BODY"], bg=STYLE["BG"], fg=STYLE["TEXT"]).pack()
        tk.Entry(add_user_window, textvariable=confirm_var, show="*", font=STYLE["FONT_BODY"], width=30, relief="solid", bd=1).pack(pady=5)

        tk.Label(add_user_window, text="Security Question", font=STYLE["FONT_BODY"], bg=STYLE["BG"], fg=STYLE["TEXT"]).pack(pady=(15, 5))
        ttk.Combobox(add_user_window, textvariable=sq_var, values=SECURITY_QUESTIONS, 
                     state="readonly", width=40, font=("Arial", 10)).pack()

        tk.Label(add_user_window, text="Security Answer", font=STYLE["FONT_BODY"], bg=STYLE["BG"], fg=STYLE["TEXT"]).pack(pady=(15, 5))
        tk.Entry(add_user_window, textvariable=sa_var, font=STYLE["FONT_BODY"], width=30, relief="solid", bd=1).pack(pady=5)

        CustomButton(add_user_window, text="CREATE USER", 
                     command=lambda: self._create_account_by_admin(username_var.get(), password_var.get(), confirm_var.get(), sq_var.get(), sa_var.get(), add_user_window, parent_window),
                     font=STYLE["FONT_BUTTON"], bg_color=STYLE["SUCCESS"], fg_color=STYLE["TEXT_LIGHT"], 
                     hover_color=STYLE["SUCCESS_HOVER"]).pack(pady=30)

    def _create_account_by_admin(self, username, password, confirm, sq_text, sa, add_user_window, manage_window):
        error_message = self._create_user_logic(username, password, confirm, sq_text, sa)
        if error_message:
            messagebox.showerror("Error", error_message, parent=add_user_window)
        else:
            messagebox.showinfo("Success", "User created successfully.", parent=add_user_window)
            # Destroy the 'add user' window and refresh the 'manage admins' window
            add_user_window.destroy()
            manage_window.destroy()
            self.show_user_management_page()

    def _show_forgot_password_flow(self):
        fp_window = tk.Toplevel(self.root)
        fp_window.title("Password Recovery")
        fp_window.geometry("450x350")
        fp_window.configure(bg=STYLE["BG"])
        fp_window.resizable(False, False)
        fp_window.transient(self.root)
        fp_window.grab_set()

        # --- Step 1: Enter Username ---
        frame1 = tk.Frame(fp_window, bg=STYLE["BG"])
        tk.Label(frame1, text="Enter Username", font=STYLE["FONT_HEADER"], bg=STYLE["BG"], fg=STYLE["TEXT"]).pack(pady=20)
        username_var = tk.StringVar()
        tk.Entry(frame1, textvariable=username_var, font=STYLE["FONT_BODY"], width=30, relief="solid", bd=1).pack(pady=10)
        CustomButton(frame1, text="Next", font=STYLE["FONT_BUTTON"], bg_color=STYLE["PRIMARY"], fg_color=STYLE["TEXT_LIGHT"], hover_color=STYLE["SECONDARY"],
                     command=lambda: self._handle_fp_step1(username_var.get(), fp_window, frame1, frame2, sq_label, sa_var)).pack(pady=20)

        # --- Step 2: Answer Security Question ---
        frame2 = tk.Frame(fp_window, bg=STYLE["BG"])
        sq_label = tk.Label(frame2, text="", font=STYLE["FONT_BODY"], bg=STYLE["BG"], fg=STYLE["TEXT"], wraplength=400)
        sq_label.pack(pady=20)
        sa_var = tk.StringVar()
        tk.Entry(frame2, textvariable=sa_var, font=STYLE["FONT_BODY"], width=30, relief="solid", bd=1).pack(pady=10)
        CustomButton(frame2, text="Submit", font=STYLE["FONT_BUTTON"], bg_color=STYLE["PRIMARY"], fg_color=STYLE["TEXT_LIGHT"], hover_color=STYLE["SECONDARY"],
                     command=lambda: self._handle_fp_step2(username_var.get(), sa_var.get(), fp_window, frame2, frame3)).pack(pady=20)

        # --- Step 3: Reset Password ---
        frame3 = tk.Frame(fp_window, bg=STYLE["BG"])
        tk.Label(frame3, text="Enter New Password", font=STYLE["FONT_HEADER"], bg=STYLE["BG"], fg=STYLE["TEXT"]).pack(pady=20)
        new_pass_var = tk.StringVar()
        confirm_pass_var = tk.StringVar()
        tk.Label(frame3, text="New Password", font=STYLE["FONT_BODY"], bg=STYLE["BG"], fg=STYLE["TEXT"]).pack()
        tk.Entry(frame3, textvariable=new_pass_var, show="*", font=STYLE["FONT_BODY"], width=30, relief="solid", bd=1).pack(pady=5)
        tk.Label(frame3, text="Confirm Password", font=STYLE["FONT_BODY"], bg=STYLE["BG"], fg=STYLE["TEXT"]).pack()
        tk.Entry(frame3, textvariable=confirm_pass_var, show="*", font=STYLE["FONT_BODY"], width=30, relief="solid", bd=1).pack(pady=5)
        CustomButton(frame3, text="Reset Password", font=STYLE["FONT_BUTTON"], bg_color=STYLE["SUCCESS"], fg_color=STYLE["TEXT_LIGHT"], hover_color=STYLE["SUCCESS_HOVER"],
                     command=lambda: self._handle_fp_step3(username_var.get(), new_pass_var.get(), confirm_pass_var.get(), fp_window)).pack(pady=20)

        # Initial state
        frame1.pack(fill="both", expand=True)

    def _handle_fp_step1(self, username, window, frame1, frame2, sq_label, sa_var):
        if not username:
            messagebox.showerror("Error", "Please enter a username.", parent=window)
            return

        user_data = self.users.get(username)
        if not user_data:
            messagebox.showerror("Error", "Username not found.", parent=window)
            return

        if "security_question_idx" not in user_data:
            messagebox.showinfo("Unavailable", "Password recovery is not set up for this account.", parent=window)
            window.destroy()
            return

        sq_idx = user_data["security_question_idx"]
        sq_label.config(text=SECURITY_QUESTIONS[sq_idx])
        sa_var.set("")

        frame1.pack_forget()
        frame2.pack(fill="both", expand=True)

    def _handle_fp_step2(self, username, answer, window, frame2, frame3):
        if not answer:
            messagebox.showerror("Error", "Please enter an answer.", parent=window)
            return

        user_data = self.users.get(username)
        stored_hash = user_data.get("security_answer_hash")
        answer_hash = hashlib.sha256(answer.lower().encode()).hexdigest()

        if stored_hash == answer_hash:
            frame2.pack_forget()
            frame3.pack(fill="both", expand=True)
        else:
            messagebox.showerror("Error", "Incorrect answer.", parent=window)

    def _handle_fp_step3(self, username, new_pass, confirm_pass, window):
        if not new_pass or not confirm_pass:
            messagebox.showerror("Error", "Please fill both password fields.", parent=window)
            return

        if new_pass != confirm_pass:
            messagebox.showerror("Error", "Passwords do not match.", parent=window)
            return

        if len(new_pass) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long.", parent=window)
            return

        new_pass_hash = hashlib.sha256(new_pass.encode()).hexdigest()
        self.users[username]["password"] = new_pass_hash
        self._save_users()

        messagebox.showinfo("Success", "Your password has been reset successfully. You can now log in.", parent=window)
        window.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = QuizApp()
    app.run()