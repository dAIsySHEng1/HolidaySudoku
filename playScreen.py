try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from runAppWithScreens import *

##################################
# Play Screen
##################################

def playScreen_onScreenStart(app):
    #board dimensions
    app.ornamentCenters = [(app.width//7, app.height//4), (5*app.width//6, app.height//6)]
    app.letterSize = 80
    app.borderWidth = 2
    app.stepsPerSecond = 0.3

def playScreen_redrawAll(app):
    #background
    drawRect(0,0,app.width,app.height,fill='crimson')
    
    #decorations
    drawOrnaments(app)
    drawHolidayCheer(app)
    drawButtons(app)
    
    #words
    drawLabel('Holiday',app.width//2, app.height//3,
             fill = 'green', bold = True,
            size = app.letterSize, border = 'black')
    drawLabel('Sudoku',app.width//2, app.height//2,
             fill = 'green', bold = True,
            size = app.letterSize, border = 'black')

def drawOrnaments(app):
    radius = 40
    for cx, cy in app.ornamentCenters:
        hangX, hangY = cx, cy-radius
        #string
        drawLine(hangX, 0, hangX, hangY, fill = 'white')
        #hanger
        drawRect(hangX, hangY, radius//2, radius//2, fill = 'goldenrod',
                align = 'center')
        #ball
        drawCircle(cx, cy, radius, fill = 'gold')

def drawHolidayCheer(app):
    #shiny ornaments
    #leftmost ornament
    drawRect(app.width//7+18, app.height//4-18, 10, 15, fill = 'white')
    #rightmost ornament
    drawRect(5*app.width//6+18, app.height//6-18, 10, 15, fill = 'white')


def drawButtons(app):
    msg = ['Standard Mode', 'Key Mode', 'Mouse Mode', 'User Manual']
    for i in range(4):
        drawRect(app.width//2, 2*app.height//3 + 55*i, 150, 45, align = 'center', fill = 'blue', border = 'black')
        drawLabel(msg[i], app.width//2, 2*app.height//3+ 55*i, fill = 'white', bold = True, size = 20)

#Citation (Set Screens): https://www.cs.cmu.edu/~112-3/notes/term-project.html 
def playScreen_onMousePress(app, mouseX, mouseY):
    selectedButton = getButton(app, mouseX, mouseY)
    if selectedButton == 1: #standard button
        setActiveScreen('standard')
    elif selectedButton == 2: #key
        #setActiveScreen('keyOnly')
        setActiveScreen('keyOnly')
    elif selectedButton == 3: #mouse
        setActiveScreen('mouseOnly')
    elif selectedButton == 4: #user manual
        setActiveScreen('helpScreen')

def getButton(app, x, y):
    if (app.width//2-150//2<=x<=app.width//2+150//2):
        #standard button
        if (2*app.height//3-45//2<=y<=2*app.height//3+45//2):
            return 1
        #key button
        elif (2*app.height//3+55-45//2<=y<=2*app.height//3+45//2+55):
            return 2
        #mouse button
        elif (2*app.height//3+55*2-45//2<=y<=2*app.height//3+45//2+55*2):
            return 3
        #user manual
        elif (2*app.height//3+55*3-45//2<=y<=2*app.height//3+45//2+55*3):
            return 4
    return None
