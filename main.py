import tkinter as tk
from tkinter import messagebox
import random
import time

from authorisation import LoginWindow
from security import load_users, save_users


class NeuralGap:

    def __init__(self, root):

        self.root = root
        self.root.title("The Neural Gap")
        self.root.geometry("900x600")

        self.current_user = None

        LoginWindow(root, self.login_success)

    def login_success(self, username):

        self.current_user = username

        self.create_main_menu()

    def clear_window(self):

        for widget in self.root.winfo_children():
            widget.destroy()

    def create_main_menu(self):

        self.clear_window()

        title = tk.Label(
            self.root,
            text="The Neural Gap",
            font=("Arial", 26, "bold")
        )
        title.pack(pady=20)

        welcome = tk.Label(
            self.root,
            text=f"Welcome, {self.current_user}",
            font=("Arial", 14)
        )
        welcome.pack(pady=5)

        tk.Button(
            self.root,
            text="Reaction Time Test",
            width=30,
            height=2,
            command=self.open_reaction_test
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Sequence Memory Test",
            width=30,
            height=2,
            command=self.sequence_coming_soon
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Aim Tracking Test",
            width=30,
            height=2,
            command=self.aim_coming_soon
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="View Statistics",
            width=30,
            height=2,
            command=self.stats_coming_soon
        ).pack(pady=10)

    def sequence_coming_soon(self):

        messagebox.showinfo(
            "Coming Soon",
            "Sequence Memory Test will be added in Part 4."
        )

    def aim_coming_soon(self):

        messagebox.showinfo(
            "Coming Soon",
            "Aim Trainer will be added in Part 4."
        )

    def stats_coming_soon(self):

        messagebox.showinfo(
            "Coming Soon",
            "Statistics Dashboard will be added in Part 5."
        )
