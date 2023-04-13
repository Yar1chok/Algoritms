"""Интерфейс командной строки с цветным поиском подстрок в строке и считывание из файла"""


import sys
import click
from search import search


def file_reading(file, lock: bool) -> str:
    """
    Считывание строк из файла
    :param file: файл
    :param lock: ограничение на считывание (10 строк)
    :return: полученная строка
    """
    string = ""
    if lock:
        for _ in range(10):
            string += file.readline()
    else:
        string = file.read()
    return string


@click.command()
@click.option("--string", default="", help="Строка для поиска")
@click.option("--sub-string", default=[], multiple=True, help="Подстрока для поиска")
@click.option("--case-sensitivity", "-case", type=click.BOOL,
              default=False, help="Чувствительность к регистру")
@click.option("--method", default="first", type=click.Choice(["first", "last"]),
              help="Метод поиска")
@click.option("--count", default=None, type=click.INT, help="Количество вхождений")
@click.option("--file", type=click.File(mode="r"), default=None, help="Файл для поиска")
@click.option("--lock", default=True, type=click.BOOL, help="Ограничение на 10 строк")
def start_search(string, sub_string, case_sensitivity, method, count, file, lock):
    """
    CLI для вывода и расскараски текста
    :param string: Введенная строка
    :param sub_string: Введенная подстрока, которую необходимо найти в строке
    :param case_sensitivity: Параметр, отвечающий за регистр строки (Если введен False, строка переводится
    в нижний регистр)
    :param method: Метод поиска подстроки, поиск идет в прямом порядке ('first') или в обратном порядке ('last')
    :param count: Количество совпадений, которые нужно найти в строке
    :param file: Путь до файла с исходной строкой
    :param lock: Флаг считывания первых 10 строк из файла
    """
    if file:
        string = file_reading(file, lock)
    try:
        result = search(string, sub_string, case_sensitivity, method, count)
        print(result)
    except ValueError:
        print("Некорректные данные")
        sys.exit()

    colors = ["red", "green", "blue", "yellow", "bright_black", "bright_cyan"]
    indexes = []
    current_index = 0

    if isinstance(result, dict):
        keys = tuple(result.keys())
        for key in result.keys():
            if result[key] is not None:
                for j in result[key]:
                    indexes.append(j)
        indexes = tuple(indexes)
    elif isinstance(result, tuple):
        keys = sub_string
        indexes = tuple(result)
    else:
        click.echo(message=string)
        return None
    while current_index < len(string):
        if current_index in indexes:
            for i, key in enumerate(keys):
                current_str = string[current_index:current_index + len(key)]
                if not case_sensitivity:
                    current_str = current_str.lower()
                    key = key.lower()
                if current_str == key:
                    click.echo(click.style(text=string[current_index:current_index + len(key)],
                                           bg=colors[i % 6]), color=True, nl=False)
                    current_index += len(key)
                    break
        else:
            click.echo(click.style(text=string[current_index]), color=True, nl=False)
            current_index += 1


if __name__ == "__main__":
    start_search()
