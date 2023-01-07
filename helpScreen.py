try: from cmu_cs3_graphics import *
except: from cmu_graphics import *
from helpers import *

from runAppWithScreens import *
##################################
# Help Screen
##################################

def helpScreen_onScreenStart(app):
    app.letterSize = 80
    app.borderWidth = 2

def helpScreen_redrawAll(app):
    #background
    drawRect(0,0,app.width,app.height,fill='crimson')
    
    #decorations
    drawScroll(app)
    drawText(app)
    #side buttons
    drawSideButtons(app)

#draw side buttons
def drawSideButtons(app):
    buttonWidth = 50
    buttonHeight = 25
    drawRect(app.width-buttonWidth-10, 20, buttonWidth, buttonHeight, fill = 'blue', border = 'white')
    drawLabel('Home', app.width-buttonWidth-10 + buttonWidth//2, 20 + buttonHeight//2, fill = 'white', borderWidth = 1, bold = True)

def drawScroll(app):
    scrollWidth = app.width//2
    scrollHeight = 3*app.height//4
    drawRect(app.width//2, app.height//2, scrollWidth,
            scrollHeight, fill='burlyWood', align = 'center')

    drawRect(app.width//2, app.height//2-3*app.height//8, scrollWidth,
           scrollHeight//6, fill='peru', align = 'center')

    drawRect(app.width//2, app.height//2+3*app.height//8, scrollWidth,
           scrollHeight//6, fill='peru', align = 'center')
    
    drawOval(app.width//2-scrollWidth//2, app.height//2-3*app.height//8, 30, scrollHeight//6,
            fill='peru')
    drawOval(app.width//2+scrollWidth//2, app.height//2-3*app.height//8, 30, scrollHeight//6,
            fill='peru')

    drawOval(app.width//2-scrollWidth//2, app.height//2+3*app.height//8, 30, scrollHeight//6,
            fill='peru')
    drawOval(app.width//2+scrollWidth//2, app.height//2+3*app.height//8, 30, scrollHeight//6,
            fill='peru')

def drawText(app):
    drawLabel('User Manual', app.width//2, app.height//4-15, size = 20, bold = True)

    left = app.width//4
    offset = 20
    drawLabel('This holiday-themed Sudoku features 9x9 boards and 3 different', left + offset, app.height//4 + 10, align = 'left')
    drawLabel('modes: standard, keyboard-only, and mouse-only. The boards also', left + offset, app.height//4 + 25, align = 'left')
    drawLabel('come in 5 levels: easy, medium, hard, expert, and evil. In each', left + offset, app.height//4 + 40, align = 'left')
    drawLabel('mode, the user can also manually enter a board or load in a txt.', left + offset, app.height//4 + 55, align = 'left')

    drawLabel('The user can display legals (by clicking on the corresponding', left + offset, app.height//4 + 80, align = 'left')
    drawLabel('button or typing the lowercase L). To add or remove legals, click', left + offset, app.height//4 + 95, align = 'left')
    drawLabel('inside the specific cell (standard or mouse) or turn on toggle', left + offset, app.height//4 + 110, align = 'left')
    drawLabel('legals mode by typing the lowercase T (standard or key mode). The', left + offset, app.height//4 + 125, align = 'left')
    drawLabel('user can play singletons for medium or harder boards in any mode.', left + offset, app.height//4 + 140, align = 'left')
    
    drawLabel('Numbers from the original board are displayed in blue. User inputted', left + offset, app.height//4 + 165, align = 'left')
    drawLabel('values are displayed in purple. Legals are displayed in orange for', left + offset, app.height//4 + 180, align = 'left')
    drawLabel('empty cells. Side buttons are available to change level and mode.', left + offset, app.height//4 + 195, align = 'left')
    
    drawLabel('Standard Mode', left + offset, app.height//4 + 220, size = 14, bold = True, align = 'left')
    drawLabel('Use the mouse to select any cell. Use the keypad or keyboard to', left + offset, app.height//4 + 235, align = 'left')
    drawLabel('input numbers. Use the keyboard or mouse to navigate.', left + offset, app.height//4 + 250, align = 'left')

    drawLabel('Keyboard-Only Mode', left + offset, app.height//4 + 270, size = 14, bold = True, align = 'left')
    drawLabel('Keyboard legend provided in mode. Use r to select center cell.', left + offset, app.height//4 + 285, align = 'left')

    drawLabel('Mouse-Only Mode', left + offset, app.height//4 + 305, size = 14, bold = True, align = 'left')
    drawLabel('When automatic legals are on, the user cannot edit the legals.', left + offset, app.height//4 + 320, align = 'left')

def helpScreen_onMousePress(app, mouseX, mouseY):
    #check if side buttons clicked
    clickInSideButtons(app, mouseX, mouseY)

def clickInSideButtons(app, mouseX, mouseY):
    buttonWidth = 50
    buttonHeight = 25
    #home button
    if (app.width-buttonWidth-10<=mouseX<=app.width-buttonWidth-10+buttonWidth) and (20<=mouseY<=20+buttonHeight):
        setActiveScreen('playScreen')
