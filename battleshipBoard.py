from prettytable import PrettyTable
import sys

EMPTY_SPACE = "_"

def xArray(symbol):
    list = [symbol]
    for x in range(10):
        list.append(EMPTY_SPACE)
    return list
def xxArray():
    list = []
    list.append(xArray("A"))
    list.append(xArray("B"))
    list.append(xArray("C"))
    list.append(xArray("D"))
    list.append(xArray("E"))
    list.append(xArray("F"))
    list.append(xArray("G"))
    list.append(xArray("H"))
    list.append(xArray("I"))
    list.append(xArray("J"))
    return list

class Board:
    dictionary = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9, "J": 10}
    def __init__(self):
        fieldNamesRow = (" ", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10")
        self.board = PrettyTable()
        self.board._set_field_names(fieldNamesRow)
        self.table = xxArray()
        self.fill(self.table)
        self.board._set_hrules(0)
        # self.board.set_style(12)
        # self.board._set_padding_width(1)

    def print(self):
        print(self.board)

    def fill(self, table):
        for i in range(10):
            # print(list(Board.dictionary.keys())[list(Board.dictionary.values()).index(0)])
            self.board.add_row(table[i])

    def insert(self, coordinates, symbol):
        if(len(coordinates) == 2 or len(coordinates) == 3):
            row = Board.dictionary[coordinates[0].upper()]
            col = int(coordinates[1]) if len(coordinates) == 2 else int(coordinates[1:3])
            if (row < 1 and row > 10) or (col < 1 or col > 10):
                print("Wrong coordinates!")
                return False
            self.board.clear_rows()
            self.table[row-1][col] = symbol if len(symbol) == 1 else symbol[0]
            self.fill(self.table)
            return True
        else:
            print("Wrong coordinates!")
            return False


    def checkCoorValidity(self, coordinates):
        if len(coordinates.split(" ")) != 2:
            print("Wrong coordinates format(or length)!")
            return False
        start, end = coordinates.split(" ")
        if start[0].upper() not in Board.dictionary:
            print("Wrong starting coordinates!")
            return False
        startRow = Board.dictionary[start[0].upper()]
        startCol = int(start[1]) if len(start) == 2 else int(start[1:3])
        if (startRow < 1 or startRow > 10) or (startCol < 1 or startCol > 10):
            print("Wrong starting coordinates!")
            return False
        if end[0].upper() not in Board.dictionary:
            print("Wrong ending coordinates!")
            return False
        endRow = Board.dictionary[end[0].upper()]
        endCol = int(end[1]) if len(end) == 2 else int(end[1:3])
        if (endRow < 1 and endRow > 10) or (endCol < 1 or endCol > 10):
            print("Wrong ending coordinates!")
            return False
        if (startRow != endRow and startCol != endCol):
            print("Wrong coordinates!")
            return False

    def insertShip(self, coordinates):


    def initShips(self):
        print("Initiate the position of your ships, in the following order:\n1x 4 square ship, 2x 3 square ship, 3x 2 square ship, 4x 1 square ship."
              "Enter the starting and ending coordinates of the ship, like the following example: A1 A4 for 4 square ship. ")



b = Board()
b.print()
b.insert("B10", "o")
b.print()