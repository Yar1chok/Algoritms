"""
Smolyaninov Yaroslav, КИ21-17/2Б, variant 2
The Sierpinski triangle fractal. The program draws a fractal with standard settings
that the user can change if desired.
"""
import turtle as t


def main():
    """
    The main function, which is the start of the function
    """
    colors = ['red', 'orange', 'yellow', 'white', 'black', 'blue', 'brown', 'purple', 'pink',
              'green', 'grey']
    menu_options()
    t.setup(width=1200, height=800)
    t.hideturtle()
    t.speed(10)
    size = 400
    generations = 2
    extreme_color = 'black'
    internal_color = 'red'
    while (option := input("*Input the number of menu: ")) != "4":
        if option == '1':
            t.clear()
            t.color(extreme_color)
            t.begin_fill()
            t.forward(size)
            t.left(120)
            t.forward(size)
            t.left(120)
            t.forward(size)
            t.left(120)
            t.end_fill()
            t.getscreen()
            t.color(internal_color)
            t.tracer(False)
            draw_triangle(generations, size)
            t.tracer(True)
        elif option == '2':
            show_settings(internal_color, extreme_color, size, generations)
        elif option == '3':
            show_change_settigns()
            while (point := input("*Your choice: ")) != "0":
                if point == '1':
                    t.speed(check_input_change())
                    break
                elif point == '2':
                    print('*Choose a color: ')
                    print(f'*{colors[0]} - 0\n*{colors[1]} - 1\n*{colors[2]} - 2\n*{colors[3]} - 3\n*{colors[4]} - 4\n'
                          f'*{colors[5]} - 5\n*{colors[6]} - 6\n*{colors[7]} - 7\n*{colors[8]} - 8\n*{colors[9]} - 9\n'
                          f'*{colors[10]} - 10')
                    extreme_color = colors[check_input_change()]
                    break
                elif point == '3':
                    print('*Choose a color: ')
                    print(f'*{colors[0]} - 0\n*{colors[1]} - 1\n*{colors[2]} - 2\n*{colors[3]} - 3\n*{colors[4]} - 4\n'
                          f'*{colors[5]} - 5\n*{colors[6]} - 6\n*{colors[7]} - 7\n*{colors[8]} - 8\n*{colors[9]} - 9\n'
                          f'*{colors[10]} - 10')
                    internal_color = colors[check_input_change()]
                    break
                elif point == '4':
                    size = check_input_digit()
                    break
                elif point == '5':
                    generations = check_input_change()
                    break
                else:
                    print("*Input error, try again.")
        else:
            print("*Input error, try again.")
        menu_options()
    else:
        print("*Program is end.")


def draw_triangle(generation=2, size=200.0):
    """
    This function draw the triangle Serpinskogo. Firstly drawn a large triangle and then drawn three small triangles
    :param generation: Number of generations triangle Serpinskogo
    :param size: The length of triangle
    """
    if generation == 0:
        t.begin_fill()
        t.forward(size)
        t.left(120)
        t.forward(size)
        t.left(120)
        t.forward(size)
        t.left(120)
        t.end_fill()
    else:
        t.begin_fill()
        draw_triangle(generation - 1, size / 2)
        t.end_fill()
        t.forward(size / 2)
        t.begin_fill()
        draw_triangle(generation - 1, size / 2)
        t.end_fill()
        t.left(120)
        t.forward(size / 2)
        t.right(120)
        t.begin_fill()
        draw_triangle(generation - 1, size / 2)
        t.end_fill()
        t.right(120)
        t.forward(size / 2)
        t.left(120)


def menu_options():
    """
    This function outputs the menu text
    """
    print("***Menu***")
    print("*Input 1 to draw triangle with standart settings")
    print("*Input 2 to show standart settings")
    print("*Input 3 to change settings of turtle")
    print("*Input 4 to exit out the program")


def show_settings(internal_color, extreme_color, size, generation):
    """
    This function outputs the default settings
    :param internal_color: The color of big triangle in zero generation
    :param extreme_color: The color of extreme triangles
    :param size: The length of triangle
    :param generation: Number of generations triangle Serpinskogo
    """
    print('*Default settings:')
    print(f'*Default speed of turtle is {t.speed()}')
    print(f'*Default color of extreme turtle is {extreme_color}')
    print(f'*Default color of internal turtle is {internal_color}')
    print(f'*Default size of triangle is {size}')
    print(f'*Default generations value for the triangle is {generation}\n')


def check_input_digit():
    """
    The function checks the input for a digit
    :return: A digit to change params
    """
    menu = True
    while menu:
        print("*Input a digit ", end='')
        change = input()
        if change.isdigit():
            if int(change) > 0:
                return int(change)
        else:
            print("*Error input, try again")


def check_input_change():
    """
    The function checks the input for a digit since zero to ten
    :return: A digit to change params
    """
    menu = True
    while menu:
        print("*Input a digit since 0 to 10: ", end='')
        change = input()
        if change.isdigit():
            if 0 <= int(change) <= 10:
                return int(change)
        else:
            print("*Error input, try again")


def show_change_settigns():
    """
    The function outputs the change menu text
    """
    print("*What you want to change?")
    print("*Input 0 to return menu")
    print("*Input 1 to change speed of turtle")
    print("*Input 2 to change color of extreme turtle")
    print("*Input 3 to change color of internal turtle")
    print("*Input 4 to change size of triangle")
    print("*Input 5 to change the generations value for the triangle")


if __name__ == '__main__':
    main()
