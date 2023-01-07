from state import *
from loadBoard import *
from helpers import *
import copy

def solveSudoku(stateObj):
    #check legality of board first before running backtracker (prevent manual boards from being illegal)
    if not boardLegal(stateObj):
        return None
    else:
        return sudokuSoln(copy.deepcopy(stateObj), zeroCount(stateObj.board))

def boardLegal(stateObj):
    allRegions = stateObj.getAllRegions()
    for region in allRegions:
        regionSet = set()
        regionLst = []
        for row,col in region:
            if stateObj.board[row][col] != 0:
                regionSet.add(stateObj.board[row][col])
                regionLst.append(stateObj.board[row][col])
        if len(regionSet) != len(regionLst):
            return False
    return True

def sudokuSoln(stateObj, numZeroes):
    if numZeroes == 0: #base case
        return stateObj.board
    else: #recursive case
        newRow, newCol = fewestLegals(stateObj)
        for num in stateObj.legals[newRow][newCol]: #iterate through legals of the board; legality check implied
            newState = State(stateObj.board) #non-mutate
            newState.set(newRow,newCol,num)
            potentialSoln = sudokuSoln(newState, numZeroes -1)
            #check if move leads to a viable solution
            if potentialSoln != None:
                return potentialSoln
            #no need to undo b/c not mutate original board
        return None

def fewestLegals(stateObj):
    rows, cols = 9,9
    minLegals = rows
    bRow, bCol = 0,0
    for row in range(rows):
        for col in range(cols):
            if (stateObj.board[row][col] == 0):
                legalsLen = len(stateObj.legals[row][col])
                if legalsLen < minLegals:
                    minLegals = legalsLen
                    bRow, bCol = (row, col)
    return bRow, bCol