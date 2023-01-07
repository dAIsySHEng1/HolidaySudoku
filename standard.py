from cmu_cs3_graphics import *
import copy
from state import *
from loadBoard import *
from helpers import *
from backtracker import *
from runAppWithScreens import *
from writeBoard import *

##################################
# Standard Mode
##################################

def standard_onScreenStart(app):
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

    app.manualBoard = False #whether or not setting manual board
    if app.filter != 'manual':
        app.state = State(loadBoard([filter])) #load random board with filter
        app.solution = solveSudoku(app.state)
    else:
        app.manualBoard = True
        app.state = State([[0]*9 for i in range(9)]) #start with empty board for manual entry
        app.solution = None
    
    app.originalBoard = copy.deepcopy(app.state.board) #original board
    
    app.selection = (app.rows//2, app.cols//2) #cell selection

    app.legalsAuto = True #automatic mode for legals
    if app.filter == 'easy': #easy boards - manual by default
        app.legalsAuto = False
    
    app.showLegals = False #display legals
    app.toggleLegals = False #toggling with legals using the keyboard
    app.buttons = False #unused - for keyboard mode

    app.gameOver = False
    app.numZeroes = zeroCount(app.state.board) #helps determine gameOver

    #undo and redo
    app.movesLst = [(copy.deepcopy(app.state), app.selection)]
    app.statePoint = -1
    app.undoRedo = False

    #competition mode
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


def standard_redrawAll(app):
    #draw background
    drawRect(0,0,app.width,app.height,fill='crimson')

    #user chooses the level of their sudoku
    if app.chooseLevel:
        #draw holiday cheer
        drawHolidayCheer(app)
        #standard mode title
        drawLabel('Standard Mode', app.width//2, app.height//5, fill = 'white', bold = True, size = 35)
        #level buttons
        drawLevelButtons(app, ['Easy', 'Medium', 'Hard', 'Expert', 'Evil', 'Manual'])
    else:
        drawBoard(app)
        drawBoardBorders(app)
        drawNumbers(app, 'normal')
        drawMouseButtons(app)
        drawHintButtons(app)

        msg = f'Standard Mode ({app.filter} level)'
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
            drawLabel('Editing Legals: ON', (left+right)//2, app.boardTop + 1*cH)
        if app.competition:
            drawLabel('Competition Mode: ON', (left+right)//2, app.boardTop + 1.5*cH, bold = True)

        #manual board - legality
        if app.filter == 'manual' and app.solution == None and not app.manualBoard:
            drawLabel('Board Has NO Solution', (left+right)//2, app.boardTop + 0.2*cH)

        #side buttons
        drawSideButtons(app)

        #load manual board button
        if app.filter == 'manual':
            drawManualButton(app, 'Load Manual Board')


def standard_onMousePress(app, mouseX, mouseY):
    #choosing a specific sudoku board level
    if app.chooseLevel:
        selectedButton = getButton(app, mouseX, mouseY)
        if selectedButton != None:
            app.filter = selectedButton
            app.chooseLevel = False
        if not app.chooseLevel: #user has now chosen their sudoku level
            appStart(app, app.filter)
    elif not app.gameOver:
        selectedCell = getCell(app, mouseX, mouseY)
        #clicked within a number or board cell
        if selectedCell != None:
            #clicked on a number
            if type(selectedCell)==int:
                if (app.selection != None):
                    row, col = app.selection
                    #entering numbers to create a manual board
                    if app.manualBoard:
                        app.state.set(row, col, selectedCell)
                        app.originalBoard[row][col] = selectedCell
                        app.state.legals[row][col] = set()
                    #setting a number on board using keypad  
                    elif app.originalBoard[row][col] ==0: 
                        if app.undoRedo: #make move right after an undo/redo
                            if app.statePoint != -1: #not at end of moves list - must truncate
                                app.movesLst = app.movesLst[:app.statePoint+1]
                            app.undoRedo = False
                            app.statePoint = -1 #reset "pointer" to end of list
                            app.state = copy.deepcopy(app.movesLst[app.statePoint][0])
                            app.state.set(row, col, selectedCell)
                        else:
                            #automatically set values and update legals
                            if app.legalsAuto:
                                app.state.set(row, col, selectedCell)
                            #manual legals - simply alter elements on board, not legals
                            else:
                                app.state.board[row][col] = selectedCell

                            if app.competition: #competition mode
                                if app.solution != None and app.state.board[row][col] != app.solution[row][col]: #number wrong - game over
                                    app.gameOver = True
                        #update moves list
                        app.movesLst.append((copy.deepcopy(app.state),app.selection))
            #clicked in a cell on board - and legals are done automatically
            elif app.legalsAuto:
                #can unselect a cell
                if (selectedCell == app.selection):
                    app.selection = None
                else:
                    app.selection = selectedCell
            #manual mode - must check if clicked inside a legal to add/remove it
            else: 
                if (selectedCell != app.selection): #move to newly selected cell
                    app.selection = selectedCell
                elif app.showLegals: 
                    r,c = selectedCell
                    i = clickInLegal(app, mouseX, mouseY, r, c)
                    if (type(i) != tuple): #remove legal
                        app.state.removeLegal(r, c, i)
                    else: #add legal
                        app.state.addLegal(r,c,i[1])
        mouseButton = checkMouseButtons(app, mouseX, mouseY)
        if mouseButton != None:
            if mouseButton == 0:
                app.showLegals = not app.showLegals
            elif mouseButton == 1:
                app.legalsAuto = not app.legalsAuto
            elif mouseButton == 2 and (app.filter == 'medium' or app.filter == 'hard') and not app.competition: #find next singleton
                selectedCell = findSingleton(app)
                if selectedCell == None: #no more singletons to find
                    app.selection = None
                else:
                    row, col, num = selectedCell
                    if app.undoRedo: #move right after doing an undo/redo
                        if app.statePoint != -1:
                            app.movesLst = app.movesLst[:app.statePoint+1]
                        app.undoRedo = False
                        app.statePoint = -1
                        app.state = copy.deepcopy(app.movesLst[app.statePoint][0])
                    app.state.set(row, col, num)
                    app.selection = (row, col)
                    #update moves lst when place singleton
                    app.movesLst.append((copy.deepcopy(app.state), app.selection))
            elif mouseButton == 3 and (app.filter == 'manual'): #exit manual mode
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
        #check whether game over
        app.numZeroes = zeroCount(app.state.board)
        if app.numZeroes == 0:
            #save as pdf
            app.gameOver = True
            app.image2 = drawing(app, 2)
            app.image2 = CMUImage(app.image2)
        app.hint2 = False
        
    #check if side buttons clicked
    clickInSideButtons(app, mouseX, mouseY)
    if app.filter == 'manual':
        if clickInLoad(app, mouseX, mouseY):
            app.state = State(loadBoard([app.filter]))
            app.originalBoard = copy.deepcopy(app.state.board)
            app.solution = solveSudoku(app.state)
            app.manualBoard = False


def standard_onKeyPress(app, key):
    if not app.gameOver:
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
        #clear cell selection
        elif key == 'e':     app.selection = None
        #display legals
        elif key == 'l': app.showLegals = not app.showLegals
        #edit legals
        elif key == 't': 
            app.toggleLegals = not app.toggleLegals
        #finish editing manual board
        elif key == 'm':
            app.manualBoard = False
            app.solution = solveSudoku(app.state)
            if app.solution == None:
                app.gameOver = True
                return
        #automatic legals
        elif key == 'a':
            app.legalsAuto = not app.legalsAuto
        #reset selection to the center of the board
        elif key == 'o':     
            app.selection = (app.rows//2, app.cols//2)
        elif key == 'p':
            app.holiday = not app.holiday
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
        #find next singleton
        elif (key == 's') and (app.filter == 'medium' or app.filter == 'hard') and not app.competition: 
            selectedCell = findSingleton(app)
            if selectedCell == None: #no singletons
                app.selection = None
            else: #set singleton if found
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
        #user entered a valid number when a cell was selected
        elif (app.selection!=None) and key.isdigit() and key!=0 and (app.originalBoard[app.selection[0]][app.selection[1]]==0):
            if app.manualBoard:
                app.state.set(app.selection[0], app.selection[1], int(key))
                app.originalBoard[app.selection[0]][app.selection[1]] = int(key)
                app.state.legals[app.selection[0]][app.selection[1]] = set()
            else:
                r,c = app.selection
                #check if user wants to edit legals using keys
                if app.showLegals and app.toggleLegals:
                    #check if key in legals
                    if int(key) in app.state.legals[r][c]:
                        app.state.removeLegal(r, c, int(key)) #if it's in it - user wants to remove it
                    else:
                        app.state.addLegal(r,c,int(key)) #not currently a legal - user wants to add it
                #enter number into board
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
                        else: #manual legals
                            app.state.board[r][c] = int(key)
                        if app.competition: #competition mode
                            if app.solution != None and app.state.board[r][c] != app.solution[r][c]: #number wrong - game over
                                app.gameOver = True
                    app.movesLst.append((copy.deepcopy(app.state), app.selection))
        #check game over
        app.numZeroes = zeroCount(app.state.board)
        if app.numZeroes == 0:
            #save as pdf
            app.gameOver = True
            app.image2 = drawing(app, 2)
            app.image2 = CMUImage(app.image2)
        app.hint2 = False
