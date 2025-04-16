import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from datetime import datetime

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe ❌⭕")
        self.current_player = "X"
        self.board = [""] * 9
        self.buttons = []
        self.player_x_score = 0
        self.player_o_score = 0
        self.draws = 0
        
        # Color scheme
        self.colors = {
            "bg": "#2E3440",
            "button_bg": "#3B4252",
            "button_fg": "#ECEFF4",
            "x_color": "#BF616A",  # Red
            "o_color": "#5E81AC",   # Blue
            "status_bg": "#3B4252",
            "status_fg": "#ECEFF4"
        }
        
        self.root.configure(bg=self.colors["bg"])
        self.load_scores()
        self.create_widgets()

    def load_scores(self):
        """Load scores from JSON file if exists"""
        if os.path.exists("tictactoe_scores.json"):
            with open("tictactoe_scores.json", "r") as f:
                scores = json.load(f)
                self.player_x_score = scores.get("player_x", 0)
                self.player_o_score = scores.get("player_o", 0)
                self.draws = scores.get("draws", 0)

    def save_scores(self):
        """Save scores to JSON file"""
        with open("tictactoe_scores.json", "w") as f:
            json.dump({
                "player_x": self.player_x_score,
                "player_o": self.player_o_score,
                "draws": self.draws,
                "last_played": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }, f, indent=4)

    def create_widgets(self):
        """Create game board and UI elements"""
        # Game board buttons
        for i in range(9):
            button = tk.Button(
                self.root, 
                text="", 
                font=("Arial", 32), 
                width=5, 
                height=2,
                bg=self.colors["button_bg"],
                fg=self.colors["button_fg"],
                activebackground=self.colors["bg"],
                command=lambda i=i: self.handle_click(i)
            )
            button.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(button)

        # Status label
        self.status_label = tk.Label(
            self.root, 
            text=f"Player X's Turn (X: {self.player_x_score} | O: {self.player_o_score} | Draws: {self.draws})",
            font=("Arial", 14),
            bg=self.colors["status_bg"],
            fg=self.colors["status_fg"]
        )
        self.status_label.grid(row=3, column=0, columnspan=3, pady=10)

        # Reset button
        reset_button = tk.Button(
            self.root,
            text="Reset Game",
            font=("Arial", 12),
            bg="#4C566A",
            fg="#ECEFF4",
            command=self.reset_game
        )
        reset_button.grid(row=4, column=0, columnspan=3, pady=5)

    def handle_click(self, index):
        """Handle player moves"""
        if self.board[index] == "":
            self.board[index] = self.current_player
            color = self.colors["x_color"] if self.current_player == "X" else self.colors["o_color"]
            self.buttons[index].config(text=self.current_player, fg=color, state="disabled")

            if self.check_winner(self.current_player):
                self.update_score(self.current_player)
                self.status_label.config(
                    text=f"Player {self.current_player} Wins! (X: {self.player_x_score} | O: {self.player_o_score} | Draws: {self.draws})"
                )
                messagebox.showinfo(
                    "Game Over", 
                    f"🎉 Player {self.current_player} wins!\n\nScores:\nX: {self.player_x_score}\nO: {self.player_o_score}\nDraws: {self.draws}"
                )
                self.disable_buttons()
            elif "" not in self.board:
                self.draws += 1
                self.save_scores()
                self.status_label.config(
                    text=f"It's a Draw! (X: {self.player_x_score} | O: {self.player_o_score} | Draws: {self.draws})"
                )
                messagebox.showinfo(
                    "Game Over", 
                    f"🤝 It's a draw!\n\nScores:\nX: {self.player_x_score}\nO: {self.player_o_score}\nDraws: {self.draws}"
                )
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.status_label.config(
                    text=f"Player {self.current_player}'s Turn (X: {self.player_x_score} | O: {self.player_o_score} | Draws: {self.draws})"
                )

    def update_score(self, player):
        """Update scores and save to file"""
        if player == "X":
            self.player_x_score += 1
        else:
            self.player_o_score += 1
        self.save_scores()

    def check_winner(self, player):
        """Check if current player has won"""
        wins = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6)              # diagonals
        ]
        return any(self.board[a] == self.board[b] == self.board[c] == player for a, b, c in wins)

    def disable_buttons(self):
        """Disable all buttons after game ends"""
        for button in self.buttons:
            button.config(state="disabled")

    def reset_game(self):
        """Reset the game board"""
        self.current_player = "X"
        self.board = [""] * 9
        for button in self.buttons:
            button.config(text="", state="normal", fg=self.colors["button_fg"])
        self.status_label.config(
            text=f"Player X's Turn (X: {self.player_x_score} | O: {self.player_o_score} | Draws: {self.draws})"
        )

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
