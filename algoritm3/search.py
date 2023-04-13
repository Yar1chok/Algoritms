"""Нахождение подстрок в строке с помощью алгоритма Бойера-Мура-Хорспула"""
from __future__ import annotations


def search(string: str, sub_string: str | list[str],
           case_sensitivity: bool = True,
           method: str = 'first', count: int | None = None
           ) -> tuple[int, ...] | dict[str, tuple[int, ...]]:
    """
    Функция поиска подстроки в строке
    :param string: Введенная строка
    :param sub_string: Введенная подстрока, которую необходимо найти в строке
    :param case_sensitivity: Параметр, отвечающий за регистр строки (Если введен False, строка переводится
    в нижний регистр)
    :param method: Метод поиска подстроки, поиск идет в прямом порядке ('first') или в обратном порядке ('last')
    :param count: Количество совпадений, которые нужно найти в строке
    :return: Словарь или список с найденными подстроками в N-ом месте строки
    """
    if isinstance(sub_string, (list, tuple)) and len(sub_string) == 1:
        sub_string = sub_string[0]

    if isinstance(sub_string, (list, tuple)):
        result_dict = {}
        result_dict.fromkeys(string, )
        for word in sub_string:
            result_dict[word] = boyer_moore_horsepool(string, word, case_sensitivity, method, count)
        return result_dict if not all(v is None for v in result_dict.values()) else None
    elif isinstance(sub_string, str):
        return boyer_moore_horsepool(string, sub_string, case_sensitivity, method, count)


def offset_table(sub_string: str) -> dict:
    """
    Функция формирования таблицы смещений для подстроки
    :param sub_string: Введенная строка, которую нужно найти
    :return: Словарь со смещениями символов
    """
    sub_string_len = len(sub_string)
    unique_symbols = set()  # Уникальные (исключающие повторений) символы в образе
    dictionary_offsets = {}  # Словарь смещений, в котором хранятся уникальные символы "Символ" - "Значение"
    for i in range(sub_string_len - 2, -1, -1):  # Пробегаем подстроку с конца
        if sub_string[i] not in unique_symbols:  # Добавление уникального символа в словарь
            dictionary_offsets[sub_string[i]] = sub_string_len - i - 1
            unique_symbols.add(sub_string[i])
    # Формирование последнего символа подстроки
    if sub_string[sub_string_len - 1] not in unique_symbols:
        dictionary_offsets[sub_string[sub_string_len - 1]] = sub_string_len
    # Формирование смещения для других символов для сдвига на длину подстроки
    dictionary_offsets['*'] = sub_string_len
    return dictionary_offsets


def boyer_moore_horsepool(string: str, sub_string: str, case_sensitivity: bool = False,
                          method: str = 'first', count: int | None = None) -> tuple[int, ...] | None:
    """
    Алгоритм Бойера-Мура-Хорспула
    :param string: Введенная строка
    :param sub_string: Введенная подстрока, которую необходимо найти в строке
    :param case_sensitivity: Параметр, отвечающий за регистр строки (Если введен False, строка переводится
    в нижний регистр)
    :param method: Метод поиска подстроки, поиск идет в прямом порядке ('first') или в обратном порядке ('last')
    :param count: Количество совпадений, которые нужно найти в строке
    :return: Словарь или список с найденными подстроками в N-ом месте строки или None, если ничего не нашли/ошибка ввода
    """
    sub_string_len = len(sub_string)
    string_len = len(string)
    if case_sensitivity is False:  # Перевод строки в нижний регистр, если флаг изменен на False
        string = string.lower()
        sub_string = sub_string.lower()
    if sub_string_len > string_len:  # Проверка, если подстрока длиннее строки
        return None
    if isinstance(count, int) and count <= 0:  # Проверка на правильность ввода кол-ва поисков подстрок
        return None

    if method == "last":  # Идем в обратном порядке, поэтому разворачиваем строку и подстроку
        string = string[::-1]
        sub_string = sub_string[::-1]

    dictionary_offsets = offset_table(sub_string)  # Словарь уникальных символов
    k = sub_string_len - 1  # Начинаем поиск с символа, равного длине подстроки
    found_indexes = []
    counter = 0
    if sub_string_len > 1:
        while k < string_len:
            i = 0
            j = 0
            for j in range(sub_string_len - 1, -1, -1):
                if string[k - i] != sub_string[j]:
                    if j == sub_string_len - 1:
                        offset = dictionary_offsets[string[k]] if dictionary_offsets.get(string[k], False) \
                            else dictionary_offsets['*']
                    else:
                        offset = dictionary_offsets[sub_string[j]]
                    k += offset
                    break
                else:
                    i += 1

            # Если подстрока полностью совпала, значит подстрока найдена
            if j == 0 and sub_string_len != 1:
                counter += 1
                if method == "last":
                    found_indexes.append(string_len - (k - i + 1) - sub_string_len)
                else:
                    found_indexes.append(k - i + 1)
                if counter == count:
                    break
                k += (sub_string_len - 1)
    else:  # Если ищем один символ
        k = 0
        found_indexes = []
        counter = 0
        while k < string_len:
            if string[k] == sub_string:
                counter += 1
                if method == "last":
                    found_indexes.append(string_len - k - sub_string_len)
                else:
                    found_indexes.append(k)
                if counter == count:
                    break
                k += 1
            else:
                k += 1

    return tuple(found_indexes) if found_indexes else None


if __name__ == '__main__':
    text = "abobaohoewhvewvbiabobapojfpjfpbob"
    example = "aboba"
    s = boyer_moore_horsepool(text, example, count=2)
    print('Text: ', text)
    print('Pattern: ', example)
    print('Pattern \"' + example + '\" found at position', s)
