import subprocess
import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk


class ScoreManager:
    def __init__(self, filename="scores.json"):
        self.filename = filename
        self.scores = self.load_scores()

    def load_scores(self):
        if not os.path.exists(self.filename):
            return {}
        with open(self.filename, "r") as f:
            return json.load(f)

    def save_scores(self):
        with open(self.filename, "w") as f:
            json.dump(self.scores, f, indent=4)

    def add_score(self, game_name, score):
        game_scores = self.scores.setdefault(game_name, {
            "scores": [],
            "total_plays": 0,
            "average_score": 0,
            "high_score": 0,
            "last_played": ""
        })

        game_scores["scores"].append(score)
        game_scores["total_plays"] += 1
        game_scores["average_score"] = sum(game_scores["scores"]) / len(game_scores["scores"])
        game_scores["high_score"] = max(game_scores["scores"])
        game_scores["last_played"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.save_scores()

    def get_stats(self):
        return self.scores


class GameArcade:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Game Arcade 🎮")
        self.root.geometry("800x600")
        self.root.configure(bg="#2E3440")

        self.load_icons()
        self.score_manager = ScoreManager()
        self.create_widgets()
        self.center_window()

    def load_icons(self):
        try:
            self.icons = {
                "memory": self.create_placeholder_icon("#4C566A"),
                "guessing": self.create_placeholder_icon("#5E81AC"),
                "tictactoe": self.create_placeholder_icon("#BF616A"),
                "pong": self.create_placeholder_icon("#88C0D0"),
                "stats": self.create_placeholder_icon("#A3BE8C"),
                "exit": self.create_placeholder_icon("#D08770")
            }
        except:
            self.icons = {}

    def create_placeholder_icon(self, color):
        img = Image.new('RGB', (100, 100), color)
        return ImageTk.PhotoImage(img)

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        header_frame = tk.Frame(self.root, bg="#3B4252")
        header_frame.pack(fill="x", padx=20, pady=20)

        tk.Label(
            header_frame,
            text="PYTHON GAME ARCADE",
            font=("Arial", 24, "bold"),
            fg="#ECEFF4",
            bg="#3B4252"
        ).pack(pady=10)

        menu_frame = tk.Frame(self.root, bg="#2E3440")
        menu_frame.pack(expand=True, fill="both", padx=50, pady=20)

        games = [
            ("Memory Match", "memory", self.launch_memory),
            ("Number Guessing", "guessing", self.launch_guessing),
            ("Tic-Tac-Toe", "tictactoe", self.launch_tictactoe),
            ("Pong", "pong", self.launch_pong),
            ("Statistics", "stats", self.show_stats),
            ("Exit", "exit", self.exit_app)
        ]

        for i, (text, icon_key, command) in enumerate(games):
            btn = tk.Button(
                menu_frame,
                text=text,
                image=self.icons.get(icon_key),
                compound="top",
                font=("Arial", 14),
                bg="#4C566A",
                fg="#ECEFF4",
                activebackground="#3B4252",
                activeforeground="#ECEFF4",
                borderwidth=0,
                padx=20,
                pady=10,
                command=command
            )
            btn.grid(row=i // 3, column=i % 3, padx=15, pady=15, sticky="nsew")
            menu_frame.grid_columnconfigure(i % 3, weight=1)

        menu_frame.grid_rowconfigure(0, weight=1)
        menu_frame.grid_rowconfigure(1, weight=1)

        self.status_bar = tk.Label(
            self.root,
            text="Welcome to Python Game Arcade!",
            bd=1,
            relief="sunken",
            anchor="w",
            font=("Arial", 10),
            bg="#3B4252",
            fg="#D8DEE9"
        )
        self.status_bar.pack(fill="x", padx=20, pady=(0, 20))

    def launch_game(self, filename, game_name):
        self.update_status(f"Launching {game_name}...")
        try:
            result = subprocess.run(["python", filename], capture_output=True, text=True)
            if result.returncode == 0:
                # Extract score from game output if sent as a single integer
                try:
                    score = int(result.stdout.strip())
                except:
                    score = 0
                self.score_manager.add_score(game_name, score)
                self.update_status(f"{game_name} completed! Score: {score}")
            else:
                messagebox.showerror("Error", f"{game_name} failed to launch")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch {game_name}:\n{str(e)}")

    def launch_memory(self):
        self.launch_game("memory_game.py", "MemoryMatch")

    def launch_guessing(self):
        self.launch_game("number_guess.py", "Number Guessing")

    def launch_tictactoe(self):
        self.launch_game("tictactoe.py", "TicTacToe")

    def launch_pong(self):
        self.launch_game("pong_game.py", "Pong")

    def show_stats(self):
        stats = self.score_manager.get_stats()
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Game Statistics")
        stats_window.geometry("600x400")
        stats_window.configure(bg="#2E3440")

        tree = ttk.Treeview(stats_window, columns=("Metric", "Value"), show="headings")
        tree.heading("Metric", text="Metric")
        tree.heading("Value", text="Value")
        tree.column("Metric", width=300)
        tree.column("Value", width=200)

        for game, data in stats.items():
            if not data:
                continue
            tree.insert("", "end", values=(f"{game.upper()} STATISTICS", ""))
            tree.insert("", "end", values=("Total plays", data["total_plays"]))
            tree.insert("", "end", values=("Average score", f"{data['average_score']:.1f}"))
            tree.insert("", "end", values=("High score", data["high_score"]))
            tree.insert("", "end", values=("Last played", data["last_played"]))
            tree.insert("", "end", values=("", ""))

        tree.pack(expand=True, fill="both", padx=20, pady=20)

        stats_window.update_idletasks()
        width = stats_window.winfo_width()
        height = stats_window.winfo_height()
        x = (stats_window.winfo_screenwidth() // 2) - (width // 2)
        y = (stats_window.winfo_screenheight() // 2) - (height // 2)
        stats_window.geometry(f'{width}x{height}+{x}+{y}')

    def exit_app(self):
        if messagebox.askyesno("Exit Game Arcade", "Are you sure you want to exit?\nYour session will be saved."):
            self.root.destroy()

    def update_status(self, message):
        self.status_bar.config(text=message)
        self.root.update_idletasks()


if __name__ == "__main__":
    root = tk.Tk()
    app = GameArcade(root)
    root.mainloop()
