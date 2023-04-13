"""
Смолянинов Ярослав Евгеньевич, КИ21-17/2Б, Практическая работа №5
Вариант 4 - Многофазная сортировка (Фибоначчиевая)
"""
import click
import pathlib
from typing import *
from multiphase_sort import multiphase_sort

PathType = Union[str, pathlib.Path]


@click.command()
@click.option("--file", default="test.txt", help="Имя файла с неотсортированными данными")
@click.option("--out-file", default=None, help="Файл для записи отсортированных данных")
@click.option("--flag", default=False, help="Флаг для сортировки")
@click.option("--key", default=None, help="Метод поиска")
@click.option("--key-csv", default="", help="Метод поиска для csv файлов")
@click.option("--streams", default=3, help="Файл для поиска")
@click.option("--type-data", default="i", help="Тип данных для сортировки")
def start_sort(file, out_file, flag, key, key_csv, streams, type_data):
    """
    CLI Для запуска алгоритима многофазной сортировки
    :param file: Передаем имя файла с неотсортированными данными или лист с именами файлов
    :param out_file: Передаем имя файла, в который запишутся отсортированные данные
    :param flag: Параметр, отвечающий за тип сортровки - по неубыванию и по невозрастанию
    :param key: Функция, вычисляющая значение, на основе которого будет производится сортировка
    :param key_csv: Функция для сортировки csv файлов
    :param streams: Количество потоков
    :param type_data: Тип сортируемых данных
    :return: Отсортированные данные в файл out_file
    """
    multiphase_sort(file, out_file, flag, key, key_csv, streams, type_data)
    print("Data was sorted!")


if __name__ == "__main__":
    start_sort()
