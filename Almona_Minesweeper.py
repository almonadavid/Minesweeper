#Name: Almona
#Date: Fall 2024 Semester
#Purpose: CSC 170 Final Project, Minesweeper

import random
from graphics import *


def text_based(gameboard, mineboard, i_row, i_col, i_mines):
    # Keep track of flags
    flags_remaining = i_mines

    # Flag to check if first move has been made
    first_move = True

    # Allow user to save to file with custom name
    i_save = input("\nDo you want to save game? (y/n) (case-sensitive): ")
    if i_save == 'y':
        filename = input("Enter filename to save the game: ").strip()
        print("Game will be saved\n")
        file = open(filename, 'a')
    else:
        print("Game NOT saved\n")
    print()

    # Game loop
    game_play = True
    while game_play:
        
        alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        alphabet_dict = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'I': 8, 'J': 9, 'K':10}
                
        print("\nMines remaining: ", flags_remaining)
        print_game_board(gameboard)

        # Loop write to file
        if i_save == 'y':
            file.write("  ")  # Leave space for row headers
            for col in range(1, len(gameboard[0]) + 1):  # Write column numbers
                file.write(str(col) + " ")
            file.write("\n")

            rowcount = 0
            for row in gameboard:
                file.write(alphabet[rowcount] + " ")  # Add row letter at the start
                rowcount += 1
                for item in row:
                    file.write(item + " ")
                file.write("\n")
            file.write("\n")
            
        user_input = input("\nEnter action (O for Open, F for Flag) and position (row col) (case-sensitive): ")
        user_input = user_input.strip()
        user_input = user_input.split(' ')

        # Input validation for action
        action_list = ['O', 'F']
        while len(user_input) < 3 or user_input[0] not in action_list:
            print("Invalid input! Format must be: Action (O/F) Row Column")
            user_input = input("Re-enter action and position (case-sensitive): ")
            user_input = user_input.strip()
            user_input = user_input.split(' ')
        
        action = user_input[0]

        # Input validation for row
        valid_rows = alphabet[:i_row]
        row_letter = user_input[1]
        while row_letter not in valid_rows:
            print("Invalid row input!!!")
            row_letter = input("Re-enter row letter (case-sensitive): ")
            row_letter = row_letter.strip()
        row_input = alphabet_dict[row_letter]

        # Input validation for column
        valid_col = []
        for index in range(1,i_col+1):
            valid_col.append(str(index))
            
        col_input = user_input[2]
        while col_input not in valid_col:
            print("Invalid column input!!!")
            col_input = input("Re-enter column number: ")
            col_input = col_input.strip()

        col_input = int(col_input) - 1

        if i_save == 'y':
            file.write("Your move was => Action: " + str(action) + " Row: " + str(row_input) + " Column: " + str(col_input) + "\n")
            

        if action == 'O':
            #regenerate board to ensure safe first click
            if first_move:
                mineboard = relocate_mines(mineboard, row_input, col_input) 
                first_move = False
                
            if gameboard[row_input][col_input] != '-' and gameboard[row_input][col_input] != '?':  # To check if cell is already revealed
                print("This cell is revealed. Choose another cell.")
                if i_save == 'y':
                    file.write("\nThis cell is revealed. Choose another cell.\n")
            elif mineboard[row_input][col_input]: # To check if cell has hidden mine
                print("BOOM! Game Over!")
                if i_save == 'y':
                    file.write("BOOM! Game Over!\n")
                    file.close()
                game_play = False
            else:
                mine_count = count_adjacent_mines(mineboard, row_input, col_input)
                gameboard[row_input][col_input] = str(mine_count)
                # Next: reveal_adjacent_cells()
                if mine_count == 0:
                    reveal_adjacent_cells(gameboard, mineboard, row_input, col_input)

        elif action == 'F': 
            if gameboard[row_input][col_input] == '-':  # This ensures to only flag unopened cells
                gameboard[row_input][col_input] = '?'
                flags_remaining = flags_remaining - 1
            elif gameboard[row_input][col_input] == '?':  # Flag user placed can be removed
                gameboard[row_input][col_input] = '-'
                flags_remaining = flags_remaining + 1
        else:
            print("Invalid action! Use O for Open or F for Flag")
            if i_save == 'y':
                file.write("Invalid action! Use O for Open or F for Flag\n")

        if check_win(gameboard, mineboard):
            print("\nCongratulations! You've won the game!")
            if i_save == 'y':
                file.write("\nCongratulations! You've won the game!")
            game_play = False

    if i_save == 'y':
        file.close()


