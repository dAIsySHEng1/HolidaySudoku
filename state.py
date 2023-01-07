import itertools
from loadBoard import *

#Citation (State Class Idea & Code Snippets): https://www.cs.cmu.edu/~112-3/notes/tp-sudoku-hints.html
class State():
    def __init__(self, board): 
        #start off with empty board & full legals
        self.board = [[0]*9 for i in range(9)]
        self.legals = [[{1,2,3,4,5,6,7,8,9} for j in range(9)] for i in range(9)]

        #populate board
        for row in range(9):
            for col in range(9):
                if board[row][col]!= 0:
                    self.set(row, col, board[row][col])

    def set(self, row, col, value):
        #set the value in the board
        self.board[row][col] = value
        #eliminate legal set for value
        self.legals[row][col] = set()
        #eliminate # from row
        for i in range(9):
            if value in self.legals[row][i]:
                self.legals[row][i].remove(value)
        #eliminate # from col
        for i in range(9):
            if value in self.legals[i][col]:
                self.legals[i][col].remove(value)
        #eliminate from block
        lenBlock = 3
        blockTopRow = (row//lenBlock)*lenBlock
        blockLeftCol = (col//lenBlock)*lenBlock
        for r in range(lenBlock):
            for c in range(lenBlock):
                if value in self.legals[blockTopRow+r][blockLeftCol+c]:
                    self.legals[blockTopRow+r][blockLeftCol+c].remove(value)
        
    def removeLegal(self, row, col, value):
        if value in self.legals[row][col]:
            self.legals[row][col].remove(value)
    
    def addLegal(self, row, col, value):
        self.legals[row][col].add(value)
    #hint 1
    def getHint1(self): #returns (row, col) representing the cell to place/highlight; singletons
        rows, cols = 9,9
        for row in range(rows):
            for col in range(cols):
                if len(self.legals[row][col]) == 1:
                    return (row, col)
        return None

    #hint 2
    def getHint2(self): #returns a list of tuples representing the grouping of cells in the hint
        for N in range(2, 6):
            for region in self.getAllRegions():
                result = self.applyRule2(region, N)
                if result != None:
                    return result
        return None
    
    def applyRule2(self, region, N):
        solution = self.solveSudoku()
        if solution != None: #ensures if legals are not correct and no soln that not crash
            for cellCombo in itertools.combinations(region, N):
                corrValues = []
                for row, col in cellCombo:
                    corrValues.append(solution[row][col]) #get the correct values in the solution
                if self.valuesAreOnlyLegals(corrValues, cellCombo): #check that the cells only involve legals
                    if self.noSingles(cellCombo):#check that none are singles
                        banning = self.getNumBans(corrValues, cellCombo)
                        if banning: #at least one ban
                            return cellCombo
        return None

    def getNumBans(self, values, target):
        targRow = target[0][0]
        #check row
        superRow = set(self.getRowRegion(targRow))
        if superRow & set(target) == set(target):
            for cell in superRow:
                if (cell not in target) and self.legals[cell[0]][cell[1]]!=set():
                    for value in values:
                        if value in self.legals[cell[0]][cell[1]]:
                            return True
        #check col
        targCol = target[0][1]
        superCol = set(self.getColRegion(targCol))
        if superCol & set(target) == set(target):
            for cell in superCol:
                if (cell not in target) and self.legals[cell[0]][cell[1]]!=set():
                    for value in values:
                        if value in self.legals[cell[0]][cell[1]]:
                            return True
        
        #check block
        superBlock = set(self.getBlockRegionByCell(targRow, targCol))
        if superBlock & set(target) == set(target):
            for cell in superBlock:
                if (cell not in target) and self.legals[cell[0]][cell[1]]!=set():
                    for value in values:
                        if value in self.legals[cell[0]][cell[1]]:
                            return True
        return False

    def noSingles(self, target):
        for r,c in target:
            if len(self.legals[r][c]) <=1:
                return False
        return True
    
    def getBansForAllRegions(self, values, target):
        #must check if hint2 encompasses a row, col, or block so remove values from legals in that region
        numBans = 0
        
        targRow = target[0][0]
        targCol = target[0][1]
        #check row
        superRow = set(self.getRowRegion(targRow))
        if superRow & set(target) == set(target):
            for cell in superRow:
                if (cell not in target):
                    for value in values:
                        self.removeLegal(cell[0], cell[1], value)
                        numBans += 1
        #check col
        superCol = set(self.getColRegion(targCol))
        if superCol & set(target) == set(target):
            for cell in superCol:
                if (cell not in target):
                    for value in values:
                        self.removeLegal(cell[0], cell[1], value)
                        numBans += 1
        
        #check block
        superBlock = set(self.getBlockRegionByCell(targRow, targCol))
        if superBlock & set(target) == set(target):
            for cell in superBlock:
                if (cell not in target):
                    for value in values:
                        self.removeLegal(cell[0], cell[1], value)
                        numBans += 1
        return numBans
    
    #check that dealing with legals only
    def valuesAreOnlyLegals(self, values, targets): #targets is a tuple; values is a list of backtracker values
        combinedLegals = set()
        for r,c in targets:
            combinedLegals = combinedLegals | self.legals[r][c]
        return len(combinedLegals) == len(targets) and combinedLegals == set(values)

    #regions - a list of 9 (row,col) tuples
    def getRowRegion(self, row):
        rowRegionLst = []
        for col in range(9):
            rowRegionLst.append((row, col))
        return tuple(rowRegionLst)

    def getColRegion(self, col):
        colRegionLst = []
        for row in range(9):
            colRegionLst.append((row, col))
        return tuple(colRegionLst)
    
    def getBlockRegion(self, block): 
        firstRow = (block//3)*3
        firstCol = (block%3)*3
        blockRegionLst = []
        for row in range(firstRow, firstRow + 3):
            for col in range(firstCol, firstCol + 3):
                blockRegionLst.append((row,col))
        return tuple(blockRegionLst)
    
    def getBlockRegionByCell(self, row, col):
        block = (row//3)*3 + col//3
        return self.getBlockRegion(block)
        
    def getBlock(self, row, col):
        return (row//3)*3 + col//3

    def getCellRegions(self, row, col): #ban legals once place a value
        rowRegion = set(self.getRowRegion(row))
        colRegion = set(self.getColRegion(col))
        blockRegion = set(self.getBlock(self, row, col))
        return list(rowRegion | colRegion | blockRegion)
    
    def getAllRegions(self):
        allRegionLst = []
        for row in range(9):
            allRegionLst.append(self.getRowRegion(row))
        for col in range(9):
            allRegionLst.append(self.getColRegion(col))
        for block in range(9):
            allRegionLst.append(self.getBlockRegion(block))
        return allRegionLst
    
    def getAllRegionsThatContainTargets(self, targets):
        allTargetRegions = set()
        for (row, col) in targets:
            allTargetRegions = allTargetRegions | set(self.getRowRegion(row)) | set(self.getColRegion(col)) | set(self.getBlock(row,col))
        return list(allTargetRegions)
    
    def solveSudoku(self):
        return self.sudokuSoln(self.zeroCount())

    def zeroCount(self):
        numZeros = 0
        rows, cols = len(self.board), len(self.board[0])
        for row in range(rows):
            for col in range(cols):
                if self.board[row][col] == 0:
                    numZeros += 1
        return numZeros

    def sudokuSoln(self, numZeroes):
        if numZeroes == 0: #base case
            return self.board
        else: #recursive case
            newRow, newCol = self.fewestLegals()
            for num in self.legals[newRow][newCol]: #iterate through legals of the board; legality check implied
                newState = State(self.board) #non-mutate
                newState.set(newRow,newCol,num)
                potentialSoln = newState.sudokuSoln(numZeroes -1)
                #check if move leads to a viable solution
                if potentialSoln != None:
                    return potentialSoln
                #no need to undo b/c not mutate original board

    def fewestLegals(self):
        rows, cols = 9,9
        minLegals = rows
        bRow, bCol = 0,0
        for row in range(rows):
            for col in range(cols):
                if (self.board[row][col] == 0):
                    legalsLen = len(self.legals[row][col])
                    if legalsLen < minLegals:
                        minLegals = legalsLen
                        bRow, bCol = (row, col)
        return bRow, bCol

#Citation: https://www.cs.cmu.edu/~112-3/notes/tp-sudoku-hints.html 
    def printBoard(self):
        print2dList(self.board)

#Citation: https://www.cs.cmu.edu/~112-3/notes/tp-sudoku-hints.html 
    def printLegals(self):
        colWidth = 4
        for col in range(9):
            colWidth = max(colWidth, 1+max([len(self.legals[row][col]) for row in range(9)]))
        for row in range(9):
            for col in range(9):
                label = ''.join([str(v) for v in sorted(self.legals[row][col])])
                if label == '': label = '-'
                print(f"{' '*(colWidth - len(label))}{label}", end='')
            print()
#citation: https://www.cs.cmu.edu/~112-3/notes/tp-sudoku-hints.html 
    def print(self): self.printBoard(); self.printLegals()
    
#Citation: https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html#printing 
def repr2dList(L):
        if (L == []): return '[]'
        output = [ ]
        rows = len(L)
        cols = max([len(L[row]) for row in range(rows)])
        M = [['']*cols for row in range(rows)]
        for row in range(rows):
            for col in range(len(L[row])):
                M[row][col] = repr(L[row][col])
        colWidths = [0] * cols
        for col in range(cols):
            colWidths[col] = max([len(M[row][col]) for row in range(rows)])
        output.append('[\n')
        for row in range(rows):
            output.append(' [ ')
            for col in range(cols):
                if (col > 0):
                    output.append(', ' if col < len(L[row]) else '  ')
                output.append(M[row][col].rjust(colWidths[col]))
            output.append((' ],' if row < rows-1 else ' ]') + '\n')
        output.append(']')
        return ''.join(output)    

#Citation: https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html#printing 
def print2dList(L):
    print(repr2dList(L))
