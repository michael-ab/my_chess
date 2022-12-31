import sys
import chess
import my_board_2
import tkinter as tk

if __name__ == '__main__':

    # Set up the board
    board = chess.Board()

    root = tk.Tk()
    gui_board = my_board_2.ChessBoard(root)
    gui_board.pack(side="top", fill="both", expand="true", padx=4, pady=4)

    gui_board.add_all_pieces()

    # run the Tk event loop

    while not board.is_game_over():
        start = input("Enter the start piece coordinate: ")
        end = input("Enter the end piece coordinate: ")

        # try:
        board.push_uci(start+end)
        gui_board.movepiece(start,end)
        print(board)
        # except:
        #         print("Error")


    result = board.result()
    print("Game over. Result: " + result)

    root.mainloop()