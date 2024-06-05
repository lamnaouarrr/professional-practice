import turtle
from turtle import *
from PIL import Image, ImageTk, ImageEnhance

#define the spinner state
state = {'turn': 0}


def draw_triangle(size, color):
    begin_fill()
    fillcolor(color)
    for _ in range(3):
        forward(130)
        left(120)
    end_fill()


def spinner():
    clear() #clear the previous drawing

    angle = state['turn'] / 10 #calculate the angle based on the turn states, to make the spinner turn more smoothly and slowly
    right(angle)
    
    # Draw the red arm
    forward(100)
    draw_triangle(80, 'red')  # Draw a triangle instead of a dot
    back(100)
    right(60)
    
    # Draw the green arm
    forward(140)
    dot(100, 'purple')
    back(140)
    right(60)
    
    # Draw the blue arm
    forward(100)
    draw_triangle(80, 'blue')  # Draw a triangle instead of a dot
    back(100)
    right(60)
    
    # Draw the yellow arm
    forward(140)
    dot(100, 'green') 
    back(140)
    right(60)
    
    # Draw the purple arm
    forward(100)
    draw_triangle(80, 'yellow')  # Draw a triangle instead of a dot
    back(100)
    right(60)
    
    # Draw the orange arm
    forward(140)
    dot(100, 'orange')
    back(140)
    right(60)
    
    #update the screen
    update()

def animate():
    #reduce the turn state of the spinner, causing it to slow down and eventually stop
    if state['turn'] > 0:
        state['turn'] -= 1
    
    spinner() #redraw the spinner with the updated angle
    ontimer(animate, 20) #sets a timer to call the animate function again after 20 milliseconds

def flick():
    #increase the spinner's turn state when a key is pressed
    state['turn'] += 10

#set up the turtle graphics window
setup(520, 520, 370, 0) #sets up the window size and position

#load the custom icon using turtle library
root = turtle.Screen()._root
root.iconbitmap("C:/Users/ayoub/Desktop/CST Bachelor\'s degree at WIT/semester 6/professional practice/professional-practice-codes/Validation_Programming/spinner-icon.ico")
turtle.title('Spinner made by LAMNAOUAR Ayoub')

root.resizable(False, False) #disable window resizing


tracer(False) #turns off automatic screen updates to improve animation performance
hideturtle() #hide turtle's cursor
width(20) #sets the width of the turtle's pen / the "pen" that it uses to draw lines and shapes on the screen
onkey(flick, 'space')
listen() #sets the window to listen for keyboard events
animate()
done() #ends the program and keeps the window open