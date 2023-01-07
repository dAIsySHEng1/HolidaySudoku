from cmu_cs3_graphics import *
import copy
from state import *
from loadBoard import *
from helpers import *
from backtracker import *
from writeBoard import *
from runAppWithScreens import *

##################################
# Keyboard Only Mode
##################################

def keyOnly_onScreenStart(app):
    app.chooseLevel = True
    app.filter = None

def appStart(app, filter):
    app.rows = 9
    app.cols = 9

    app.boardLeft = 20
    app.boardTop = 60
    app.boardHeight = app.height-80
    app.boardWidth = app.boardHeight
    app.cellBorderWidth = 1

    app.manualBoard = False
    if app.filter != 'manual':
        app.state = State(loadBoard([filter]))
        app.solution = solveSudoku(app.state)
    else:
        app.manualBoard = True
        app.state = State([[0]*9 for i in range(9)])
        app.solution = None

    app.originalBoard = copy.deepcopy(app.state.board)

    app.selection = (app.rows//2, app.cols//2) #cell selection starts off at the middle of the board

    app.legalsAuto = True
    #easy boards - manual by default
    if app.filter == 'easy':
        app.legalsAuto = False
    app.showLegals = False
    app.toggleLegals = False
    app.buttons = False #flag for whether user wants to select side buttons (level, mode, help)

    app.gameOver = False
    app.numZeroes = zeroCount(app.state.board) #helps to determine gameOver

    #undo and redo
    app.movesLst = [(copy.deepcopy(app.state), app.selection)]
    app.statePoint = -1
    app.undoRedo = False

    app.competition = False

    #displaying hint 2
    app.hint2 = False
    app.hint2Draw = []

    app.holiday = False

    #save as pdf
    app.imageWidth = 600
    app.imageHeight = 600
    app.image1 = CMUImage(drawing(app, 1))
    app.image2 = None


def keyOnly_redrawAll(app):
    drawRect(0,0,app.width,app.height,fill='crimson') #background
    if app.chooseLevel:
        drawHolidayCheer(app)
        drawLabel('Key Only Mode', app.width//2, app.height//5, fill = 'white', bold = True, size = 35)
        
        #drawing the level buttons
        msg = ['Easy (0)', 'Medium (1)', 'Hard (2)', 'Expert (3)', 'Evil (4)', 'Manual (5)']
        drawLevelButtons(app, msg)
    else:
        drawBoard(app)
        drawBoardBorders(app)

        msg = f'Key Mode ({app.filter} level)'
        if app.gameOver:
            msg = '*GAME OVER*'
            saveAsPdf(app)
        drawLabel(msg, app.width//3, app.boardTop-30, fill = 'white', bold = True, size = 35)
        #competition mode - save the board when user solves the board (regardless of whether correct)
        if app.competition and app.gameOver:
            writeFile('boards/submit.txt', convertBoard(app.state.board)) #written to file as submit.txt

        left = app.boardWidth + 3*app.boardLeft
        right = app.width - 2*app.boardLeft
        _, cH = getCellSize(app)
        if app.showLegals and app.toggleLegals:
            drawLabel('Editing Legals: ON', (left+right)//2, app.boardTop + 1.5*cH)
        if app.competition:
            drawLabel('Competition Mode: ON', (left+right)//2, app.boardTop + 1.5*cH, bold = True)


        #side buttons
        drawSideButtons(app)

        #load manual board button
        if app.filter == 'manual':
            drawManualButton(app, 'Load Manual Board (x)')
        
        #manual board - legality
        if app.solution == None and not app.manualBoard:
            drawLabel('Board Has NO Solution', (left+right)//2, app.boardTop + 0.2*cH)

        #key instructions
        drawKeyInstructions(app)

def drawKeyInstructions(app):
    cW, cH = getCellSize(app)
    left = app.boardWidth + 3*app.boardLeft
    right = app.width - 2*app.boardLeft
    difference = right-left
    
    drawLabel('Key Legend', (left+right)//2, app.boardTop + 2.5*cH, size = 30, bold = True, fill = 'white')
    drawLabel('(all lowercase)', (left+right)//2, app.boardTop + 3*cH,size = 15, fill = 'white')
    labels = ['l = display legals', 't = edit legals', 'a = automatic legals', 'o = reset selection to center',
         'm = exit manual board entry', 's = place next singleton','b = access side buttons']
    for i in range(len(labels)):
        drawLabel(labels[i], difference//2 + left, app.boardTop + 3.5*cH + i*30,
                    size = 18, fill = 'white')
    drawLabel('(l = levels; m = mode; h = help)', difference//2 + left, app.boardTop + 3.5*cH + (len(labels)-1)*30+15,
                    size = 15, fill = 'white')
    drawLabel('0-9 = place number in cell', difference//2 + left, app.boardTop + 3.5*cH + len(labels)*30+5,
                    size = 18, fill = 'white')
    drawLabel('(Edit Legals Mode: add/remove legals)', difference//2 + left, app.boardTop + 3.5*cH + (len(labels))*30+20,
                    size = 15, fill = 'white')


def keyOnly_onKeyPress(app, key):
    button = ['easy', 'medium', 'hard', 'expert', 'evil', 'manual']
    if app.chooseLevel:
        if key.isdigit() and key in '012345':
            app.filter = button[int(key)]
            app.chooseLevel = False
        if not app.chooseLevel:
            appStart(app, app.filter)
    elif not app.gameOver:
        #load manual board
        if app.manualBoard and key=='x':
            app.state = State(loadBoard([app.filter]))
            app.originalBoard = copy.deepcopy(app.state.board)
            app.manualBoard = False
        if app.buttons: #side buttons on
            if key == 'l':
                app.chooseLevel = True
            elif key == 'm':
                setActiveScreen('playScreen')
            elif key == 'h':
                setActiveScreen('helpScreen')
        else:
            if key == 'left':    moveSelection(app, 0, -1)
            elif key == 'right': moveSelection(app, 0, +1)
            elif key == 'up':    moveSelection(app ,-1, 0)
            elif key == 'down':  moveSelection(app, +1, 0)
            #undo
            elif key == 'u':
                if app.statePoint > -len(app.movesLst):
                    app.statePoint -= 1
                    app.state = app.movesLst[app.statePoint][0]
                    app.undoRedo = True
                    app.selection = app.movesLst[app.statePoint][1]
            #redo
            elif key == 'r':
                if app.statePoint < -1:
                    app.statePoint += 1
                    app.state = app.movesLst[app.statePoint][0]
                    app.undoRedo = True
                    app.selection = app.movesLst[app.statePoint][1]
            #competition mode
            elif key == 'c': app.competition = not app.competition
            elif key == 'b': app.buttons = not app.buttons
            elif key == 'l': app.showLegals = not app.showLegals
            elif key == 't': 
                app.toggleLegals = not app.toggleLegals
            elif key == 'p':
                app.holiday = not app.holiday
            elif key == 'm':
                app.manualBoard = False
                app.solution = solveSudoku(app.state)
                if app.solution == None:
                    app.gameOver = True
                    return
            elif key == 'a':
                app.legalsAuto = not app.legalsAuto
            elif key == 'o':     
                app.selection = (app.rows//2, app.cols//2)
            #hint 1 - show
            elif key == 'j':
                hint = app.state.getHint1()
                if hint!=None:
                    app.selection = hint
            #hint 1 - play
            elif key == 'k':
                hint = app.state.getHint1()
                if hint!=None:
                    row, col = hint
                    app.selection = row, col
                    app.newState = copy.deepcopy(app.state)
                    app.newState.set(row, col, app.solution[row][col])
                    if app.undoRedo: #play hint after doing an undo-redo
                        if app.statePoint != -1:
                            app.movesLst = app.movesLst[:app.statePoint + 1] #splice extra moves
                        app.undoRedo = False
                        app.statePoint = -1
                    app.state = app.newState
                    app.movesLst.append((copy.deepcopy(app.state), app.selection))
            #hint 2 - show
            elif key == 'g':
                cells = app.state.getHint2()
                if cells != None:
                    app.hint2 = True
                    app.hint2Draw = cells
                    return
            #hint 2 - ban legals
            elif key == 'h':
                cells = app.state.getHint2()
                if cells != None:
                    app.hint2 = True
                    app.hint2Draw = cells
                    app.newState = copy.deepcopy(app.state)
                    vals = []
                    for r,c in cells:
                        vals.append(app.solution[r][c])
                    app.newState.getBansForAllRegions(vals, cells)
                    if app.undoRedo: #move right after doing an undo/redo
                        if app.statePoint != -1: #if at end of list [:0] gives empty list
                            app.movesLst = app.movesLst[:app.statePoint+1]
                        app.undoRedo = False
                        app.statePoint = -1
                    app.state = app.newState
                    app.movesLst.append((copy.deepcopy(app.state), app.selection))
                    return
            elif (key == 's') and (app.filter == 'medium' or app.filter == 'hard') and not app.competition: #find next singleton
                selectedCell = findSingleton(app)
                if selectedCell == None: #placeholder
                    app.selection = None
                else:
                    row, col, num = selectedCell
                    if app.undoRedo: #move right after doing an undo/redo
                        if app.statePoint != -1: #if at end of list [:0] gives empty list
                            app.movesLst = app.movesLst[:app.statePoint+1]
                        app.undoRedo = False
                        app.statePoint = -1
                        app.state = copy.deepcopy(app.movesLst[app.statePoint][0])
                    app.state.set(row, col, num)
                    app.selection = (row, col)
                    app.movesLst.append((copy.deepcopy(app.state), app.selection))
            elif key.isdigit() and key!=0 and (app.originalBoard[app.selection[0]][app.selection[1]]==0):
                if app.manualBoard: #entering values for manual board input
                    app.state.set(app.selection[0], app.selection[1], int(key))
                    app.originalBoard[app.selection[0]][app.selection[1]] = int(key)
                    app.state.legals[app.selection[0]][app.selection[1]] = set()
                else:
                    r,c = app.selection
                    if app.showLegals and app.toggleLegals:
                        #check if key in legals
                        if int(key) in app.state.legals[r][c]:
                            app.state.removeLegal(r, c, int(key)) #if it's in it - user wants to remove
                        else:
                            app.state.addLegal(r,c,int(key)) #not currently showing as a legal - user wants to add it
                    else:
                        if app.undoRedo: #move right after doing an undo/redo
                            if app.statePoint != -1: #if at end of list [:0] gives empty list
                                app.movesLst = app.movesLst[:app.statePoint+1]
                            app.undoRedo = False
                            app.statePoint = -1
                            app.state = copy.deepcopy(app.movesLst[app.statePoint][0])
                            app.state.set(r, c, int(key))
                        else:
                            if app.legalsAuto:
                                app.state.set(r, c, int(key))
                            else:
                                app.state.board[r][c] = int(key)
                            if app.competition: #competition mode
                                if app.solution != None and app.state.board[r][c] != app.solution[r][c]: #number wrong - game over
                                    app.gameOver = True
                        app.movesLst.append((copy.deepcopy(app.state), app.selection))
            app.numZeroes = zeroCount(app.state.board)
            if app.numZeroes == 0:
                #save as pdf
                app.gameOver = True
                app.image2 = drawing(app, 2)
                app.image2 = CMUImage(app.image2)
            app.hint2 = False
