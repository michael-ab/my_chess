from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QFrame, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QDrag
from PyQt5.QtCore import Qt, QMimeData, QPoint

class ChessPieceLabel(QLabel):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.setPixmap(pixmap)
        self.setCursor(Qt.OpenHandCursor)
        self.drag_start_position = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.ClosedHandCursor)
            self.mime_data = QMimeData()
            self.pixmap = self.pixmap()
            self.offset = event.pos()
            self.mime_data.setImageData(self.pixmap)
            self.drag_start_position = self.parent().pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
                return
            drag = QDrag(self)
            drag.setMimeData(self.mime_data)
            drag.setPixmap(self.pixmap)
            drag.setHotSpot(self.offset)
            drag.exec_(Qt.MoveAction)
            self.setCursor(Qt.OpenHandCursor)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.OpenHandCursor)
            # Check if the mouse was released over a valid destination square
            parent = self.parent().parent()
            grid_layout = parent.layout()
            index = grid_layout.indexOf(self.parent())
            row, col, _, _ = grid_layout.getItemPosition(index)
            # Update the position of the chess piece on the board
            self.setParent(grid_layout.itemAtPosition(row, col).widget())


class ChessBoard(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the window
        self.setWindowTitle('Chess Board')
        self.setGeometry(300, 300, 650, 750)

        # Create a widget to hold the chessboard
        self.chessboard_widget = QWidget(self)
        self.setCentralWidget(self.chessboard_widget)

        # Create a grid layout for the chessboard
        self.grid_layout = QGridLayout()
        self.chessboard_widget.setLayout(self.grid_layout)

        # Add the chess pieces to the board
        self.add_chess_pieces()

        # Show the window
        self.show()

    def add_chess_pieces(self):
        # Load the images for the chess pieces
        self.black_pawn = QPixmap('pieces/pb.png')
        self.black_knight = QPixmap('pieces/knb.png')
        self.black_bishop = QPixmap('pieces/bb.png')
        self.black_rook = QPixmap('pieces/rb.png')
        self.black_queen = QPixmap('pieces/qb.png')
        self.black_king = QPixmap('pieces/kb.png')
        self.white_pawn = QPixmap('pieces/pw.png')
        self.white_knight = QPixmap('pieces/knw.png')
        self.white_bishop = QPixmap('pieces/bw.png')
        self.white_rook = QPixmap('pieces/rw.png')
        self.white_queen = QPixmap('pieces/qw.png')
        self.white_king = QPixmap('pieces/kw.png')

        # Add the black pieces to the board
        self.add_piece(self.black_rook, 0, 0)
        self.add_piece(self.black_knight, 0, 1)
        self.add_piece(self.black_bishop, 0, 2)
        self.add_piece(self.black_queen, 0, 3)
        self.add_piece(self.black_king, 0, 4)
        self.add_piece(self.black_bishop, 0, 5)
        self.add_piece(self.black_knight, 0, 6)
        self.add_piece(self.black_rook, 0, 7)

        # Add the black pawns to the board
        for i in range(8):
            self.add_piece(self.black_pawn, 1, i)

        # Add the empty squares to the board
        for i in range(2, 6):
            for j in range(8):
                self.add_square((i + j) % 2 == 0)

        # Add the white pawns to the board
        for i in range(8):
            self.add_piece(self.white_pawn, 6, i)

        # Add the white pieces to the board
        self.add_piece(self.white_rook, 7, 0)
        self.add_piece(self.white_knight, 7, 1)
        self.add_piece(self.white_bishop, 7, 2)
        self.add_piece(self.white_queen, 7, 3)
        self.add_piece(self.white_king, 7, 4)
        self.add_piece(self.white_bishop, 7, 5)
        self.add_piece(self.white_knight, 7, 6)
        self.add_piece(self.white_rook, 7, 7)

    def add_square(self, is_white):
        frame = QFrame()
        # Set the background color for the square
        if is_white:
            frame.setStyleSheet('background-color: white')
        else:
            frame.setStyleSheet('background-color: lightgray')
        self.grid_layout.addWidget(frame)

    def add_piece(self, pixmap, row, col):
        # Create a frame with the appropriate background color
        is_white = (row + col) % 2 == 0
        frame = QFrame()
        if is_white:
            frame.setStyleSheet('background-color: white')
        else:
            frame.setStyleSheet('background-color: lightgray')
        self.grid_layout.addWidget(frame, row, col)

        # Add the chess piece label on top of the frame
        label = ChessPieceLabel(pixmap)
        frame.setLayout(QGridLayout())
        frame.layout().addWidget(label, 0, 0)

    def move_piece(self, start, end):

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
        # Get the widget at the starting position
        start_widget = self.grid_layout.itemAtPosition(let2num[start[0]]-1, int(start[1])-1).widget()

        # Remove the widget at the starting position
        self.grid_layout.removeWidget(start_widget)

        # Add the widget at the end position
        self.grid_layout.addWidget(start_widget, let2num[end[0]]-1, int(end[1])-1)

    def showBoard(self):
        self.show()
