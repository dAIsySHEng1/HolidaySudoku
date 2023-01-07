import os
import random

#Citation (Load Board): https://www.cs.cmu.edu/~112-3/notes/tp-sudoku-hints.html 
def loadBoardPaths(filters):
    boardPaths = [ ]
    for filename in os.listdir(f'boards/'):
        if filename.endswith('.txt'):
            if hasFilters(filename, filters):
                boardPaths.append(f'boards/{filename}')
    return boardPaths

#Citation (Load Board): https://www.cs.cmu.edu/~112-3/notes/tp-sudoku-hints.html 
def hasFilters(filename, filters=None):
    if filters == None: return True
    for filter in filters:
        if filter not in filename:
            return False
    return True

#Citation (Read File): Code provided in 15-112 Piazza Post
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

#processing the board to turn it into a list
def lstBoard(s):
    board = []
    for line in s.splitlines():
        numberLst = line.split()
        numLst = []
        for numStr in numberLst:
            numLst.append(int(numStr))
        board.append(numLst)
    return board

#Citation (Load Board): Code provided in 15-112 Piazza Post
def loadBoard(filters):
    filesLst = loadBoardPaths(filters)
    filename = random.choice(filesLst)
    pathToFile = f'{filename}'
    fileContents = readFile(pathToFile)
    return lstBoard(fileContents)
