"""
Console implementation of working with a maze
Смолянинов Ярослав Евгеньевич, КИ21-17/2Б, Практическая работа №7
Генерация лабиринта вариант 6 - Рекурсивный алгоритм сегментации
Решение генерации вариант 3 - Jump Point Search
"""
import click
from maze import MazeGenerator, jump_point_search, path_first_last
from read_from_files import reading_maze_from_text_binary


@click.command()
@click.option("--width", "-w", type=click.INT, help='Ширина лабиринта')
@click.option("--height", "-h", type=click.INT, help="Высота лабиринта")
@click.option("--tackle-maze", "-tm", type=click.INT, multiple=True, default=[],
              help="x, y для стартовой и финальной координат для решения лабиринта")
@click.option("--first-last", "-fl", is_flag=True, default=False,
              help="Вывести путь от первой свободной точки до последней свободной точки")
@click.option("--save", "-s", help='Файл для сохранения лабиринта', default=None)
@click.option("--draw", "-d", is_flag=True, default=False, help='Отрисовка лабиринта в модуле Pygame')
@click.option("--read-file", "-rf", default=None, help='Чтение лабиринта из файла')
def cli_maze(width: int, height: int, tackle_maze: list, first_last: bool, save: str, draw: bool, read_file: str):
    """
    Working with the maze in the console
    :param draw: Drawing a maze using the Pygame module
    :param width: Width of the maze
    :param height: Height of the maze
    :param tackle_maze: Array with a starting point and an ending point, to find a path between them
    :param first_last: Flag for finding the path from the first to the last free point
    :param save: The name of the file to save the maze
    :param read_file: The path to the file to read the maze
    """
    if read_file:
        if read_file:
            labyrinth_bin = reading_maze_from_text_binary(read_file)
            for row in labyrinth_bin:
                print(row)
            path, distance = path_first_last(labyrinth_bin)
            if path:
                click.echo(f"The path from the first free to the last free: {path}\nDistance traveled: {distance}")
            else:
                click.echo("The path from the first free point to the last free point does not exist")
        else:
            click.echo("Error in specifying the path to the file!")
    else:
        labyrinth = MazeGenerator(width, height)
        labyrinth.generate()
        labyrinth.print_maze()
        if draw:
            labyrinth.draw_maze()
        if save:
            labyrinth.save_maze_image(save)
        if len(tackle_maze) == 4:
            start = (tackle_maze[0], tackle_maze[1])
            end = (tackle_maze[2], tackle_maze[3])
            labyrinth_bin = labyrinth.convert_maze_to_binary()
            path, distance = jump_point_search(labyrinth_bin, start, end)
            if not path:
                click.echo(f"Path from {start} to {end} not exist")
            else:
                click.echo(f"Path from {start} to {end}: {path}\nDistance traveled: {distance}")
        if first_last:
            labyrinth_bin = labyrinth.convert_maze_to_binary()
            path, distance = path_first_last(labyrinth_bin)
            if path:
                click.echo(f"The path from the first free to the last free: {path}\nDistance traveled: {distance}")
            else:
                click.echo("The path from the first free point to the last free point does not exist")