def graphics_window(gameboard, mineboard, i_row, i_col, i_mines): 

    # Graphics Window with extra width for flag button
    win = GraphWin("Minesweeper", (i_col * 30) + 60, i_row * 30)

    # Create game board cells
    cells = []
    for row in range(i_row):
        rowlist = []
        for col in range(i_col):
            rect = Rectangle(Point(col * 30, row * 30), Point((col + 1) * 30, (row + 1) * 30))
            rect.setFill("gray")
            rect.draw(win)
            rowlist.append(rect)
        cells.append(rowlist)

    # Create flag button outside game board
    flag_button = Rectangle(Point(i_col * 30 + 10, (i_row * 30 // 2) - 15), Point(i_col * 30 + 50, (i_row * 30 // 2) + 15))
    flag_button.setFill("lightgray")
    flag_button.draw(win)
    flag_text = Text(flag_button.getCenter(), "Flag")
    flag_text.draw(win)

    flags_remaining = i_mines
    flag_mode = False

    first_click = True

    game_play = True
    while game_play:
        click = win.getMouse()
        click_x = click.getX()
        click_y = click.getY()

        # Check if flag button is clicked
        if (click_x >= i_col * 30 + 10 and click_x <= i_col * 30 + 50 and click_y >= (i_row * 30 // 2) - 15 and click_y <= (i_row * 30 // 2) + 15):
            flag_mode = not flag_mode
            if flag_mode:
                flag_button.setFill("yellow")
                flag_text.setText("Flag (" + str(flags_remaining) + ")")
            else:
                flag_button.setFill("lightgray")
                flag_text.setText("Flag")
        elif click_x < i_col * 30:  # Prevent clicks outside game board
            col_input = int(click_x // 30)
            row_input = int(click_y // 30)

            # Flag mode handling
            if flag_mode:
                if gameboard[row_input][col_input] == '-' and flags_remaining > 0:
                    gameboard[row_input][col_input] = '?'
                    cells[row_input][col_input].setFill("orange")
                    flags_remaining -= 1
                    flag_text.setText("Flag (" + str(flags_remaining) + ")")
                elif gameboard[row_input][col_input] == '?':
                    gameboard[row_input][col_input] = '-'
                    cells[row_input][col_input].setFill("gray")
                    flags_remaining += 1
                    flag_text.setText("Flag (" + str(flags_remaining) + ")")
            else:
                if first_click:
                    mineboard = relocate_mines(mineboard, row_input, col_input)
                    first_click = False

                if mineboard[row_input][col_input]:
                    cells[row_input][col_input].setFill("red")
                    print("BOOM! Game Over!")
                    for row in range(len(mineboard)):
                        for col in range(len(mineboard[0])):
                            if mineboard[row][col]:
                                cells[row][col].setFill("red")
                    game_play = False
                else:
                    mine_count = count_adjacent_mines(mineboard, row_input, col_input)
                    cells[row_input][col_input].setFill("white")
                    if mine_count > 0:
                        gameboard[row_input][col_input] = str(mine_count)
                        label = Text(cells[row_input][col_input].getCenter(), str(mine_count))
                        label.draw(win)
                    else:
                        reveal_adjacent_cells_graphics(gameboard, mineboard, cells, win, row_input, col_input)

                if check_win(gameboard, mineboard):
                    print("\nCongratulations! You've won the game!")
                    for row in range(len(mineboard)):
                        for col in range(len(mineboard[0])):
                            if mineboard[row][col]:
                                cells[row][col].setFill("red")
                    game_play = False

##    win.close() #decided to kep window open so user can inspect gameboard

def game_and_mine_board(row, col, mines): 
    gameboard = []
    for r in range(row):
        rowlist = []
        for c in range(col):
            rowlist.append('-')
        gameboard.append(rowlist)

    mineboard = []
    for r in range(row):
        rowlist = []
        for c in range(col):
            rowlist.append(False)
        mineboard.append(rowlist)

    #Randomize mines
    count = 0 #Keeping track of number of mines placed
    while count < mines:
        mine_row = random.randint(0,row-1)
        mine_col = random.randint(0,col-1)

        if mineboard[mine_row][mine_col] == False:
            mineboard[mine_row][mine_col] = True
            count += 1

    return gameboard, mineboard


def relocate_mines(mineboard, first_row, first_col):
    row = len(mineboard)
    col = len(mineboard[0])
    
    # Collect all current mine locations
    current_mines = []
    for r in range(row):
        for c in range(col):
            if mineboard[r][c]:
                current_mines.append((r, c))
                mineboard[r][c] = False
    
    # Potential safe cell check
    def is_safe_cell(r, c):
        if r < int(first_row) - 1 or r > int(first_row) + 1 or c < int(first_col) - 1 or c > int(first_col) + 1:
            return True
        return False
    
    # Redistribute mines
    count = 0
    index = 0
    while index < len(current_mines):
        mine_row, mine_col = current_mines[index]
        index += 1

        # Find a new safe location
        found_safe_location = False
        while not found_safe_location:
            new_row = random.randint(0, row - 1)
            new_col = random.randint(0, col - 1)

            # Check if this new location is safe and not already mined
            if is_safe_cell(new_row, new_col) and not mineboard[new_row][new_col]:
                mineboard[new_row][new_col] = True
                found_safe_location = True

    return mineboard

  
def print_game_board(gameboard):

    alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L']
    rowcount = 0
    colcount = 1
    print()
    print(' ', end = ' ')
    for item in gameboard[0]:
        print(colcount, end = ' ')
        colcount += 1
    print()
    
    for row in gameboard:
        print(alphabet[rowcount], end = ' ')
        rowcount += 1
        for item in row:
            print(item, end = ' ')
        print()


def count_adjacent_mines(mineboard, row_input, col_input):
    # I could either use multiple if-elif-else statements or for loop
    count = 0
    r_row = len(mineboard) #r_row means "range of row"
    r_col = len(mineboard[0])
    
    for row in range(row_input - 1, row_input + 2):
        for col in range(col_input - 1, col_input + 2):
            #if within board and there's a mine...
            if (row >= 0 and row < r_row and col >= 0 and col < r_col):
                if mineboard[row][col]:
                    count += 1
        
    return count


def reveal_adjacent_cells(gameboard, mineboard, row_input, col_input):
    r_row = len(gameboard) #r_row means "range of row"
    r_col = len(gameboard[0])
    
    for row in range(row_input - 1, row_input + 2):
        for col in range(col_input - 1, col_input + 2):
            #if within board and there's a mine...
            if (row >= 0 and row < r_row and col >= 0 and col < r_col) and gameboard[row][col] == '-':
                mine_count = count_adjacent_mines(mineboard, row, col)
                gameboard[row][col] = str(mine_count)
                if mine_count == 0:
                    reveal_adjacent_cells(gameboard, mineboard, row, col)


def reveal_adjacent_cells_graphics(gameboard, mineboard, cells, win, row_input, col_input):
    r_row = len(gameboard)
    r_col = len(gameboard[0])

    for row in range(row_input - 1, row_input + 2):
        for col in range(col_input - 1, col_input + 2):
            if ( row >= 0 and row < r_row and col >= 0 and col < r_col) and gameboard[row][col] == '-':
                mine_count = count_adjacent_mines(mineboard, row, col)
                gameboard[row][col] = str(mine_count)
                cells[row][col].setFill("white")
                if mine_count > 0:
                    label = Text(cells[row][col].getCenter(), str(mine_count))
                    label.draw(win)
                else:
                    reveal_adjacent_cells_graphics(gameboard, mineboard, cells, win, row, col)


def check_win(gameboard, mineboard):
    for row in range(len(gameboard)):
        for col in range(len(gameboard[0])):
            # Check if there are any unopened cells without mines
            if gameboard[row][col] == '-' and not mineboard[row][col]:
                return False
            
    return True

#correction, flagging all mined cells does not win game. only by opening all unmined cells


def gameboard_graphics(i_row, i_col):

    win = GraphWin("Minesweeper", (i_col * 30), i_row * 30)
    ###

    cell_list = []
    for row in range(i_row):
        rowlist = []
        for col in range(i_col):
            rect = Rectangle(Point(col * 30, row * 30), Point((col + 1) * 30, (row + 1) * 30))
            rect.setFill("gray")
            rect.draw(win)
            rowlist.append(rect)
        cell_list.append(rowlist)

    return win, cell_list
    

def select_difficulty_text():
    print("\nLet's play Minesweeper\n")
    print("Difficulty levels:\n"
          "1. Easy (5x6 board with 6 mines)\n"
          "2. Medium (8x10 board with 12 mines)\n")

    dlevel = input("Enter difficulty level: ") #decision level
    dlevel_list = ['1','2']
    while dlevel not in dlevel_list: #input validation
        print("Invalid input. Please choose 1 or 2.")
        dlevel = input("Enter difficulty level: ")

    if dlevel == '1':
        return 5, 6, 6 #i_row, i_col, i_mines
    else:
        return 8, 10, 12


def select_difficulty_graphics():
    print("\nLet's play Minesweeper\n")
    print("Difficulty levels:\n"
          "1. Easy (8x10 board with 10 mines)\n"
          "2. Medium (14x18 board with 40 mines)\n"
          "3. Hard (20x24 board with 99 mines)\n")

    dlevel = int(input("Enter difficulty level: ")) #decision level
    while dlevel != 1 and dlevel != 2 and dlevel != 3: #input validation
        print("Invalid input. Please choose 1 or 2 or 3.")
        dlevel = int(input("Enter difficulty level: "))

    if dlevel == 1:
        return 8, 10, 10 #i_row, i_col, i_mines
    elif dlevel == 2:
        return 14, 18, 40
    else:
        return 20, 24, 99


def main():        

    # Let user choose between text-based or graphics window
    user_decision = input("How do you want to play?: (1) Text-based or (2) Graphics Window: ")
    user_decision = user_decision.strip()
    while user_decision != '1' and user_decision != '2':
        print("Invalid! Must choose 1 or 2")
        user_decision = input("How do you want to play?: (1) Text-based or (2) Graphics Window: ")
        user_decision = user_decision.strip()

    if user_decision == '1':
        i_row, i_col, i_mines = select_difficulty_text()
        gameboard, mineboard = game_and_mine_board(i_row, i_col, i_mines)
        text_based(gameboard, mineboard, i_row, i_col, i_mines)
    else:
        i_row, i_col, i_mines = select_difficulty_graphics()
        gameboard, mineboard = game_and_mine_board(i_row, i_col, i_mines)
        graphics_window(gameboard, mineboard, i_row, i_col, i_mines)
        
main()
