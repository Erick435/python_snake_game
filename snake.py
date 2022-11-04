import curses
from random import randint

#This will be our setup window
curses.initscr()
win = curses.newwin(20, 60, 0, 0) # y is first, then x coordinate
#20 lines, 60 columns, starting point at 0, 0

win.keypad(1) #arrow keys
curses.noecho() #to not listen to other input characters

#to hide curses do the following below
curses.curs_set(0)

win.border(0)
win.nodelay(1) #waiting for input, maybe play with this to learn more

#------ the window is now setup -----------

#Snake and food
snake = [(4, 10), (4, 9), (4, 8)]  #creating a tuple since it's immutable
    #this is the initial coordinate
food = (10, 20)

#Starting game logic
score = 0 #score starts at 0

#Game will keep running until the user presses the ESC key which is 27 in the curses module
ESC = 27
key = curses.KEY_RIGHT  #This makes the snake starting movement go to the right


while key != ESC: 
    win.addstr(0, 2, 'Score ' + str(score) + ' ')

    #When snake get bigger, the speed will increase (below)
    win.timeout(150 - (len(snake)) // 5 + len(snake) // 10 % 120)

    prev_key = key
    event = win.getch() #get the next character
    key = event if event != -1 else prev_key
    
    if key not in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN, ESC]:
        key = prev_key

    #find the next coord for the snake
    y = snake[0][0]
    x = snake[0][1]
    if key == curses.KEY_DOWN:
        y += 1
    if key == curses.KEY_UP:
        y -= 1
    if key == curses.KEY_LEFT:
        x -= 1
    if key == curses.KEY_RIGHT:
        x += 1

    snake.insert(0,(y, x)) #this is the new head in the beginning

    #we check if we hit the border
    if y == 0:
        break
    if y == 19: 
        break
    if x == 0:
        break
    if x == 59:
        break

    #check if snake hits itself
    if snake[0] in snake[1:]:
        break

    #check if snake consumes food
    if snake[0] == food:
        score += 1
        food = ()
        while food == ():
            food = (randint(1, 18), randint(1, 58))
            if food in snake:
                food = ()
        win.addch(food[0], food[1], '#')
    else:
        last = snake.pop()
        win.addch(last[0], last[1], ' ')
    
    win.addch(snake[0][0], snake[0][1], 'V')

    for coordinate in snake:
        win.addch(coordinate[0], coordinate[1], 'V')

    win.addch(food[0], food[1], '#')

curses.endwin() #destroys the window
print(f"Final score = {score}") #keeps record of final score
