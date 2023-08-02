#!/usr/bin/env python3
"""
Tic-Tac-Toe Game GUI using Tkinter

This script implements a simple Tic-Tac-Toe game using Tkinter for the graphical user interface.
Players can enter their names, and the game starts with a 3x3 grid. Players take turns placing
their symbols ('X' or 'O') on the board until one player wins or it's a draw.

Author: Lisan Eisinga
Date: 02-08-2023
"""

import time
import tkinter as tk


class TicTacToeGame:
    """
    A class to represent the Tic-Tac-Toe game and its graphical user interface.

    Attributes:
        board (List[List[str]]): The 3x3 board to store the game state.
        players (List[Dict]): A list of two player dictionaries containing their names and symbols ('X' or 'O').
        player_index (int): The index of the current player in the players list.
        game_over (bool): A flag indicating whether the game is over or not.
        ranking (Dict[str, int]): A dictionary to store the players' names and their number of wins.
    """

    def __init__(self):
        """Initialize the TicTacToeGame class and set up the main window."""
        self.ranking_window = None
        self.window_width = 300
        self.window_height = 450
        self.screen_width = None
        self.screen_height = None
        self.x_coordinate = None
        self.y_coordinate = None
        self.root = None
        self.start_frame = None
        self.board_frame = None
        self.board_labels = None
        self.player_names = None
        self.start_button = None
        self.player_label = None
        self.play_again_button = None
        self.reset_button = None
        self.ranking_button = None
        self.result_label = None
        self.players = None
        self.player_index = None
        self.game_over = None
        self.board = None
        self.ranking = {}

        self.initialize_window()
        self.create_widgets()
        self.root.mainloop()

    def initialize_window(self):
        """Initialize the main window and set its size and position."""
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe")
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.x_coordinate = (self.screen_width - self.window_width) // 2
        self.y_coordinate = (self.screen_height - self.window_height) // 2
        self.root.geometry(f"{self.window_width}x{self.window_height}+{self.x_coordinate}+{self.y_coordinate}")

    def create_widgets(self):
        """Create the widgets for the start frame and the board frame."""
        self.create_start_frame()
        self.create_board_frame()

    def create_start_frame(self):
        """Create the start frame with input fields for player names and buttons."""
        self.start_frame = tk.Frame(self.root)

        self.player_names = [tk.StringVar() for _ in range(2)]
        for i in range(2):
            tk.Label(self.start_frame, text=f"Player {i + 1} Name:").pack(pady=5)
            entry = tk.Entry(self.start_frame, textvariable=self.player_names[i])
            entry.pack(pady=5)

        self.start_button = tk.Button(self.start_frame, text="Start", command=self.start_game)
        self.start_button.pack(pady=10)

        self.ranking_button = tk.Button(self.start_frame, text="Ranking", command=self.show_ranking)
        self.ranking_button.pack(pady=5)

        self.start_frame.pack()

    def create_board_frame(self):
        """Create the board frame to display the game board and buttons for game actions."""
        self.board_frame = tk.Frame(self.root)
        self.board_labels = [[None for _ in range(3)] for _ in range(3)]

        for i in range(3):
            frame = tk.Frame(self.board_frame)
            frame.pack()
            for j in range(3):
                cell_label = tk.Button(frame, text='', font=('Courier', 20), width=4, height=2,
                                       command=lambda r=i, c=j: self.handle_move(r, c))
                cell_label.grid(row=i, column=j, padx=5, pady=5, sticky="n")
                self.board_labels[i][j] = cell_label

        self.player_label = tk.Label(self.board_frame, text="", font=('Helvetica', 12))
        self.player_label.pack(pady=10)

        self.play_again_button = tk.Button(self.board_frame, text="Play Again", command=self.switch_symbols)
        self.play_again_button.pack(pady=5)

        self.reset_button = tk.Button(self.board_frame, text="Reset", command=self.back_to_menu)
        self.reset_button.pack(pady=5)

        self.result_label = tk.Label(self.board_frame, text="", font=('Helvetica', 12))
        self.result_label.pack(pady=10)

    def start_game(self):
        """Start a new game with the names provided by the players."""
        player1_name = self.player_names[0].get()
        player2_name = self.player_names[1].get()

        if not player1_name:
            player1_name = "Lazy Daisy"
        if not player2_name:
            player2_name = "Snoozing Sally"

        self.players = [{'name': player1_name, 'symbol': 'X'}, {'name': player2_name, 'symbol': 'O'}]

        # If Player 2 has the 'X' symbol, switch the players
        if self.players[1]['symbol'] == 'X':
            self.players[0], self.players[1] = self.players[1], self.players[0]

        self.board = self.initialize_board()
        self.player_index = 0 if self.players[0]['symbol'] == 'X' else 1
        self.game_over = False

        self.update_board()
        self.player_label.config(text=f"Current Player: {self.players[self.player_index]['name']} "
                                      f"({self.players[self.player_index]['symbol']})")
        self.board_frame.pack()
        self.start_frame.pack_forget()

    @staticmethod
    def initialize_board():
        """Initialize the game board as an empty 3x3 matrix."""
        return [[' ' for _ in range(3)] for _ in range(3)]

    def update_board(self):
        """Update the game board UI with the current state of the board."""
        for i in range(3):
            for j in range(3):
                cell_label = self.board_labels[i][j]
                cell_label.config(text=self.board[i][j],
                                  state=tk.DISABLED if self.board[i][j] != ' ' or self.game_over else tk.NORMAL)
                if self.board[i][j] == 'X':
                    cell_label.config(fg="black", font=('Courier', 20, 'bold'))
                    cell_label.config(bg="green", disabledforeground="black")
                elif self.board[i][j] == 'O':
                    cell_label.config(fg="black", font=('Courier', 20, 'bold'))
                    cell_label.config(bg="red", disabledforeground="black")
                else:
                    cell_label.config(fg="black", font=('Courier', 20))
                    cell_label.config(bg="#f2f2f2", disabledforeground="black")
                    cell_label.config(highlightthickness=0)

    def animate_move(self, row, col):
        """Animate the move by updating the cell label's appearance."""
        symbol = self.players[self.player_index]['symbol']
        cell_label = self.board_labels[row][col]
        cell_label.config(text='', state=tk.DISABLED)
        if symbol == 'X':
            cell_label.config(bg="green", fg="black")
        elif symbol == 'O':
            cell_label.config(bg="red", fg="black")
        self.root.update()  # Update the window to show the new color
        time.sleep(0.01)  # Pause for a short time to create the animation effect
        cell_label.config(text=symbol, state=tk.NORMAL)

    def handle_move(self, row, col):
        """Handle a player's move and update the board accordingly."""
        if self.board[row][col] == ' ' and not self.game_over:
            self.board[row][col] = self.players[self.player_index]['symbol']
            self.animate_move(row, col)
            if self.check_winner(self.board, self.players[self.player_index]['symbol']):
                self.result_label.config(text=f"{self.players[self.player_index]['name']} wins!", fg="green")
                self.update_ranking(self.players[self.player_index]['name'])
                self.game_over = True
            elif all(self.board[i][j] != ' ' for i in range(3) for j in range(3)):
                self.result_label.config(text="It's a draw!", fg="blue")
                self.game_over = True
            else:
                self.player_index = (self.player_index + 1) % 2
                self.player_label.config(text=f"Current Player: {self.players[self.player_index]['name']} "
                                              f"({self.players[self.player_index]['symbol']})")

    @staticmethod
    def check_winner(board, player):
        """Check if a player has won the game."""
        for i in range(3):
            if all(board[i][j] == player for j in range(3)):
                return True
            if all(board[j][i] == player for j in range(3)):
                return True
        if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def update_ranking(self, player_name):
        """Update the ranking with the number of wins for each player."""
        if player_name in self.ranking:
            self.ranking[player_name] += 1
        else:
            self.ranking[player_name] = 1

    def clear_ranking(self):
        """Clear the ranking of players."""
        self.ranking = {}
        if 'ranking_window' in globals() and self.ranking_window.winfo_exists():
            self.ranking_window.destroy()

    def show_ranking(self):
        """Show the top 5 players and their wins in a separate window."""
        top_players = sorted(self.ranking.items(), key=lambda x: x[1], reverse=True)[:5]
        self.ranking_window = tk.Toplevel(self.root)
        self.ranking_window.title("Top 5 Players")
        self.ranking_window.geometry("200x200")
        tk.Label(self.ranking_window, text="Top 5 Players", font=('Helvetica', 12, 'bold')).pack(pady=5)
        for idx, (name, wins) in enumerate(top_players, start=1):
            win_plural = "wins" if wins > 1 else "win"
            tk.Label(self.ranking_window, text=f"{idx}. {name}: {wins} {win_plural}").pack(pady=2)

        if self.ranking:
            clear_button = tk.Button(self.ranking_window, text="Clear Ranking", command=self.clear_ranking)
            clear_button.pack(pady=5)

    def switch_symbols(self):
        """Switch player symbols and restart the game."""
        self.players[0]['symbol'], self.players[1]['symbol'] = self.players[1]['symbol'], self.players[0]['symbol']
        self.player_index = 1 if self.players[0]['symbol'] == 'O' else 0
        self.game_over = False
        self.restart_game()

    def restart_game(self):
        """Restart the game with the same players."""
        self.game_over = False
        for i in range(3):
            for j in range(3):
                self.board[i][j] = ' '
                self.board_labels[i][j].config(bg="#f2f2f2")
        self.update_board()
        self.result_label.config(text="")

    def back_to_menu(self):
        """Go back to the menu and show the start frame."""
        self.board_frame.pack_forget()
        self.start_frame.pack()
        self.result_label.config(text="")


if __name__ == "__main__":
    game = TicTacToeGame()
