# Holiday Sudoku
Holiday Sudoku is my holiday-themed sudoku app for CMU's 15-112 Lecture 3 Term Project. It is written in Python and uses the CMU CS Academy CS3 graphics package. A short video overview about my sudoku project and its special features can be found at this [link](https://www.loom.com/share/0f1516868dbc434aad9f09f96f8942da). Special thanks to Prof. Kosbie and my term project mentor, Ethan!

## Project Description 

Users can play sudoku in 3 different modes: standard, key-only, and mouse-only. A user manual is also provided on the home screen to introduce players to the specifics of the app.

Each mode has 6 different levels: easy, medium, hard, expert, evil, and manual. All levels, except manual, consist of pre-loaded boards from .txt files. In
manual mode, the user can choose to input a custom board or load a .txt file. In each mode, the user can also receive hints, undo/redo moves, and toggle legals. 

### Special Holiday Features:
A "stamps" button is provided in each mode, which allows the user to play a variation of sudoku where numbers are replaced by Canada Post's holiday stamps
from over the years. Users can "play" the stamps by clicking on a key pad or entering a digit from 1-9 corresponding with the particular image's name/position.
To turn holiday mode on/off, click the "Stamps" button in Standard/Mouse mode or type the key "p" in Standard/Key mode.

Once the user has completed a board (i.e. no spaces left), the original board and the user's board will be automatically be saved as a pdf titled 
"sudokuBoards.pdf". The pdf has been designed with the holiday colors of red, green, and white. Note: the user must delete the existing "sudokuBoards.pdf" file 
in order for the program to save a new board. A check has been implemented in the  code to prevent the program from saving a new board to the same file name (which would cause a crash).

### A Few Notes:
- In manual mode, if the user enters an invalid board (i.e. same number in same row, col, or block) or an unsolvable board, the program will indicate
that there is no solution and display "Game Over" when the user exits Manual Entry.
- In key mode, a few additional key functionalities are: "x" to load a manual board; "u" to undo moves; "r" to redo moves; "c" to turn on competition mode;
"j" to highlight the cell for Hint 1; "k" to play the cell for Hint 1; "g" to highlight the cells for Hint 2; "h" to ban legals for Hint 2.

### Running the Program:
- Run the program by running "main.py". You will need the CMU CS Academy graphics package that can be found [here](https://academy.cs.cmu.edu/desktop). 
- No external libraries need to be imported - what's needed has already been imported in the relevant .py files. The holiday stamp images are in the stamps 
folder and the pre-loaded sudoku board are in the board folder.
- This project was coded up using cmu-graphics version 1.1.18.
- Enjoy, and Happy Holidays! 
