"""
Смолянинов Ярослав Евгеньевич, КИ21-17/2Б, Практическая работа №6
Вариант 2 - Сжатие изображений
"""
import click
from matplotlib.image import imread
from tree import QuadTree, make_gif, save_img


@click.command()
@click.option("--image", '--i', required=True, help="Имя файла с исходной картинкой")
@click.option("--insert", '-ins', type=click.INT, multiple=True, help="Вставить линию (принимает 4 аргумента (R, G, B) и "
                                                              "значение координаты)")
@click.option("-insertXY", '-insXY', type=click.Choice(['x', 'y']), help="Выбор оси для добавления")
@click.option("--delete", '--del', type=click.INT, help="Удалить линию (принимает координату y и/или x для удаления линий по "
                                               "этим координатам)")
@click.option("-deleteXY", '-delXY', type=click.Choice(['x', 'y']), help="Выбор оси для удаления")
@click.option("--gif", is_flag=True, help='Сделать гифку', default=False)
@click.option("--area", '--a', type=click.INT, multiple=True, help="Выбрать область (принимает координаты x_start, "
                                                            "y_start, x_finish, y_finish)")
@click.option("--level", '--l', type=click.INT, help="Уровень нормальности", default=5)
def cli_tree(image: str, level: int, insertxy: str, deletexy: str, gif: bool, insert: list = None, delete: int = None,
             area: list = None):
    """
    Реализация работы с квадродеревом для командной строки
    :param image: путь к картинке
    :param level: уровень нормирования
    :param insertxy: ось по которой вставить линию (x или y)
    :param deletexy: ось по которой удалить линию (x или y)
    :param gif: флаг для создания гифки
    :param insert: цвет для созданной линии и значение координаты для вставки
    :param delete: значение координаты для удаления
    :param area: координаты для выделения области
    """
    array_image = imread(image)
    quad_tree = QuadTree(array_image)
    if insert:
        if insertxy == "x":
            quad_tree.insert(insert[0:3], x_coor=insert[3])
        elif insertxy == "y":
            quad_tree.insert(insert[0:3], y_coor=insert[3])
    if delete:
        if deletexy == "x":
            quad_tree.delete(x_coor=delete)
        elif deletexy == "y":
            quad_tree.delete(y_coor=delete)
    if area:
        quad_tree.area(area[0], area[1], area[2], area[3])
    quad_tree.subdivide()
    if gif:
        make_gif(quad_tree)
    save_img(quad_tree, level)


if __name__ == "__main__":
    cli_tree()
