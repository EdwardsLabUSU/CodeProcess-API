# Hunter Jensen
# CS-1400-LW2 XL
# Assignment 8

# imports
import turtle
import random


# reset
def reset():
    turtle.reset()
    setup()


# setup()
def setup():
    turtle.penup()
    turtle.speed(20)
    turtle.screensize(1000, 800)


# patterns

# draw the rectangle pattern with input
def drawRectanglePattern(centerX, centerY, offset, width, height, count, rotation):
    # set dial (amount each shape is spaced)
    dial = 360 / count
    # start printing loop
    for i in range(count):
        setRandomColor()
        turtle.goto(centerX, centerY)
        turtle.setheading(90)
        turtle.right(dial * i)
        turtle.forward(offset)
        turtle.right(rotation)
        turtle.pendown()
        # call drawRectangle
        drawRectangle(width, height)
        turtle.penup()


def drawRectangle(width, height):
    # draws one rectangle
    turtle.forward(height)
    turtle.right(90)
    turtle.forward(width)
    turtle.right(90)
    turtle.forward(height)
    turtle.right(90)
    turtle.forward(width)


# draws circle pattern
def drawCirclePattern(centerX, centerY, offset, radius, count):
    # set dial (amount each shape is spaced)
    dial = 360 / count
    # start print loop
    for z in range(count):
        setRandomColor()
        turtle.goto(centerX, centerY)
        turtle.setheading(90)
        turtle.right(dial * z)
        turtle.forward(offset)
        turtle.pendown()
        turtle.circle(radius)
        turtle.penup()


def drawSuperPattern(num):
    # draws a random assortment of patterns
    for y in range(num):
        # assign random values
        centerX = random.randint(-500, 500)
        centerY = random.randint(-400, 400)
        offset = random.randint(0, 100)
        count = random.randint(0, 100)
        radius = random.randint(0, 100)
        width = random.randint(0, 100)
        height = random.randint(0, 100)
        rotation = random.randint(-90, 90)
        # decide circle or rectangle
        circRec = random.randint(0, 1)
        if circRec == 1:
            drawCirclePattern(centerX, centerY, offset, radius, count)
        else:
            drawRectanglePattern(centerX, centerY, offset, width, height, count, rotation)


# color
def setRandomColor():
    turColor = random.randint(0, 4)
    if turColor == 1:
        turtle.color("red")
    elif turColor == 2:
        turtle.color("blue")
    elif turColor == 3:
        turtle.color("green")
    elif turColor == 4:
        turtle.color("orange")
    else:
        turtle.color("purple")


# done
def done():
    turtle.done()
##########TESTZONE############

# setup()

# centerX, centerY, offset, width, height, count, rotation, radius = 50,10,20,40,50,40,45,25

# drawRectanglePattern(centerX, centerY, offset, width, height, count, rotation)
# turtle.reset()
# setup()
# drawCirclePattern(centerX, centerY, offset, radius, count)
# turtle.done()
