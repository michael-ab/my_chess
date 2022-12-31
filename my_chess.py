import sys
import chess
import my_board_2
import tkinter as tk

if __name__ == '__main__':

    # Set up the board
    board = chess.Board()

    root = tk.Tk()
    root.title("Chess Game")
    root.iconbitmap("chess.ico")
    gui_board = my_board_2.ChessBoard(root, board)
    gui_board.pack(side="top", fill="both", expand="true", padx=4, pady=4)

    gui_board.add_all_pieces()

    root.mainloop()