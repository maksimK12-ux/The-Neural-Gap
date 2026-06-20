import tkinter as tk
from tkinter import messagebox
import random
import time
from tests import SequenceMemoryTest, AimTrainer

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
            command=self.open_sequence_test
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Aim Tracking Test",
            width=30,
            height=2,
            command=self.open_aim_test
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="View Statistics",
            width=30,
            height=2,
            command=self.stats_coming_soon
        ).pack(pady=10)

    def open_sequence_test(self):

        self.clear_window()

        SequenceMemoryTest(
            self.root,
            self.current_user,
            self.create_main_menu
        )

    def open_aim_test(self):

        self.clear_window()

        AimTrainer(
            self.root,
            self.current_user,
            self.create_main_menu
        )

    def stats_coming_soon(self):

        messagebox.showinfo(
            "Coming Soon",
            "Statistics Dashboard will be added in Part 5."
        )


    def open_reaction_test(self):

        self.clear_window()

        self.waiting_for_click = False

        self.reaction_frame = tk.Frame(self.root)
        self.reaction_frame.pack(expand=True)

        title = tk.Label(
            self.reaction_frame,
            text="Reaction Time Test",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=20)

        self.instructions = tk.Label(
            self.reaction_frame,
            text="Press Start and wait for GREEN.",
            font=("Arial", 14)
        )
        self.instructions.pack(pady=10)

        self.reaction_button = tk.Button(
            self.reaction_frame,
            text="START",
            width=25,
            height=5,
            bg="lightgrey",
            command=self.start_reaction_round
        )

        self.reaction_button.pack(pady=20)

        tk.Button(
            self.reaction_frame,
            text="Back",
            command=self.create_main_menu
        ).pack(pady=10)

    def start_reaction_round(self):

        self.reaction_button.config(
            text="WAIT...",
            bg="red",
            command=self.clicked_too_early
        )

        delay = random.randint(2000, 5000)

        self.root.after(
            delay,
            self.turn_green
        )

    def clicked_too_early(self):

        messagebox.showwarning(
            "Too Early!",
            "You clicked before the signal."
        )

        self.open_reaction_test()

    def turn_green(self):

        self.waiting_for_click = True

        self.start_time = time.time()

        self.reaction_button.config(
            text="CLICK!",
            bg="green",
            command=self.record_reaction
        )

    def record_reaction(self):

        if not self.waiting_for_click:
            return

        reaction_time = (
            time.time() - self.start_time
        ) * 1000

        self.save_reaction_result(
            round(reaction_time, 2)
        )

        messagebox.showinfo(
            "Result",
            f"Reaction Time:\n\n{round(reaction_time,2)} ms"
        )

        self.open_reaction_test()

    def save_reaction_result(self, score):

        users = load_users()

        users[self.current_user]["results"][
            "reaction_test"
        ].append(score)

        save_users(users)


if __name__ == "__main__":

    root = tk.Tk()

    app = NeuralGap(root)

    root.mainloop()


