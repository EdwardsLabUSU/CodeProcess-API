# Hunter Jensen
# CS-1400-LW2 XL
# Assignment 8

#### Add Import Statement(s) as needed ####
import random
import pattern
import turtle
#### End Add Import Statement(s) ####

def main():
    # Setup pattern
    pattern.setup()
    # Play again loop
    playAgain = True

    while playAgain:
        # Present a menu to the user
        # Let them select 'Super' mode or 'Single' mode
        print("Choose a mode")
        print("1) Rectangle Pattern")
        print("2) Circle Pattern")
        print("3) Super Pattern")
        mode = eval(input("Which mode do you want to play? 1, 2 or 3: "))

        # If they choose 'Rectangle Patterns'
        if mode == 1:
            #### Add Input Statement(s) as needed ####
            centerX, centerY = eval(input("enter a center point(X, Y)"))
            offset = eval(input("offset?"))
            width = eval(input("width?"))
            height = eval(input("height?"))
            count = eval(input("count?"))
            rotation = eval(input("rotation?"))
            #### End Add Inputs Statement(s) ####


            # Draw the rectangle pattern
            pattern.drawRectanglePattern(centerX, centerY, offset, width, height, count, rotation)

        # If they choose 'Circle Patterns'
        elif mode == 2:
            #### Add Input Statement(s) as needed ####
            centerX, centerY = eval(input("enter a center point(X, Y)"))
            offset = eval(input("offset?"))
            radius = eval(input("radius?"))
            count = eval(input("count?"))
            #### End Add Inputs Statement(s) ####

            # Draw the circle pattern
            pattern.drawCirclePattern(centerX, centerY, offset, radius, count)

        # If they choose 'Super Patterns'
        elif mode == 3:
            #### Add Input Statement(s) as needed ####
            num = input("number?")
            #### End Add Inputs Statement(s) ####
            if num == "":
                pattern.drawSuperPattern()
            else:
                pattern.drawSuperPattern(eval(num))

        # Play again?
        print("Do you want to play again?")
        print("1) Yes, and keep drawings")
        print("2) Yes, and clear drawings")
        print("3) No, I am all done")
        response = eval(input("Choose 1, 2, or 3: "))

        #### Add Statement(s) to clear drawings and play again ####
        if response == 3:
            playAgain = False
        elif response == 2:
            pattern.reset()
        #### End Add Inputs Statement(s) ####

    # print a message saying thank you
    print("Thanks for playing!")
    pattern.done()


main()
