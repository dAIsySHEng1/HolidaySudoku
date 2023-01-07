from cmu_cs3_graphics import *
import copy
from state import *
from loadBoard import *
from helpers import *
from backtracker import *
from runAppWithScreens import *
from writeBoard import *

##################################
# Mouse Only Mode
##################################


def mouseOnly_onScreenStart(app):
    app.chooseLevel = True
    app.filter = None

def appStart(app, filter):
    #board dimensions
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

    app.selection = (app.rows//2, app.cols//2)

    app.legalsAuto = True #automatic mode for legals
    if app.filter == 'easy':
        app.legalsAuto = False

    app.showLegals = False
    app.toggleLegals = False #unused
    app.buttons = False #unused

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


def mouseOnly_redrawAll(app):
    drawRect(0,0,app.width,app.height,fill='crimson')
    if app.chooseLevel:
        #draw holiday cheer
        drawHolidayCheer(app)
        #mode
        drawLabel('Mouse Only Mode', app.width//2, app.height//5, fill = 'white', bold = True, size = 35)
        #level buttons
        drawLevelButtons(app, ['Easy', 'Medium', 'Hard', 'Expert', 'Evil', 'Manual'])
    else:
        drawBoard(app)
        drawBoardBorders(app)
        drawNumbers(app, 'normal')
        drawMouseButtons(app)
        drawHintButtons(app)

        msg = f'Mouse Mode ({app.filter} level)'
        if app.gameOver:
            msg = '*GAME OVER*'
            saveAsPdf(app)
        drawLabel(msg, app.width//3, app.boardTop-30, fill = 'white', bold = True, size = 35)

        #competition mode - save the board when user solves the board (regardless of whether correct)
        if app.competition and app.gameOver:
            writeFile('boards/submit.txt', convertBoard(app.state.board)) #written to file as submit.txt

        #side buttons
        drawSideButtons(app)

        #load manual board button
        if app.filter == 'manual':
            drawManualButton(app, 'Load Manual Board')
        
        #draw competition button
        cOn = 'On' if app.competition else 'Off'
        drawCompetitionButton(app, f'Competition Mode: {cOn}')
        
        #manual board - legality
        left = app.boardWidth + 3*app.boardLeft
        right = app.width - 2*app.boardLeft
        _, cH = getCellSize(app)
        if app.solution == None and not app.manualBoard:
            drawLabel('Board Has NO Solution', (left+right)//2, app.boardTop + 0.2*cH)

def mouseOnly_onMousePress(app, mouseX, mouseY):
    if app.chooseLevel:
        selectedButton = getButton(app, mouseX, mouseY)
        if selectedButton != None:
            app.filter = selectedButton
            app.chooseLevel = False
        if not app.chooseLevel:
            appStart(app, app.filter)
    elif not app.gameOver:
        selectedCell = getCell(app, mouseX, mouseY)
        if selectedCell != None:
            #clicked on a number
            if type(selectedCell)==int:
                if (app.selection != None):
                    row, col = app.selection
                    if app.manualBoard: #manual board entry
                        app.state.set(app.selection[0], app.selection[1], selectedCell)
                        app.originalBoard[app.selection[0]][app.selection[1]] = selectedCell
                        app.state.legals[app.selection[0]][app.selection[1]] = set()   
                    elif app.originalBoard[app.selection[0]][app.selection[1]] ==0: 
                        if app.undoRedo: #move right after doing an undo/redo
                            if app.statePoint != -1: #if at end of list [:0] gives empty list
                                app.movesLst = app.movesLst[:app.statePoint+1]
                            app.undoRedo = False
                            app.statePoint = -1
                            app.state = copy.deepcopy(app.movesLst[app.statePoint][0])
                            app.state.set(row, col, selectedCell)
                        else:
                            if app.legalsAuto: #set number in cell on board
                                app.state.set(app.selection[0], app.selection[1], selectedCell)
                            #manual legals
                            else:
                                app.state.board[app.selection[0]][app.selection[1]] = selectedCell
                            if app.competition: #competition mode
                                if app.solution != None and app.state.board[row][col] != app.solution[row][col]: #number wrong - game over
                                    app.gameOver = True
                            #update moves list
                        app.movesLst.append((copy.deepcopy(app.state),app.selection))
            #clicked in a cell on board & legals are done automatically
            elif app.legalsAuto:
                if (selectedCell == app.selection): #unselect cell
                    app.selection = None
                else:
                    app.selection = selectedCell #select new cell
            else: #manual mode - check if clicked inside a legal
                if (selectedCell != app.selection):
                    app.selection = selectedCell
                elif app.showLegals: #toggle legals only if cell is already selected
                    r,c = selectedCell
                    i = clickInLegal(app, mouseX, mouseY, r, c)
                    if (type(i) != tuple): #remove legal
                        app.state.removeLegal(r, c, i)
                    else: #add legal
                        app.state.addLegal(r,c,i[1])
        #check if any of pink mouse buttons have been clicked
        mouseButton = checkMouseButtons(app, mouseX, mouseY)
        if mouseButton != None:
            if mouseButton == 0:
                app.showLegals = not app.showLegals
            elif mouseButton == 1:
                app.legalsAuto = not app.legalsAuto
            elif mouseButton == 2 and (app.filter == 'medium' or app.filter == 'hard') and not app.competition: #find next singleton:
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
                    #update moves lst when place singleton
                    app.movesLst.append((copy.deepcopy(app.state), app.selection))
            elif mouseButton == 3 and (app.filter == 'manual'):
                app.manualBoard = False
                app.solution = solveSudoku(app.state)
                if app.solution == None:
                    app.gameOver = True
                    return
        #check undo redo
        if clickUndo(app, mouseX, mouseY):
            if app.statePoint > -len(app.movesLst):
                app.statePoint -= 1
                app.state = app.movesLst[app.statePoint][0]
                app.undoRedo = True
                app.selection = app.movesLst[app.statePoint][1]
        elif clickRedo(app, mouseX, mouseY):
            if app.statePoint < -1:
                app.statePoint += 1
                app.state = app.movesLst[app.statePoint][0]
                app.undoRedo = True
                app.selection = app.movesLst[app.statePoint][1]
        
        #check whether asked for a hint
        hintButton = clickHints(app, mouseX, mouseY)
        if hintButton!= None: #user clicked in a hint button
            if hintButton == 0: #hint1 - highlight cells
                hint = app.state.getHint1()
                if hint!=None:
                    app.selection = hint
            elif hintButton == 1: #hint 2 - highlight cells
                cells = app.state.getHint2()
                if cells != None:
                    app.hint2 = True
                    app.hint2Draw = cells
                    return
            elif hintButton == 2: #hint 1 - make move
                hint = app.state.getHint1()
                if hint!=None:
                    row, col = hint
                    app.selection = row, col
                    app.newState = copy.deepcopy(app.state)
                    app.newState.set(row, col, app.solution[row][col])
                    if app.undoRedo: #if play hint after doing an undo-redo
                        if app.statePoint != -1:
                            app.movesLst = app.movesLst[:app.statePoint + 1] #splice extra moves
                        app.undoRedo = False
                        app.statePoint = -1
                    app.state = app.newState
                    app.movesLst.append((copy.deepcopy(app.state), app.selection))
            elif hintButton == 3: #hint 2 - ban values
                cells = app.state.getHint2()
                if cells != None:
                    app.hint2 = True
                    app.hint2Draw = cells
                    app.newState = copy.deepcopy(app.state)
                    vals = []
                    for r,c in cells:
                        vals.append(app.solution[r][c])
                    app.newState.getBansForAllRegions(vals, cells) #ban legals
                    if app.undoRedo: #move right after doing an undo/redo
                        if app.statePoint != -1: #if at end of list [:0] gives empty list
                            app.movesLst = app.movesLst[:app.statePoint+1]
                        app.undoRedo = False
                        app.statePoint = -1
                    app.state = app.newState
                    app.movesLst.append((copy.deepcopy(app.state), app.selection))
                    return
        app.numZeroes = zeroCount(app.state.board)
        if app.numZeroes == 0:
            #save as pdf
            app.gameOver = True
            app.image2 = drawing(app, 2)
            app.image2 = CMUImage(app.image2)
        app.hint2 = False
    clickInSideButtons(app, mouseX, mouseY) #check if click in side buttons

    if clickCompetition(app, mouseX, mouseY):
        app.competition = not app.competition

    if app.filter == 'manual':
        if clickInLoad(app, mouseX, mouseY): #lead manually made txt board
            app.state = State(loadBoard([app.filter]))
            app.originalBoard = copy.deepcopy(app.state.board)
            app.solution = solveSudoku(app.state)
            app.manualBoard = False
