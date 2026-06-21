import tkinter as tk
from tkinter import messagebox, filedialog
import statistics
import json

import matplotlib.pyplot as plt

from authorisation import load_users


class AnalyticsDashboard:

    def __init__(self, root, username, return_callback):

        self.root = root
        self.username = username
        self.return_callback = return_callback

        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        tk.Label(
            self.frame,
            text="Performance Analytics",
            font=("Arial", 22, "bold")
        ).pack(pady=15)

        tk.Button(
            self.frame,
            text="Statistics",
            width=30,
            command=self.show_statistics
        ).pack(pady=5)

        tk.Button(
            self.frame,
            text="Reaction Age Analysis",
            width=30,
            command=self.reaction_age
        ).pack(pady=5)

        tk.Button(
            self.frame,
            text="Progress Chart",
            width=30,
            command=self.show_graph
        ).pack(pady=5)

        tk.Button(
            self.frame,
            text="Export Results",
            width=30,
            command=self.export_results
        ).pack(pady=5)

        tk.Button(
            self.frame,
            text="Back",
            width=30,
            command=self.close_dashboard
        ).pack(pady=15)

    def get_results(self):

        users = load_users()

        return users[self.username]["results"]

    def average(self, values):

        if not values:
            return 0

        return round(statistics.mean(values), 2)

    def best(self, values):

        if not values:
            return 0

        return min(values)

    def show_statistics(self):

        data = self.get_results()

        reaction_avg = self.average(
            data["reaction_test"]
        )

        reaction_best = self.best(
            data["reaction_test"]
        )

        memory_avg = self.average(
            data["sequence_memory"]
        )

        aim_avg = self.average(
            data["aim_trainer"]
        )

        messagebox.showinfo(
            "Detailed Statistics",
            f"""
Reaction Average:
{reaction_avg} ms

Best Reaction:
{reaction_best} ms

Memory Average:
{memory_avg}

Aim Average:
{aim_avg} ms

Total Tests Completed:
{len(data['reaction_test']) + len(data['sequence_memory']) + len(data['aim_trainer'])}
"""
        )

    def reaction_age(self):

        data = self.get_results()

        if not data["reaction_test"]:

            messagebox.showinfo(
                "Reaction Age",
                "No reaction data available."
            )
            return

        avg = self.average(
            data["reaction_test"]
        )

        if avg < 200:
            age = "15-20 years"
        elif avg < 250:
            age = "20-30 years"
        elif avg < 300:
            age = "30-45 years"
        elif avg < 350:
            age = "45-60 years"
        else:
            age = "60+ years"

        messagebox.showinfo(
            "Reaction Age Analysis",
            f"""
Average Reaction Time:
{avg} ms

Estimated Reaction Age:
{age}
"""
        )

    def show_graph(self):

        data = self.get_results()

        reaction_scores = data["reaction_test"]

        if len(reaction_scores) < 2:

            messagebox.showinfo(
                "Graph",
                "Complete at least 2 reaction tests."
            )
            return

        plt.figure(figsize=(8, 5))

        plt.plot(
            range(1, len(reaction_scores)+1),
            reaction_scores,
            marker="o"
        )

        plt.title("Reaction Time Progress")

        plt.xlabel("Attempt")

        plt.ylabel("Milliseconds")

        plt.grid(True)

        plt.show()

    def export_results(self):

        users = load_users()

        save_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")]
        )

        if not save_path:
            return

        with open(save_path, "w") as file:

            json.dump(
                users[self.username],
                file,
                indent=4
            )

        messagebox.showinfo(
            "Export Complete",
            "Results successfully exported."
        )

    def close_dashboard(self):

        self.frame.destroy()

        self.return_callback()