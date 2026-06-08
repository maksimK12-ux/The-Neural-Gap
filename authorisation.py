import tkinter as tk
from tkinter import messagebox

from security import (
    load_users,
    save_users,
    hash_password,
    verify_password
)


class LoginWindow:

    def __init__(self, root, login_success_callback):
        self.root = root
        self.login_success_callback = login_success_callback

        self.frame = tk.Frame(root, padx=30, pady=30)
        self.frame.pack(expand=True)

        title = tk.Label(
            self.frame,
            text="The Neural Gap",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=10)

        subtitle = tk.Label(
            self.frame,
            text="Reaction Time Analysis Platform",
            font=("Arial", 10)
        )
        subtitle.pack(pady=5)

        tk.Label(self.frame, text="Username").pack()

        self.username_entry = tk.Entry(
            self.frame,
            width=30
        )
        self.username_entry.pack(pady=5)

        tk.Label(self.frame, text="Password").pack()

        self.password_entry = tk.Entry(
            self.frame,
            width=30,
            show="*"
        )
        self.password_entry.pack(pady=5)

        tk.Button(
            self.frame,
            text="Login",
            width=20,
            command=self.login
        ).pack(pady=5)

        tk.Button(
            self.frame,
            text="Register",
            width=20,
            command=self.register
        ).pack(pady=5)

    def login(self):

        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        users = load_users()

        if username not in users:
            messagebox.showerror(
                "Login Failed",
                "Account does not exist."
            )
            return

        user = users[username]

        if verify_password(
            user["password"],
            user["salt"],
            password
        ):

            messagebox.showinfo(
                "Success",
                f"Welcome back, {username}!"
            )

            self.frame.destroy()

            self.login_success_callback(username)

        else:
            messagebox.showerror(
                "Login Failed",
                "Incorrect password."
            )

    def register(self):

        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if len(username) < 3:
            messagebox.showerror(
                "Invalid Username",
                "Username must be at least 3 characters."
            )
            return

        if len(password) < 6:
            messagebox.showerror(
                "Weak Password",
                "Password must be at least 6 characters."
            )
            return

        users = load_users()

        if username in users:
            messagebox.showerror(
                "Registration Failed",
                "Username already exists."
            )
            return

        hashed_password, salt = hash_password(password)

        users[username] = {
            "password": hashed_password,
            "salt": salt,
            "results": {
                "reaction_test": [],
                "sequence_memory": [],
                "aim_trainer": []
            }
        }

        save_users(users)

        messagebox.showinfo(
            "Success",
            "Account created successfully."
        )

        self.password_entry.delete(0, tk.END)