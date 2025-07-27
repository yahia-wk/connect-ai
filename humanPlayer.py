import board

class humanPlayer:
    def __init__(self, name):
        self.name = name

    def getMove(self, gameBoard):
        maxCol = gameBoard.numColumns
        choice = int(input("Enter the column number to place your piece: "))
        while choice < 1 or choice > maxCol:
            print("Invalid column number. Please try again.")
            choice = int(input("Enter the column number to place your piece: "))
        return choice -1
