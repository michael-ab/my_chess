import tkinter as tk
import os

class ChessBoard(tk.Frame):
    def __init__(self, parent, rows=8, columns=8, size=100, color1="white", color2="gray"):
        '''size is the size of a square, in pixels'''

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.pieces = {}
        self.board = [[0]*columns] * rows

        canvas_width = columns * size
        canvas_height = rows * size

        self.images = {
            "pawn_write": tk.PhotoImage(file='.\pieces\pw.png'),
            "knight_write": tk.PhotoImage(file='.\pieces\knw.png'),
            "bishop_write": tk.PhotoImage(file='.\pieces\\bw.png'),
            "rook_write": tk.PhotoImage(file='.\pieces\\rw.png'),
            "queen_write": tk.PhotoImage(file='.\pieces\qw.png'),
            "king_write": tk.PhotoImage(file='.\pieces\kw.png'),
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

    def addpiece(self, name, image, row=0, column=0):
        '''Add a piece to the playing board'''
        self.canvas.create_image(0,0, image=image, tags=(name, "piece"), anchor="c")
        self.placepiece(name, row, column)

    def placepiece(self, name, row, column):
        '''Place a piece at the given row/column'''
        self.pieces[name] = (row, column)
        x0 = (column * self.size) + int(self.size/2)
        y0 = (row * self.size) + int(self.size/2)
        self.canvas.coords(name, x0, y0)
        self.board[row][column] = name

    def remove_piece(self, name):
        # remove the piece from the board
        self.canvas.delete(name)

        # remove the piece from the pieces dictionary
        del self.pieces[name]

    def movepiece(self, start, end):
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

        name = self.board[let2num[start[0]]-1][int(start[1])-1]
        self.board[let2num[start[0]]-1][int(start[1])-1] = 0
        self.remove_piece(name)
        self.addpiece(name, self.images[name[:-1]], let2num[end[0]]-1, int(end[1])-1)

    def refresh(self, event):
        '''Redraw the board, possibly in response to window being resized'''
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

    def add_all_pieces(self):
        # create a dictionary mapping piece names to images


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
            self.addpiece("pawn_write" + str(col), self.images["pawn_write"], row=1, column=col)
        self.addpiece("rook_write1", self.images["rook_write"], row=0, column=0)
        self.addpiece("knight_write1", self.images["knight_write"], row=0, column=1)
        self.addpiece("bishop_write1", self.images["bishop_write"], row=0, column=2)
        self.addpiece("queen_write1", self.images["queen_write"], row=0, column=3)
        self.addpiece("king_write1", self.images["king_write"], row=0, column=4)
        self.addpiece("bishop_write2", self.images["bishop_write"], row=0, column=5)
        self.addpiece("knight_write2", self.images["knight_write"], row=0, column=6)
        self.addpiece("rook_write2", self.images["rook_write"], row=0, column=7)


if __name__ == "__main__":
    root = tk.Tk()
    board = ChessBoard(root)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)

    board.add_all_pieces()

    # run the Tk event loop
    root.mainloop()
