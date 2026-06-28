import tkinter as tk
from tkinter import messagebox
import random
import time

from authorisation import load_users, save_users

class SequenceMemoryTest:

    def __init__(self, root, username, return_callback):

        self.root = root
        self.username = username
        self.return_callback = return_callback
        
        self.sequence = []
        self.user_sequence = []
        self.level = 1

        self.frame = tk.Frame(root)
        self.frame.pack(expand=True, fill="both")

        tk.Label(
            self.frame,
            text="Sequence Memory Test",
            font=("Arial", 22, "bold")
        ).pack(pady=10)

        self.info_label = tk.Label(
            self.frame,
            text="Remember the sequence.",
            font=("Arial", 14)
        )
        self.info_label.pack()

        self.grid_frame = tk.Frame(self.frame)
        self.grid_frame.pack(pady=20)

        self.buttons = []

        for row in range(3):
            for col in range(3):

                btn = tk.Label(
                    self.grid_frame,
                    width=10,
                    height=4,
                    bg="lightgrey",
                    relief="raised",
                    bd=2,
                    cursor="hand2"
                )

                btn.grid(row=row, column=col, padx=5, pady=5)
                btn.bind(
                    "<Button-1>",
                    lambda event, i=len(self.buttons):
                    self.user_click(i)
                )

                self.buttons.append(btn)

        tk.Button(
            self.frame,
            text="Start",
            command=self.start_game
        ).pack(pady=10)

        tk.Button(
            self.frame,
            text="Back",
            command=self.close_test
        ).pack()

    def start_game(self):

        self.sequence.append(
            random.randint(0, 8)
        )

        self.user_sequence = []

        self.show_sequence()

    def show_sequence(self):

        self.info_label.config(
            text=f"Level {self.level}"
        )

        delay = 500

        for position in self.sequence:

            self.root.after(
                delay,
                lambda p=position:
                self.highlight_button(p)
            )

            delay += 800

        self.root.after(
            delay,
            self.enable_input
        )

    def highlight_button(self, index):

        self.buttons[index].config(bg="yellow")

        self.root.after(
            500,
            lambda:
            self.buttons[index].config(
                bg="lightgrey"
            )
        )

    def enable_input(self):

        self.info_label.config(
            text="Repeat the pattern."
        )

    def user_click(self, index):

        self.user_sequence.append(index)

        current = len(self.user_sequence) - 1

        if self.user_sequence[current] != self.sequence[current]:

            self.end_game()
            return

        if len(self.user_sequence) == len(self.sequence):

            self.level += 1

            self.root.after(
                800,
                self.start_game
            )

    def end_game(self):

        score = self.level - 1

        users = load_users()

        users[self.username]["results"][
            "sequence_memory"
        ].append(score)

        save_users(users)

        messagebox.showinfo(
            "Game Over",
            f"Sequence Score: {score}"
        )

        self.close_test()

    def close_test(self):

        self.frame.destroy()

        self.return_callback()


class AimTrainer:

    def __init__(self, root, username, return_callback):

        self.root = root
        self.username = username
        self.return_callback = return_callback

        self.targets_hit = 0
        self.max_targets = 10
        self.target_size = 60
        self.start_time = None

        self.frame = tk.Frame(root)
        self.frame.pack(expand=True, fill="both")

        tk.Label(
            self.frame,
            text="Aim Trainer",
            font=("Arial", 22, "bold")
        ).pack(pady=10)

        self.info_label = tk.Label(
            self.frame,
            text="Press Start to begin.",
            font=("Arial", 14)
        )
        self.info_label.pack()

        self.canvas = tk.Canvas(
            self.frame,
            width=800,
            height=450,
            bg="white"
        )

        self.canvas.pack()

        self.start_button = tk.Button(
            self.frame,
            text="Start",
            width=20,
            command=self.start_test
        )
        self.start_button.pack(pady=10)

        tk.Button(
            self.frame,
            text="Back",
            width=20,
            command=self.close_test
        ).pack()

    def start_test(self):

        self.targets_hit = 0
        self.start_time = time.perf_counter()

        self.start_button.config(state=tk.DISABLED)

        self.info_label.config(
            text=f"Targets hit: 0/{self.max_targets}"
        )

        self.spawn_target()

    def spawn_target(self):

        self.canvas.delete("all")

        if self.targets_hit >= self.max_targets:

            self.finish_test()
            return

        x = random.randint(50, 750 - self.target_size)
        y = random.randint(50, 400 - self.target_size)

        self.target = self.canvas.create_oval(
            x,
            y,
            x + self.target_size,
            y + self.target_size,
            fill="red"
        )

        self.canvas.tag_bind(
            self.target,
            "<Button-1>",
            self.hit_target
        )

    def hit_target(self, event):

        if self.start_time is None:
            return

        self.targets_hit += 1

        self.info_label.config(
            text=f"Targets hit: {self.targets_hit}/{self.max_targets}"
        )

        self.spawn_target()

    def finish_test(self):

        if self.start_time is None:
            return

        total_time = round(
            (time.perf_counter() - self.start_time) * 1000,
            2
        )

        self.start_time = None

        users = load_users()

        users[self.username]["results"][
            "aim_trainer"
        ].append(total_time)

        save_users(users)

        messagebox.showinfo(
            "Finished",
            f"Aim Time:\n{total_time} ms"
        )

        self.close_test()

    def close_test(self):

        self.frame.destroy()

        self.return_callback()
