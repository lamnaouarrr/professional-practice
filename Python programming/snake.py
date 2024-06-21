from tkinter import *  #import tkinter library for gui elements
import random  #import random library for generating random numbers

#constants
GAME_WIDTH=400  #set game window width
GAME_HEIGHT=400  #set game window height
SPEED=100  #adjusted speed for playability
SPACE_SIZE=20  #set size of each part of the snake and food
BODY_PARTS=3  #initial body parts of the snake
SNAKE_COLOR="#2ecc71"  #color of the snake
FOOD_COLOR="#e74c3c"  #color of the food
BACKGROUND_COLOR="#2c3e50"  #background color of the game window
GAME_OVER_BG_COLOR="#16a085"  #background color when the game is over
GAME_OVER_TEXT_COLOR="#e67e22"  #text color when the game is over
REPLAY_TEXT_COLOR="#ecf0f1"  #replay text color when the game is over

class Snake:  #class representing the snake
    def __init__(self):  #initialize the snake
        self.body_size=BODY_PARTS  #set the initial body size of the snake
        self.coordinates=[]  #list to store the coordinates of the snake's body parts
        self.squares=[]  #list to store the square objects representing the snake's body

        for i in range(0, BODY_PARTS):  #initialize the coordinates of the snake's body
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:  #create the squares for the snake's body
            square=canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:  #class representing the food
    def __init__(self):  #initialize the food
        x=random.randint(0, (GAME_WIDTH // SPACE_SIZE)-1) * SPACE_SIZE  #generate random x coordinate
        y=random.randint(0, (GAME_HEIGHT // SPACE_SIZE)-1) * SPACE_SIZE  #generate random y coordinate

        self.coordinates=[x, y]  #set the coordinates of the food

        canvas.create_oval(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=FOOD_COLOR, tag="food")  #create the oval representing the food

def next_turn(snake, food):  #function to handle the next turn of the game
    try:
        x, y=snake.coordinates[0]  #get the current head position of the snake

        if direction=="up":  #move the snake up
            y-=SPACE_SIZE
        elif direction=="down":  #move the snake down
            y+=SPACE_SIZE
        elif direction=="left":  #move the snake left
            x-=SPACE_SIZE
        elif direction=="right":  #move the snake right
            x+=SPACE_SIZE

        x=(x+GAME_WIDTH) % GAME_WIDTH  #wrap around if the snake goes out of the window horizontally
        y=(y+GAME_HEIGHT) % GAME_HEIGHT  #wrap around if the snake goes out of the window vertically

        snake.coordinates.insert(0, (x, y))  #insert new head position

        square=canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOR)  #create new square for the new head
        snake.squares.insert(0, square)

        if x==food.coordinates[0] and y==food.coordinates[1]:  #check if the snake eats the food
            global score

            score+=1  #increase score
            label.config(text="Score:{}".format(score))  #update score label

            canvas.delete("food")  #remove the old food
            food=Food()  #create new food
        else:
            del snake.coordinates[-1]  #remove the last part of the snake's body
            canvas.delete(snake.squares[-1])  #delete the last square
            del snake.squares[-1]  #remove the last square from the list

        if check_collisions(snake):  #check for collisions
            game_over()  #end the game if collision occurs
        else:
            window.after(SPEED, next_turn, snake, food)  #schedule the next turn
    except Exception as e:
        print(f"Error: {e}")  #print any errors

def change_direction(new_direction):  #function to change the direction of the snake
    global direction
    if new_direction=='left' and direction!='right':  #change to left if not currently moving right
        direction=new_direction
    elif new_direction=='right' and direction!='left':  #change to right if not currently moving left
        direction=new_direction
    elif new_direction=='up' and direction!='down':  #change to up if not currently moving down
        direction=new_direction
    elif new_direction=='down' and direction!='up':  #change to down if not currently moving up
        direction=new_direction

def check_collisions(snake):  #function to check for collisions
    x, y=snake.coordinates[0]  #get the head position of the snake

    for body_part in snake.coordinates[1:]:  #check if the head collides with the body
        if x==body_part[0] and y==body_part[1]:
            return True

    return False

def game_over():  #function to handle game over
    canvas.delete(ALL)  #clear the canvas
    canvas.create_rectangle(0, 0, GAME_WIDTH, GAME_HEIGHT, fill=GAME_OVER_BG_COLOR, tag="gameover")  #create game over background
    canvas.create_text(GAME_WIDTH//2, GAME_HEIGHT//2-40, text="GAME OVER", fill=GAME_OVER_TEXT_COLOR, font=("Arcade", 40), tag="gameover_text")  #create game over text
    canvas.create_text(GAME_WIDTH//2, GAME_HEIGHT//2+20, text="CLICK TO REPLAY", fill=REPLAY_TEXT_COLOR, font=("Arcade", 20), tag="replay_text")  #create replay text
    canvas.bind("<Button-1>", restart_game)  #bind click to restart game

def restart_game(event):  #function to restart the game
    canvas.unbind("<Button-1>")  #unbind click event
    start_game()  #start a new game

def start_game():  #function to start the game
    global snake, food, score, direction
    canvas.delete(ALL)  #clear the canvas
    score=0  #reset score
    direction='down'  #set initial direction
    label.config(text="Score:{}".format(score))  #update score label
    snake=Snake()  #create new snake
    food=Food()  #create new food
    next_turn(snake, food)  #start the game loop

window=Tk()  #create main window
window.title("Snake game by LAMNAOUAR AYOUB")  #set window title
window.resizable(False, False)  #make window non-resizable

icon=PhotoImage(file='asclepius.png')  #load window icon
window.iconphoto(True, icon)  #set window icon

score=0  #initialize score
direction='down'  #initialize direction

label=Label(window, text="Score:{}".format(score), font=('consolas', 20))  #create score label
label.pack()  #add score label to window

canvas=Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)  #create game canvas
canvas.pack()  #add canvas to window

window.update()  #update window

window_width=window.winfo_width()  #get window width
window_height=window.winfo_height()  #get window height
screen_width=window.winfo_screenwidth()  #get screen width
screen_height=window.winfo_screenheight()  #get screen height

x=int((screen_width/2)-(window_width/2))  #calculate x position for centering window
y=int((screen_height/2)-(window_height/2))  #calculate y position for centering window

window.geometry(f"{window_width}x{window_height}+{x}+{y}")  #set window position

window.bind('<Left>', lambda event: change_direction('left'))  #bind left arrow key to change direction
window.bind('<Right>', lambda event: change_direction('right'))  #bind right arrow key to change direction
window.bind('<Up>', lambda event: change_direction('up'))  #bind up arrow key to change direction
window.bind('<Down>', lambda event: change_direction('down'))  #bind down arrow key to change direction

start_game()  #start the game

window.mainloop()  #run the main loop
