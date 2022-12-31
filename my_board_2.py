import tkinter as tk
import os
import pprint
import math
import chess

class ChessBoard(tk.Frame):
    def __init__(self, parent, logic_board, rows=8, columns=8, size=100, color1="white", color2="gray"):
        '''size is the size of a square, in pixels'''

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.pieces = {}
        self.board = [[0]* self.columns for i in range (self.rows)]
        self.logic_board = logic_board
        canvas_width = columns * size
        canvas_height = rows * size

        self.num2let = {
            0: "a",
            1: "b",
            2: "c",
            3: "d",
            4: "e",
            5: "f",
            6: "g",
            7: "h"
        }

        self.images = {
            "pawn_white": tk.PhotoImage(file='.\pieces\pw.png'),
            "knight_white": tk.PhotoImage(file='.\pieces\knw.png'),
            "bishop_white": tk.PhotoImage(file='.\pieces\\bw.png'),
            "rook_white": tk.PhotoImage(file='.\pieces\\rw.png'),
            "queen_white": tk.PhotoImage(file='.\pieces\qw.png'),
            "king_white": tk.PhotoImage(file='.\pieces\kw.png'),
            "pawn_black": tk.PhotoImage(file='.\pieces\pb.png'),
            "knight_black": tk.PhotoImage(file='.\pieces\knb.png'),
            "bishop_black": tk.PhotoImage(file='.\pieces\\bb.png'),
            "rook_black": tk.PhotoImage(file='.\pieces\\rb.png'),
            "queen_black": tk.PhotoImage(file='.\pieces\qb.png'),
            "king_black": tk.PhotoImage(file='.\pieces\kb.png'),
        }
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        # this binding will cause a refresh if the user interactively
        # changes the window size
        self.canvas.bind("<Configure>", self.refresh)

        # bind events to the canvas
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)

        # data field for the selected square
        self.selected_square = None

    def on_button_press(self, event):
        # highlight the clicked square
        x, y = (event.x, event.y)
        row, col = self.get_square_at_point(x, y)
        self.select_square(row, col)

    def select_square(self, row, col):
        if not self.selected_square:
            if self.board[row][col]:
                self.draw_square(row, col, "yellow")
                self.selected_square = [row, col]
                self.canvas.tag_raise("piece")
            return

        try:
            self.logic_board.push_uci(self.num2let[self.selected_square[1]]+str(self.selected_square[0] + 1)+self.num2let[col]+str(row + 1))
            self.canvas.delete("square_color")
            self.movepiece(self.num2let[self.selected_square[1]]+str(self.selected_square[0] + 1), self.num2let[col]+str(row + 1), promote=False)
            self.selected_square = None
        except:
            if chess.Move.from_uci(self.num2let[self.selected_square[1]]+str(self.selected_square[0] + 1)+self.num2let[col]+str(row + 1) + "q") in self.logic_board.legal_moves:
                self.logic_board.push_uci(self.num2let[self.selected_square[1]]+str(self.selected_square[0] + 1)+self.num2let[col]+str(row + 1) + "q")
                self.movepiece(self.num2let[self.selected_square[1]]+str(self.selected_square[0] + 1), self.num2let[col]+str(row + 1), promote=True)
            print("Move error - Retry")
            self.canvas.delete("square_color")
            self.selected_square = None

    def get_square_at_point(self, x, y):
        # calculate the row and column of the square at the given point
        row = int(math.floor(y / self.size))
        col = int(math.floor(x / self.size))
        return row, col

    def draw_square(self, row, col, color):
            # calculate the coordinates of the top-left corner of the square
            x0 = col * self.size
            y0 = row * self.size
            x1 = x0 + self.size
            y1 = y0 + self.size

            # draw the square
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black", tags="square_color")

    def addpiece(self, name, image, row=0, column=0):
        '''Add a piece to the playing board'''
        self.canvas.create_image(0,0, image=image, tags=(name, "piece"), anchor="c")
        self.placepiece(name, row, column)

    def placepiece(self, name, row, column):
        '''Place a piece at the given row/column'''
        self.pieces[name] = (row, column)
        self.board[row][column] = name
        x0 = (column * self.size) + int(self.size/2)
        y0 = (row * self.size) + int(self.size/2)
        self.canvas.coords(name, x0, y0)

    def remove_piece(self, name):
        # remove the piece from the board
        self.canvas.delete(name)

        # remove the piece from the pieces dictionary
        del self.pieces[name]

    def movepiece(self, start, end, promote=False):

        let2num = {
            "A":1,
            "a":1,
            "B":2,
            "b":2,
            "C":3,
            "c":3,
            "D":4,
            "d":4,
            "E":5,
            "e":5,
            "F":6,
            "f":6,
            "G":7,
            "g":7,
            "H":8,
            "h":8,
        }

        name = self.board[int(start[1])-1][let2num[start[0]]-1]
        self.board[int(start[1])-1][let2num[start[0]]-1] = 0
        self.remove_piece(name)
        pieceToRemove = None

        if self.board[int(end[1])-1][let2num[end[0]]-1]:
            pieceToRemove = self.board[int(end[1])-1][let2num[end[0]]-1]
            self.board[int(end[1])-1][let2num[end[0]]-1] = 0
            self.remove_piece(pieceToRemove)

        if (name == "king_black1") and (pieceToRemove == "rook_black1"):
           self.addpiece(name, self.images[name[:-1]], int(start[1])-1, let2num[start[0]]-3)
           self.addpiece(pieceToRemove, self.images[pieceToRemove[:-1]], int(start[1])-1, let2num[start[0]]-2)
        elif (name == "king_black1") and (pieceToRemove == "rook_black2"):
           self.addpiece(name, self.images[name[:-1]], int(start[1])-1, let2num[start[0]]+1)
           self.addpiece(pieceToRemove, self.images[pieceToRemove[:-1]], int(start[1])-1, let2num[start[0]])
        elif (name == "king_white1") and (pieceToRemove == "rook_white1"):
           self.addpiece(name, self.images[name[:-1]], int(start[1])-1, let2num[start[0]]-3)
           self.addpiece(pieceToRemove, self.images[pieceToRemove[:-1]], int(start[1])-1, let2num[start[0]]-2)
        elif (name == "king_white1") and (pieceToRemove == "rook_white2"):
           self.addpiece(name, self.images[name[:-1]], int(start[1])-1, let2num[start[0]]+1)
           self.addpiece(pieceToRemove, self.images[pieceToRemove[:-1]], int(start[1])-1, let2num[start[0]])
        else:
            if promote:
                name = "queen" + name[-7:]
            self.addpiece(name, self.images[name[:-1]], int(end[1])-1, let2num[end[0]]-1)
        self.checkFinishGame()

    def refresh(self, event=None):
        '''Redraw the board, possibly in response to window being resized'''
        if event:
            xsize = int((event.width-1) / self.columns)
            ysize = int((event.height-1) / self.rows)
            self.size = min(xsize, ysize)
        self.canvas.delete("square")
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2
        for name in self.pieces:
            self.placepiece(name, self.pieces[name][0], self.pieces[name][1])

        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")

    def show_winner(self, color):
            # create a label displaying the winner
            label = tk.Label(self, text=color, font=("Arial", 24))
            label.pack(side="top", fill="both", expand="true", padx=4, pady=4)

    def checkFinishGame(self):
        if self.logic_board.is_checkmate():
            if self.logic_board.outcome().winner == 1:
                self.show_winner("White wins!")
            if self.logic_board.outcome().winner == 0:
                self.show_winner("Black wins")
            if self.logic_board.outcome().winner == None:
                self.show_winner("Draw")

    def add_all_pieces(self):
        # add white pieces
        for col in range(self.columns):
            self.addpiece("pawn_black" + str(col), self.images["pawn_black"], row=6, column=col)

        self.addpiece("rook_black1", self.images["rook_black"], row=7, column=0)
        self.addpiece("knight_black1", self.images["knight_black"], row=7, column=1)
        self.addpiece("bishop_black1", self.images["bishop_black"], row=7, column=2)
        self.addpiece("queen_black1", self.images["queen_black"], row=7, column=3)
        self.addpiece("king_black1", self.images["king_black"], row=7, column=4)
        self.addpiece("bishop_black2", self.images["bishop_black"], row=7, column=5)
        self.addpiece("knight_black2", self.images["knight_black"], row=7, column=6)
        self.addpiece("rook_black2", self.images["rook_black"], row=7, column=7)

        # add black pieces
        for col in range(self.columns):
            self.addpiece("pawn_white" + str(col), self.images["pawn_white"], row=1, column=col)
        self.addpiece("rook_white1", self.images["rook_white"], row=0, column=0)
        self.addpiece("knight_white1", self.images["knight_white"], row=0, column=1)
        self.addpiece("bishop_white1", self.images["bishop_white"], row=0, column=2)
        self.addpiece("queen_white1", self.images["queen_white"], row=0, column=3)
        self.addpiece("king_white1", self.images["king_white"], row=0, column=4)
        self.addpiece("bishop_white2", self.images["bishop_white"], row=0, column=5)
        self.addpiece("knight_white2", self.images["knight_white"], row=0, column=6)
        self.addpiece("rook_white2", self.images["rook_white"], row=0, column=7)

