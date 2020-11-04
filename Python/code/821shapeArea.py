
import math

def get_area(shape):

    # switch the lowercase for easy comparison

    shape = shape.lower()

    if shape == 'rectangle':
        rectangle_area()
    elif shape == 'circle':
        circle_area()
    else:
        print("Please enter rectangle or circle")

# Create function that calculates the rectangle area
def rectangle_area():
    length = float(input("Enter the length: "))
    width = float(input("Enter the width: "))

    area = length * width
    print("The area of the rectangle is", area)

# Create function that calculate the circle area
def circle_area():

    radius = float(input("Enter the radius: "))

    area = math.pi * math.pow(radius, 2)

    print("The area of circle is {:.2f}".format(area))


# Ask the user what shape they want
shape_type = input("Get area for what shape: ")


# Call a function that will route to the correct function
get_area(shape_type)