import os
import string

#Citation (Write File): Code provided in 15-112 Piazza Post
def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

def convertBoard(stateBoard):
    strBoard = ''
    #2d list board
    for row in range(9):
        rowStr = ''
        for col in range(9):
            rowStr += str(stateBoard[row][col]) + ' '
        rowStr.strip()
        strBoard += rowStr + '\n'
    return strBoard
