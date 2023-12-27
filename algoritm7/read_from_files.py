from typing import List
from PIL import Image


def reading_maze_from_text(path_to_file: str) -> List[List[str]]:
    """
    Reads a maze from a text file and returns it as a list of lists of strings
    :param path_to_file: The path to the text file with the maze
    :return: A list of string lists representing a maze
    """
    maze = []
    with open(path_to_file, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                maze.append(list(line.strip()))
    return maze


def reading_maze_from_text_binary(path_to_file: str) -> list[list[int]]:
    """
    Reads a maze from a text file and returns it as a list of lists of strings
    :param path_to_file: The path to the text file with the maze
    :return: A list of string lists representing a maze
    """
    maze = []
    with open(path_to_file, "r", encoding="utf-8") as file:
        for line in file:
            row = [int(cell) for cell in line.replace(",", '').replace("[", '').replace("]", '').replace("\n", '')
            .split()]
            maze.append(row)
    return maze


def get_square_size(path_to_file: str) -> int:
    """
    The function calculates the size of the square in the maze image
    :param path_to_file: The path to the maze image file
    :return: The size of the square in pixels
    """
    with Image.open(path_to_file) as img:
        width, height = img.size
        for i in range(width):
            for j in range(height):
                if img.getpixel((i, j)) == (255, 255, 255):
                    diagonal = ((i ** 2 + j ** 2) ** 0.5)
                    square_size = int(diagonal / (2 ** 0.5))
                    return square_size


def reading_maze_from_image(path_to_file: str) -> List[List[str]]:
    """
    The function reads the maze from the image and returns it as a list of lists of strings
    :param path_to_file: The path to the maze image file
    :return: A list of string lists representing a maze
    """
    with Image.open(path_to_file) as img:
        maze = []
        square_size = get_square_size(path_to_file)
        for i in range(0, img.size[1], square_size):
            row = []
            for j in range(0, img.size[0], square_size):
                square = img.crop((j, i, j + square_size, i + square_size))
                if (0, 0, 0) in [color[1] for color in square.getcolors()]:
                    row.append('|')
                else:
                    row.append('')
            maze.append(row)
    return maze
