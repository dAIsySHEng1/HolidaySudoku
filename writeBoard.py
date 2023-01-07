import os
import string

#Citation (Write File): https://piazza.com/class/l7fcib4cn0c34h/post/453 
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
