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

        users = load_users() # Loads the logged-in user's saved test results

        return users[self.username]["results"]

    def average(self, values):

        if not values: # Prevents an error if no results have been recorded
            return 0

        return round(statistics.mean(values), 2)

    def best(self, values):

        if not values: # Returns 0 if there are no recorded results
            return 0

        return min(values) # Lower reaction/aim times are considered better

    def show_statistics(self):

        data = self.get_results()

        reaction_avg = self.average( # Calculates averages and best scores for each test
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

        aim_best = self.best(
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

Best Aim Completion Time:
{aim_best} ms

Total Tests Completed:
{len(data['reaction_test']) + len(data['sequence_memory']) + len(data['aim_trainer'])}
"""
        )

    def reaction_age(self):

        data = self.get_results()

        if not data["reaction_test"]: # Stops the analysis if the user has not completed a reaction test

            messagebox.showinfo(
                "Reaction Age",
                "No reaction data available."
            )
            return

        avg = self.average(
            data["reaction_test"]
        )
          # Estimates a reaction age based on the average reaction time
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

        chart_data = { # Stores all available test data for graphing
            "Reaction Time (ms)": data["reaction_test"],
            "Sequence Memory": data["sequence_memory"],
            "Aim Time (ms)": data["aim_trainer"]
        }

        chart_data = { # Removes any tests that do not yet have results
            name: scores
            for name, scores in chart_data.items()
            if scores
        }

        if not chart_data:

            messagebox.showinfo(
                "Graph",
                "Complete at least 1 reaction tests."
            )
            return

        plt.figure(figsize=(8, 5))

        for label, scores in chart_data.items(): # Draws a line for each completed test type

            plt.plot(
                range(1, len(scores) + 1),
                scores,
                marker="o",
                label=label
            )

        plt.title("Test Progress")

        plt.xlabel("Attempt")

        plt.ylabel("Score/Milliseconds")

        plt.grid(True)

        plt.legend()

        plt.show() # Displays the completed graph in a new window

    def export_results(self):

        users = load_users()

        save_path = filedialog.asksaveasfilename(  # Allows the user to choose where to save their exported results
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")]
        )

        if not save_path:
            return

        with open(save_path, "w") as file:  # Writes the user's data to a new JSON file

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

        self.frame.destroy() # Closes the analytics page and returns to the main menu

        self.return_callback()