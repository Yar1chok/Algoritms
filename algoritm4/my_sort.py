from typing import Optional, Callable


def find_minrun(len_array):
    """
    Поиск наименьшего размера отсортированного массива
    :param len_array: Длина массива
    :return: Количество минранов
    """
    MINIMUM = 32
    r = 0
    while len_array >= MINIMUM:
        r |= len_array & 1
        len_array >>= 1
    return len_array + r


def insertion_sort_descending(array, left, right, key: Optional[Callable]):
    """
    Сортировка по убыванию
    :param array: Введенный массив
    :param left: Первый элемент в массиве
    :param right: Последний элемент в массиве
    :param key: Функция для нахождения значения элемента
    :return: Отсортированынй массив
    """
    for i in range(left + 1, right + 1):
        element = array[i]
        j = i - 1
        while element > key(array[j]) and j >= left:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = element
    return array


def insertion_sort_ascending(array, left, right, key: Optional[Callable]):
    """
    Сортировка по возрастанию
    :param array: Введенный массив
    :param left: Первый элемент в массиве
    :param right: Последний элемент в массиве
    :param key: Функция для нахождения значения элемента
    :return: Отсортированынй массив
    """
    for i in range(left + 1, right + 1):
        element = array[i]
        j = i - 1
        while element < key(array[j]) and j >= left:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = element
    return array


def merge(array, len_array, middle_element, right_element):
    """
    Сортировка слияние частей массива
    :param array: Введенный массив
    :param len_array: Длина массива
    :param middle_element: Средний элемент
    :param right_element: Последний элемент
    """
    array_length1 = middle_element - len_array + 1
    array_length2 = right_element - middle_element
    left = []
    right = []
    for first_counter in range(0, array_length1):
        left.append(array[len_array + first_counter])
    for first_counter in range(0, array_length2):
        right.append(array[middle_element + 1 + first_counter])

    first_counter = 0
    second_counter = 0
    k = len_array

    while second_counter < array_length2 and first_counter < array_length1:
        if left[first_counter] <= right[second_counter]:
            array[k] = left[first_counter]
            first_counter += 1

        else:
            array[k] = right[second_counter]
            second_counter += 1

        k += 1

    while first_counter < array_length1:
        array[k] = left[first_counter]
        k += 1
        first_counter += 1

    while second_counter < array_length2:
        array[k] = right[second_counter]
        k += 1
        second_counter += 1


def tim_sort(array, reverse: bool, key: Optional[Callable], cmp: Optional[Callable]):
    """
    Сортировка Тима Петерсона
    :param array: Введенный массив
    :param reverse: Флаг обратной сортировки
    :param key: Функция для нахождения значения элемента
    """
    len_array = len(array)
    minrun = find_minrun(len_array)

    for start in range(0, minrun):
        end = min(start + minrun - 1, len_array - 1)
        if reverse:
            insertion_sort_descending(array, start, end, key)
        else:
            insertion_sort_ascending(array, start, end, key)

    size = minrun
    while size < len_array:
        for left in range(0, len_array, 2 * size):
            mid = min(len_array - 1, left + size - 1)
            right = min((left + 2 * size - 1), (len_array - 1))
            merge(array, left, mid, right)
        size *= 2


def my_sort(array: list, reverse: bool = False, key: Optional[Callable] = None, cmp: Optional[Callable] = None) -> list:
    """
    Получение отсортированного списка
    :param array: Введенный массив
    :param reverse: Флаг обратной сортировки
    :param key: Функция для нахождения значения элемента
    :param cmp: Функция для сравнивания элементов
    :return: отсортированный список
    """
    if key is None:
        key = lambda a: a
    if cmp is None:
        cmp = lambda a, b: a < b
    tim_sort(array, reverse, key, cmp)
    return array
