import turtle
import time
import random

WIDHT,HEIGHT = 700,600
COLORS = ['red', 'green', 'blue', 'orange', 'yellow', 'black', 'purple', 'pink', 'brown', 'cyan']

def get_number_of_race():
    racers = 0 
    while True:
        racers = input('Enter the number of racers (2 - 10): ')
        if racers.isdigit():
            racers = int(racers)
        else:
            print('Input is not numeric..Try Again!')
            continue
        if 2 <= racers <= 10:
            return racers 
        else:
            print('Number not in range 2-10.Try again!')
def race(colors):
	turtles = create_turtule(colors)

	while True:
		for racer in turtles:
			distance = random.randrange(1, 20)
			racer.forward(distance)

			x, y = racer.pos()
			if y >= HEIGHT // 2 - 10:
				return colors[turtles.index(racer)]
def create_turtule(colors):
    turtles = []
    spacingx = WIDHT// (len(colors)+1)
    for i,color in enumerate(colors):
        racer = turtle.Turtle()
        racer.color(color)
        racer.shape('turtle')
        racer.left(90)
        racer.penup()
        racer.setpos(-WIDHT//2 + (i+1)*spacingx,-HEIGHT//2 + 20)
        racer.pendown()
        turtles.append(racer)
        
    return turtles

def init_turtle():
    screen = turtle.Screen()
    screen.setup(WIDHT,HEIGHT)
    screen.title('Turtle Racing!')
      
    
racers = get_number_of_race()
colors = COLORS[:racers]
init_turtle()
Winner = race(colors)
print("the winner is the turtle with color", Winner)
time.sleep(10)
            