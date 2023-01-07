try: from cmu_cs3_graphics import *
except: from cmu_graphics import *

from runAppWithScreens import *
##################################
# Splash Screen
##################################

def splashScreen_onScreenStart(app):
    app.ornamentCenters = [(app.width//7, app.height//4), (5*app.width//6, app.height//6)]
    app.letterSize = 80
    app.borderWidth = 2
    app.stepsPerSecond = 0.3

def splashScreen_redrawAll(app):
    #background
    drawRect(0,0,app.width,app.height,fill='crimson')
    
    #decorations
    drawOrnaments(app)
    drawLoading(app)
    
    #words
    drawLabel('Holiday',app.width//2, app.height//3,
             fill = 'green', bold = True,
            size = app.letterSize, border = 'black')
    drawLabel('Sudoku',app.width//2, app.height//2,
             fill = 'green', bold = True,
            size = app.letterSize, border = 'black')
    drawLabel('...Loading...',app.width//2, 14.5*app.height//24,
             fill = 'black', bold = True,
            size = 18)

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

def drawLoading(app):
    #bow
    drawLabel('*',app.width//2, 5*app.height//6,
             fill = 'darkViolet', bold = True,
            size = 4*app.letterSize, border = 'black')
    #mini gift grid
    sidelength = app.letterSize*1.5

    drawRect(app.width//2, 5*app.height//6, sidelength, sidelength,
            align = 'center', fill = 'plum', border = 'black',
            borderWidth = app.borderWidth)

    drawRect(app.width//2-sidelength//2, 5*app.height//6-sidelength//2, 
            sidelength//3, sidelength, fill = 'violet', border = 'black',
            borderWidth = app.borderWidth)

    drawRect(app.width//2+sidelength//6, 5*app.height//6-sidelength//2, 
            sidelength//3, sidelength, fill = 'violet', border = 'black',
            borderWidth = app.borderWidth)
    
    drawRect(app.width//2-sidelength//2, 5*app.height//6-sidelength//6, 
            sidelength, sidelength//3, fill = 'blue', border = 'black',
            borderWidth = app.borderWidth)

    drawLabel('15-112', app.width//2, 5*app.height//6, fill = 'white',
            size = 20, bold = True)

def splashScreen_onStep(app):
     setActiveScreen('playScreen')
