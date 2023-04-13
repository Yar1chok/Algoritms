"""
Модуль содержащий реализацию алгоритма бинарного
поиска в массиве
"""
from __future__ import annotations


def search(array: list, item: object):
    """
    Функция бинарного поиска в массиве
    :param array: массив
    :param item: элемент
    :return: индекс или None
    """
    min = 0
    max = len(array) - 1
    if len(array) == 0:
        return None
    while min < max:
        mid = (min + max) // 2
        if item > array[mid]:
            min = mid + 1
        else:
            max = mid
    if array[max] == item:
        return max
    return None


print(search([2, 3, 3, 3, 3, 3, 3, 4], 3))
