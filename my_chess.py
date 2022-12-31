import sys
import chess
from PyQt5.QtWidgets import QApplication
import my_board

if __name__ == '__main__':

    # Set up the board
    board = chess.Board()
    app = QApplication(sys.argv)
    chess_board = my_board.ChessBoard()
    chess_board.showBoard()

    while not board.is_game_over():
        start = input("Enter the start piece coordinate: ")
        end = input("Enter the end piece coordinate: ")


        # board.push_uci(start+end)
        chess_board.move_piece(start, end)
        chess_board.showBoard()
        # print(board)
        # except:
        #     print("Error")


    result = board.result()
    print("Game over. Result: " + result)
    sys.exit(app.exec_())