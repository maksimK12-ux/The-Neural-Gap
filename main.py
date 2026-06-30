import tkinter as tk
from tkinter import messagebox
import random
import time
from tests import SequenceMemoryTest, AimTrainer

from authorisation import LoginWindow
from security import load_users, save_users
from results import AnalyticsDashboard


class NeuralGap:

    def __init__(self, root):

        self.root = root
        self.root.title("The Neural Gap")
        self.root.geometry("900x600")
        self.root.configure(bg="white")

        self.current_user = None  # Stores the username of whoever logs in successfully

        LoginWindow(root, self.login_success)  # Opens the login window and waits until login succeeds

    def login_success(self, username):

        self.current_user = username

        self.create_main_menu()

    def clear_window(self):

        for widget in self.root.winfo_children(): # Removes every widget currently on the screen so a new page can be loaded
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
            command=self.open_statistics
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Settings",
            width=30,
            height=2,
            command=self.show_settings
        ).pack(side="bottom", pady=20)

    def show_settings(self):

        messagebox.showinfo(
            "Settings",
            """
How the program works:

Reaction Time Test:
Press Start, wait for green, then click as fast as possible.

Sequence Memory Test:
Watch the highlighted squares, then repeat the pattern.

Aim Tracking Test:
Press Start, then click 10 red targets as fast as possible.

Statistics:
Your results are saved to your account and used for averages, best scores, and progress charts.
"""
        )

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

    def open_statistics(self):

        self.clear_window()

        AnalyticsDashboard(
            self.root,
            self.current_user,
            self.create_main_menu
        )


    def open_reaction_test(self):

        self.clear_window()

        self.waiting_for_click = False  # Used to check whether the user clicked before the green signal

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

        self.reaction_button.config( # Changes the button while the player waits for the random signal
            text="WAIT...",
            bg="red",
            command=self.clicked_too_early
        )

        delay = random.randint(2000, 5000)

        self.root.after( # Runs turn_green() after the random delay has finished
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

        self.waiting_for_click = True   # Starts timing as soon as the signal appears

        self.start_time = time.time()

        self.reaction_button.config(
            text="CLICK!",
            bg="green",
            command=self.record_reaction
        )

    def record_reaction(self):

        if not self.waiting_for_click:  # Prevents invalid clicks from being recorded
            return

        reaction_time = (  # Calculates the reaction time in milliseconds
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

        users = load_users() # Loads the current user data from the JSON file

        users[self.current_user]["results"][  # Adds the new reaction time to the user's list of results
            "reaction_test"
        ].append(score)

        save_users(users) # Saves the updated data back to the JSON file


if __name__ == "__main__":

    root = tk.Tk() # Creates the main Tkinter window and starts the program

    app = NeuralGap(root)

    root.mainloop()


