from cmu_cs3_graphics import *
import math
from state import *
from runAppWithScreens import *

##################################
# Button Drawing
##################################

#level buttons - i.e. easy, medium, hard, expert, evil, manual
def drawLevelButtons(app, msg):
    buttonWidth = 120
    buttonHeight = 45
    buttonSpacing = (app.width-5*buttonWidth-40*2)//4
    for i in range(5):
        drawRect(40+ (buttonWidth+buttonSpacing)*i, 2*app.height//3, buttonWidth, buttonHeight, fill = 'blue', border = 'black')
        drawLabel(msg[i], 40+ (buttonWidth+buttonSpacing)*i+buttonWidth//2, 2*app.height//3+ buttonHeight//2, fill = 'white', bold = True, size = 20)
    #manual button
    drawRect(40+ (buttonWidth+buttonSpacing)*2, 4*app.height//5, buttonWidth, buttonHeight, fill = 'lightBlue', border = 'black')
    drawLabel(msg[-1], 40+ (buttonWidth+buttonSpacing)*2+buttonWidth//2, 4*app.height//5+ buttonHeight//2, fill = 'black', bold = True, size = 20)
  

#draw side buttons - i.e. level, mode, help, holiday stamp
def drawSideButtons(app):
    buttonWidth = 50
    buttonHeight = 25
    drawRect(app.width-buttonWidth-10, 20, buttonWidth, buttonHeight, fill = 'blue', border = 'white')
    drawRect(app.width-buttonWidth-10, 20 + buttonHeight + 10, buttonWidth, buttonHeight, fill = 'blue', border = 'white')
    drawLabel('Levels', app.width-buttonWidth-10 + buttonWidth//2, 20 + buttonHeight//2, fill = 'white', borderWidth = 1, bold = True)
    drawLabel('Mode', app.width-buttonWidth-10 + buttonWidth//2, 20 + 3*buttonHeight//2 + 10, fill = 'white', borderWidth = 1, bold = True)
    #holiday button
    drawRect(app.width-buttonWidth-10, 20 + 2*(buttonHeight + 10), buttonWidth, buttonHeight, fill = 'orange', border = 'white')
    drawLabel('Stamps', app.width-buttonWidth-10 + buttonWidth//2, 20 + 5*buttonHeight//2 + 20, fill = 'black', borderWidth = 1, bold = True)

    drawRect(app.width-buttonWidth-10, app.height-buttonHeight-20, buttonWidth, buttonHeight, fill = 'blue', border = 'white')
    drawLabel('Help', app.width-buttonWidth-10 + buttonWidth//2, app.height-buttonHeight//2-20, fill = 'white', borderWidth = 1, bold = True)


def drawManualButton(app, msg):
    cW, cH = getCellSize(app)
    left = app.boardWidth + 3*app.boardLeft
    right = app.width - 2*app.boardLeft
    difference = right-left
    width = (difference-app.boardLeft)//3
    drawRect((left+right)//2, app.boardTop + 1.5*cH, 2.5*width, width//2, align = 'center', fill = 'pink', border = 'black')
    drawLabel(msg, (left+right)//2, app.boardTop + 1.5*cH)

def drawCompetitionButton(app, msg):
    cW, cH = getCellSize(app)
    left = app.boardWidth + 3*app.boardLeft
    right = app.width - 2*app.boardLeft
    difference = right-left
    width = (difference-app.boardLeft)//3
    drawRect((left+right)//2, app.boardTop + 0.75*cH, 2.5*width, width//2, align = 'center', fill = 'pink', border = 'black')
    drawLabel(msg, (left+right)//2, app.boardTop + 0.75*cH)


#pink buttons in mouse only mode
def drawMouseButtons(app):
    cW, cH = getCellSize(app)
    left = app.boardWidth + 3*app.boardLeft
    right = app.width - 2*app.boardLeft
    difference = right-left
    width = (difference-app.boardLeft)//2
    height = 40
    
    for r in range(2):
        for c in range(2):
            if r==1 and c==1 and not app.manualBoard:
                pass
            else:
                drawRect(left+c*(width + app.boardLeft), 
                    app.boardTop + 6.5*cH + r*(height + 0.5*app.boardLeft), width, height, fill = 'pink', border = 'black', borderWidth = 2)
    #labels
    drawLabel('Show/Hide', left + width//2, app.boardTop + 6.75*cH)
    drawLabel('Legals', left + width//2, app.boardTop + 6.95*cH)

    if app.legalsAuto:
        drawLabel('Manual', left + app.boardLeft + 3*width//2, app.boardTop + 6.75*cH)
    else:
        drawLabel('Automatic', left + app.boardLeft + 3*width//2, app.boardTop + 6.75*cH)
    drawLabel('Legals', left + app.boardLeft + 3*width//2, app.boardTop + 6.95*cH)

    drawLabel('Place Next', left + width//2, 8.65*cH)
    drawLabel('Singleton', left + width//2,8.85*cH)

    if app.filter == 'manual' and app.manualBoard == True:
        drawLabel('Exit Manual', left + app.boardLeft + 3*width//2, 8.65*cH)
        drawLabel('Entry', left + app.boardLeft + 3*width//2,8.85*cH)
    else: #undo/redo buttons
        newWidth = (width-10)//2
        drawRect(left + width + app.boardLeft, app.boardTop + 6.5*cH + height + 0.5*app.boardLeft,
                newWidth, height, fill = 'purple', border = 'black', borderWidth = 2)
        drawLabel('Undo', left + width + app.boardLeft + newWidth//2, app.boardTop + 6.5*cH + height + 0.5*app.boardLeft + height//2,
                fill = 'white', size = 10, bold = True)
        
        drawRect(left + width + app.boardLeft + newWidth + 10, app.boardTop + 6.5*cH + height + 0.5*app.boardLeft,
                newWidth, height, fill = 'purple', border = 'black', borderWidth = 2)
        drawLabel('Redo', left + width + app.boardLeft + newWidth//2 + newWidth + 10, 
                app.boardTop + 6.5*cH + height + 0.5*app.boardLeft + height//2,
                fill = 'white', size = 10, bold = True)

def drawHintButtons(app):
    _, cH = getCellSize(app) 
    height = 20
    width = 60
    hintMsg = ['Show', 'Show', 'Play', 'Ban']

    drawLabel('HINT #1', 3*app.boardLeft + app.boardWidth+width//2, app.boardTop + 8.25*cH, fill = 'white', bold = True)
    drawLabel('HINT #2', 3*app.boardLeft + app.boardWidth+3*width//2+10, app.boardTop + 8.25*cH, fill = 'white', bold = True)

    for r in range(2):
        for c in range(2):
            xL = 3*app.boardLeft + app.boardWidth + (10+width)*c
            yL = app.boardTop + 8.4*cH + (5+height)*r
            drawRect(xL, yL, width, height, fill='teal', border = 'black')
            drawLabel(hintMsg[2*r+c], xL + width//2, yL + height//2, fill = 'white', bold = True)

##################################
# Button Click Checking - Controller Helper
##################################

#check which level button user clicked
def getButton(app, x, y):
    msg = ['easy', 'medium', 'hard', 'expert', 'evil', 'manual']
    buttonWidth = 120
    buttonHeight = 45
    buttonSpacing = (app.width-5*buttonWidth-40*2)//4
    
    if (2*app.height//3<=y<=2*app.height//3+buttonHeight):
        for i in range(5):
            if (40+ (buttonWidth+buttonSpacing)*i<=x<=40+ (buttonWidth+buttonSpacing)*i+buttonWidth):
                return msg[i]
    #check manual
    elif (4*app.height//6<=y<=4*app.height//5+buttonHeight):
        if (40+ (buttonWidth+buttonSpacing)*2<=x<=40+ (buttonWidth+buttonSpacing)*2+buttonWidth):
            return msg[-1]
    return None

#checks whether user has clicked in the region of the legals - helps with toggling legals in standard & mouse only modes
def clickInLegal(app, mouseX, mouseY, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    width = cellWidth//3
    for i in range(1,10): #check if in legal set
        legalRow = (i-1)//3 #'row' 0 1 2 of cell
        legalCol = (i-1)%3 #'col' 0 1 2 of cell
        if ((cellLeft+legalCol*width<=mouseX<=cellLeft+legalCol*width+width) and 
            (cellTop+legalRow*width<=mouseY<=cellTop+legalRow*width+width)):
            if (i in app.state.legals[row][col]):
                return i
            else:
                return (0,i)    

#check which number button on keypad user clicked
def getNumKeys(app, x, y):
    _, cH = getCellSize(app)
    left = app.boardWidth + 3*app.boardLeft
    right = app.width - 2*app.boardLeft
    difference = right-left
    width = (difference-app.boardLeft)//3
    for r in range(3):
        for c in range(3):
            if ((left+c*(width + 0.5*app.boardLeft)<=x<=left+c*(width + 0.5*app.boardLeft)+width)
                and (app.boardTop + 3*cH + r*(width + 0.5*app.boardLeft)<=y<=app.boardTop + 3*cH + r*(width + 0.5*app.boardLeft)+width)):
                return 3*r+c+1
    return None

#check whether user clicked in the side buttons (level, mode, help)
def clickInSideButtons(app, mouseX, mouseY):
    buttonWidth = 50
    buttonHeight = 25
    #level button
    if (app.width-buttonWidth-10<=mouseX<=app.width-buttonWidth-10+buttonWidth) and (20<=mouseY<=20+buttonHeight):
        app.chooseLevel = True
    #mode button
    elif (app.width-buttonWidth-10<=mouseX<=app.width-buttonWidth-10+buttonWidth) and (20+buttonHeight + 10<=mouseY<=20+10+2*buttonHeight):
        setActiveScreen('playScreen')
    #help button
    elif (app.width-buttonWidth-10<=mouseX<=app.width-10) and (app.height-buttonHeight-20<=mouseY<=app.height-20):
        setActiveScreen('helpScreen')
    #holiday button    
    elif (app.width-buttonWidth-10<=mouseX<=app.width-10) and (20 + 2*(buttonHeight + 10)<=mouseY<=20 + 2*(buttonHeight + 10)+buttonHeight):
        app.holiday = not app.holiday

#check if user clicked to load a manual txt board
def clickInLoad(app, mouseX, mouseY):
    cW, cH = getCellSize(app)
    left = app.boardWidth + 3*app.boardLeft
    right = app.width - 2*app.boardLeft
    difference = right-left
    width = (difference-app.boardLeft)//3
    if (((left+right)//2-2.5*width//2<=mouseX<=(left+right)//2+2.5*width//2) 
        and (app.boardTop + 1.5*cH - width//4<=mouseY<=app.boardTop + 1.5*cH + width//4)):
        return True

#check if user clicked in pink buttons in mouse only mode
def checkMouseButtons(app, mouseX, mouseY):
    _, cH = getCellSize(app)
    left = app.boardWidth + 3*app.boardLeft
    right = app.width - 2*app.boardLeft
    difference = right-left
    width = (difference-app.boardLeft)//2
    height = 40
    for r in range(2):
        for c in range(2):
            if r==1 and c==1 and not app.manualBoard:
                pass
            elif ((left +c*(width + app.boardLeft)<= mouseX <= left + +c*(width + app.boardLeft) + width) 
                and (app.boardTop + 6.5*cH + r*(height + 0.5*app.boardLeft)<= mouseY <= app.boardTop + 6.5*cH + r*(height + 0.5*app.boardLeft) + height)):
                return 2*r+c
    return None

#check if user clicked in undo button
def clickUndo(app, mouseX, mouseY):
    _, cH = getCellSize(app)
    left = app.boardWidth + 3*app.boardLeft
    right = app.width - 2*app.boardLeft
    difference = right-left
    width = (difference-app.boardLeft)//2
    height = 40
    newWidth = (width-10)//2
    if ((left + width + app.boardLeft<=mouseX<=left + width + app.boardLeft + newWidth) 
        and (app.boardTop + 6.5*cH + height + 0.5*app.boardLeft<=mouseY<=app.boardTop + 6.5*cH + height + 0.5*app.boardLeft+height)):
        return True

#check if user clicked in redo button
def clickRedo(app, mouseX, mouseY):
    _, cH = getCellSize(app)
    left = app.boardWidth + 3*app.boardLeft
    right = app.width - 2*app.boardLeft
    difference = right-left
    width = (difference-app.boardLeft)//2
    height = 40
    newWidth = (width-10)//2
    if ((left + width + app.boardLeft + newWidth + 10<=mouseX<=left + width + app.boardLeft + newWidth + 10+newWidth) 
        and (app.boardTop + 6.5*cH + height + 0.5*app.boardLeft<=mouseY<=app.boardTop + 6.5*cH + height + 0.5*app.boardLeft+height)):
        return True

def clickCompetition(app, mouseX, mouseY):
    cW, cH = getCellSize(app)
    left = app.boardWidth + 3*app.boardLeft
    right = app.width - 2*app.boardLeft
    difference = right-left
    width = (difference-app.boardLeft)//3
    if (((left+right)//2-2.5*width//2<=mouseX<=(left+right)//2+2.5*width//2) 
        and (app.boardTop + 0.75*cH - width//4<=mouseY<=app.boardTop + 0.75*cH + width//4)):
        return True

def clickHints(app, mouseX, mouseY):
    _, cH = getCellSize(app) 
    height = 20
    width = 60

    for r in range(2):
        for c in range(2):
            xL = 3*app.boardLeft + app.boardWidth + (10+width)*c
            yL = app.boardTop + 8.4*cH + (5+height)*r
            if (xL <= mouseX <= xL + width) and (yL <= mouseY <= yL + height):
                return 2*r + c

##################################
# Background Animations
##################################

#draw holiday cheer
def drawHolidayCheer(app):
    drawLabel('Holiday',app.width//2, app.height//3,
             fill = 'green', bold = True,
            size = app.letterSize, border = 'black')
    drawLabel('Sudoku',app.width//2, app.height//2,
             fill = 'green', bold = True,
            size = app.letterSize, border = 'black')

    radius = 40
    ornamentCenters = [(app.width//7, app.height//4), (5*app.width//6, app.height//6)]
    for cx, cy in ornamentCenters:
        hangX, hangY = cx, cy-radius
        #string
        drawLine(hangX, 0, hangX, hangY, fill = 'white')
        #hanger
        drawRect(hangX, hangY, radius//2, radius//2, fill = 'goldenrod',
                align = 'center')
        #ball
        drawCircle(cx, cy, radius, fill = 'gold')

    #leftmost ornament
    drawRect(app.width//7+18, app.height//4-18, 10, 15, fill = 'white')
    #rightmost ornament
    drawRect(5*app.width//6+18, app.height//6-18, 10, 15, fill = 'white')


##################################
# Miscellaneous Drawing Helpers
##################################
from PIL import Image
#Citation (Images & PIL Demo): https://www.cs.cmu.edu/~112-3/notes/term-project.html 

#draw numbers keypad
def drawNumbers(app, typeNum):
    cW, cH = getCellSize(app)
    left = app.boardWidth + 3*app.boardLeft
    right = app.width - 2*app.boardLeft
    difference = right-left
    width = (difference-app.boardLeft)//3

    drawLabel('Key Pad', (left+right)//2, app.boardTop + 2.5*cH, size = 30, bold = True, fill = 'white')

    for r in range(3):
        for c in range(3):
            drawRect(left+c*(width + 0.5*app.boardLeft), 
                    app.boardTop + 3*cH + r*(width + 0.5*app.boardLeft), width, width, fill = 'white', border = 'black', borderWidth = 1)
            if not app.holiday:
                drawLabel(str(3*r + c+1), left+c*(width + 0.5*app.boardLeft) + width//2,
                    app.boardTop + 3*cH + r*(width + 0.5*app.boardLeft) + width//2,
                    size = 20, bold = True)
            else:
                image =  CMUImage(Image.open(f'stamps/img{3*r+c+1}.jpg'))
                drawImage(image, left+c*(width + 0.5*app.boardLeft), app.boardTop + 3*cH + r*(width + 0.5*app.boardLeft),
                        width=width, height=width)

def drawLegals(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    width = cellWidth//3
    for i in range(1,10): #check if in legal set
        if i in app.state.legals[row][col]:
            legalRow = (i-1)//3 #'row' 0 1 2 of cell
            legalCol = (i-1)%3 #'col' 0 1 2 of cell
            drawLabel(str(i), cellLeft+width//2+legalCol*width, cellTop+width//2+legalRow*width,
                        fill = 'orange')

##################################
# Sudoku Board Drawing Helpers
##################################

#Citation (Draw Board): https://cs3-112-f22.academy.cs.cmu.edu/notes/4187 
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col, app.state.board[row][col])

#Citation (Draw Board Borders): https://cs3-112-f22.academy.cs.cmu.edu/notes/4187 
def drawBoardBorders(app):
    cellWidth, cellHeight = getCellSize(app)
    #board border
    drawRect(app.boardLeft-4, app.boardTop-4, app.boardWidth+8, app.boardHeight+8,
            fill = None, border = 'black', borderWidth = 5*app.cellBorderWidth)
    #vertical & horizontal lines
    for index in range(1,int(app.cols**0.5)):
        drawLine(app.boardLeft + 3*index*cellWidth, app.boardTop, 
                app.boardLeft+3*index*cellWidth,
                 app.boardTop + app.boardHeight, fill = 'black',
                 lineWidth = 5*app.cellBorderWidth)
        drawLine(app.boardLeft, app.boardTop + 3*index*cellHeight, 
                app.boardLeft + app.boardWidth, app.boardTop + 3*index*cellHeight, 
                fill = 'black',lineWidth = 5*app.cellBorderWidth)

#Citation (Draw Cell): https://cs3-112-f22.academy.cs.cmu.edu/notes/4187 
#Citation (Images & PIL Demo): https://www.cs.cmu.edu/~112-3/notes/term-project.html 
def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    if (row, col) == app.selection:
        color = 'green'
    elif app.hint2 and (row, col) in app.hint2Draw:
        color = 'pink'
    else:
        color = 'white'
    
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill = color, border='black',
             borderWidth=app.cellBorderWidth)
    labelNum = app.state.board[row][col]
    if app.originalBoard[row][col] != 0:
        labelColor = 'blue'
    elif app.state.board[row][col] != 0:
        labelColor = 'purple'
    if app.state.board[row][col] != 0:
        if not app.holiday:
            drawLabel(str(labelNum), cellLeft+cellWidth//2, cellTop+cellHeight//2,
                size = 20, bold = True, align = 'center', fill = labelColor)
        else:
            image =  CMUImage(Image.open(f'stamps/img{app.state.board[row][col]}.jpg'))
            pilImage = image.image
            drawImage(image, cellLeft+2, cellTop+2,
                    width=cellWidth-4, height=cellHeight-4)
        #incorrect value
        if app.solution != None and app.state.board[row][col] != app.solution[row][col]:
            if not app.holiday:
                drawCircle(cellLeft+cellWidth-12, cellTop + cellWidth-12, 5, fill = 'red')
            else:
                drawCircle(cellLeft+cellWidth-12, cellTop + cellWidth-12, 5, 
                    fill = 'black', border = 'yellow', borderWidth = 2)
    else:
        if app.showLegals and not app.manualBoard:
            #incorrect legals
            if app.solution!=None and app.solution[row][col] not in app.state.legals[row][col]:
                if not app.holiday:
                    drawCircle(cellLeft+cellWidth-12, cellTop + cellWidth-12, 5, fill = 'red')
            drawLegals(app,row,col)


##################################
# Sudoku Board General Helpers
##################################

#Citation: https://cs3-112-f22.academy.cs.cmu.edu/notes/4187 
def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

#Citation: https://cs3-112-f22.academy.cs.cmu.edu/notes/4187 
def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

#counts the number of zeroes on the board
def zeroCount(boardLst):
    numZeros = 0
    rows, cols = len(boardLst), len(boardLst[0])
    for row in range(rows):
        for col in range(cols):
            if boardLst[row][col] == 0:
                numZeros += 1
    return numZeros

#Citation: https://cs3-112-f22.academy.cs.cmu.edu/notes/4189 
def getCell(app, x, y):
    dx = x - app.boardLeft
    dy = y - app.boardTop
    cellWidth, cellHeight = getCellSize(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.rows) and (0 <= col < app.cols):
      return (row, col)
    else:
        i = getNumKeys(app, x, y)
        if i != None:
            return i
        return None


##################################
# General Board Solving Helpers
##################################

def findSingleton(app):
    rows, cols = 9,9
    for row in range(rows):
        for col in range(cols):
            if len(app.state.legals[row][col]) == 1:
                for i in app.state.legals[row][col]:
                    value = i
                return row, col, value
    return None

##################################
# General Controller Helpers
##################################

#Citation: https://cs3-112-f22.academy.cs.cmu.edu/notes/4189
def moveSelection(app, drow, dcol):
    if app.selection != None:
        selectedRow, selectedCol = app.selection
        newSelectedRow = (selectedRow + drow) % app.rows
        newSelectedCol = (selectedCol + dcol) % app.cols
        app.selection = (newSelectedRow, newSelectedCol)

##################################
# Save as PDF Helpers
##################################

import os
from PIL import Image, ImageDraw, ImageFont

#Citation for Draw Text in PIL: https://www.geeksforgeeks.org/python-pil-imagedraw-draw-text/
#Citation for Draw Line in PIL: https://www.geeksforgeeks.org/python-pil-imagedraw-draw-line/ 
#Citation for Crimson Color: https://cs3-112-f22.academy.cs.cmu.edu/docs/builtInColors 
#Citation for Image Font Type & Size in PIL: https://pillow.readthedocs.io/en/stable/reference/ImageFont.html#PIL.ImageFont.truetype 
#Citation for Image, PIL, and Save as PDF: https://www.cs.cmu.edu/~112-3/notes/term-project.html 

def drawing(app,num):
    crimson = (220, 40, 60)
    pilImage = Image.new('RGB', (app.imageWidth, app.imageHeight), crimson)
    draw = ImageDraw.Draw(pilImage)

    font = ImageFont.truetype("arial.ttf", 40)
    if num == 1:
        draw.text((30,40), 'Holiday Sudoku: Original Board', align = 'left', font = font, fill = 'green')
    elif num == 2:
        draw.text((30,40), 'Holiday Sudoku: Your Board', align = 'left', font = font, fill = 'green')

    for row in range(9):
        for col in range(9):
            if app.state.board[row][col] != 0:
                if app.originalBoard[row][col] != 0:
                    draw.text((50+col*60,100+row*50), str(app.originalBoard[row][col]), align = 'left', font = font, fill = 'black')
                else:
                    draw.text((50+col*60,100+row*50), str(app.state.board[row][col]), align = 'left', font = font, fill = 'blue')
            cw = 5 if col % 3 == 0 else 1
            draw.line([(30+(col)*60,100), (30+(col)*60, 100+9*50)], fill = 'white', width = cw)
        w = 5 if row % 3 == 0 else 1
        draw.line([(30,98+(row)*50), (30+9*60, 98+(row)*50)], fill = 'white', width = w)
    
    draw.line([(30+(9)*60,100), (30+(9)*60, 100+9*50)], fill = 'white', width = 5)
    draw.line([(30,100+(9)*50), (30+9*60, 100+(9)*50)], fill = 'white', width = 5)
    return pilImage

#Citation for Saving as PDF in CS3: https://www.cs.cmu.edu/~112-3/notes/term-project.html 
#File Path Check Borrowed from Load Board

def saveAsPdf(app):
    for filename in os.listdir():
        if filename == 'sudokuBoards.pdf':
            return
    cmuImages = [app.image1, app.image2]
    pilImages = [cmuImage.image for cmuImage in cmuImages]
    pilImages[0].save('sudokuBoards.pdf', save_all=True, append_images=pilImages[1:])    