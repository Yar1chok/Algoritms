import pathlib
from typing import *
import os
import csv

PathType = Union[str, pathlib.Path]


def first_distribution(src: PathType, sequence: int, file_names, cmp):
    """
    Первичное фибоначчиевое распределение
    :param src: исходный файл
    :param sequence: количество файлов (последовательностей)
    :param file_names: имена файлов
    :param cmp: лямбда функция сравнения
    """
    flag = True
    line_order = [1] * sequence
    line_order_copy = line_order.copy()
    last_lines = [0] * sequence
    with open(src, "r") as stream:
        line = stream.readline().replace("\n", "")
        if not line:
            return -1, -1
        for i in range(sequence):
            with open(file_names[i], "a") as file:  # открытие файлов
                file.write(line + "\n")
                last_lines[i] = line
                line = stream.readline().replace("\n", "")
                if not line:
                    line_order_copy[i] -= 1
                    return 1, line_order_copy
                while cmp(last_lines[i], line):
                    file.write(line + "\n")
                    last_lines[i] = line
                    line = stream.readline().replace("\n", "")
                    if not line:
                        line_order_copy[i] -= 1
                        return 1, line_order_copy
                line_order_copy[i] -= 1
                level = 1
        if not line:
            flag = False
        while flag:
            line_order_copy = line_order.copy()
            line_order = line_order_next(line_order)
            line_order_copy = [(line_order[i] - line_order_copy[i]) for i in range(sequence)]
            level += 1
            i = 0
            while max(line_order_copy) > 0:
                with open(file_names[i], "a") as file:
                    if cmp(last_lines[i], line):
                        line_order_copy[i] += 1
                    file.write(line + "\n")
                    last_lines[i] = line
                    line = stream.readline().replace("\n", "")
                    if not line:
                        line_order_copy[i] -= 1
                        flag = False
                        break
                    while cmp(last_lines[i], line):
                        file.write(line + "\n")
                        last_lines[i] = line
                        line = stream.readline().replace("\n", "")
                        if not line:
                            line_order_copy[i] -= 1
                            flag = False
                            break
                    if flag:
                        line_order_copy[i] -= 1
                        if (i != sequence - 1) and line_order_copy[i + 1] > line_order_copy[i]:
                            i += 1
                        else:
                            i = line_order_copy.index(line_order_copy[i])
                    else:
                        break
    return level, line_order_copy


def multiphase_sort(src: Union[PathType, list[PathType]], output: PathType = None, reverse: bool = False,
                    key_opt: Optional[Callable] = lambda a: a, key_csv: str = "", nflows: int = 3,
                    type_data: str = "i") -> None:
    """
    Многофазная сортировка (Фибоначчиевая)
    :param src: Исходный файл
    :param output: Выходной файл, если не указан файл src сортируется на месте
    :param reverse: Флаг определяющий вариант сортировки
    :param key_opt: Функция, вычисляющая значение, на основе которого будет производится сортировка.
    :param key_csv: Столбец для csv по которому производится сортировка
    :param nflows: Количество потоков
    :param type_data: Тип сортируемых данных
    """
    if isinstance(src, list):  # Проверка на список файлов
        if not output:
            for i in src:
                multiphase_sort(i, i, reverse, key_opt, key_csv, nflows, type_data)
            return
        else:
            if src[0][len(src[0]) - 3:] == "txt":
                open("new_stream.txt", "w").close()
                with open("new_stream.txt", "a") as new_src:
                    for i in src:
                        with open(i, "r") as file:
                            line = file.readline()
                            while line:
                                new_src.write(line)
                                line = file.readline()
                src = "new_stream.txt"
            elif src[0][len(src) - 3:] == "csv":
                open("new_stream.csv", "w").close()
                with open("new_stream.csv", "a") as new_src:
                    file_writer = csv.writer(new_src)
                    for i in src:
                        with open(i, "r") as file:
                            file_reader = csv.reader(file, delimiter=",")
                            for j in file_reader:
                                file_writer.writerow(j)
                src = "new_stream.txt"
            else:
                raise ValueError("Неверный формат файлов")
    if src[len(src) - 3:] == "csv":  # Проверка на файл с расширением "csv"
        if output and output[len(output) - 3:] != "csv":
            raise ValueError("Неверный формат файлов")
        multiphase_sort_csv(src, output, reverse, key_opt, key_csv, nflows, type_data)
        return
    if output and output[len(output) - 3:] != "txt":  # Проверка на файл с расширением "txt"
        raise ValueError("Неверный формат файлов")
    if not key_opt:  # Проверка на отсутствие функции
        key_opt = lambda a: a
    if nflows < 3:  # Проверка на кол-во потоков
        raise ValueError("Количество потоков должно быть не меньше 3")
    if type_data == "i":  # Проверка на тип "цисло"
        key = lambda a: key_opt(int(a))
    elif type_data == "f":  # Проверка на вещественные числа
        key = lambda a: key_opt(float(a))
    elif type_data == "s":  # Проверка на строки
        key = lambda a: key_opt(a)
    else:
        raise ValueError("Некорректный тип")
    file_names = []
    # Создание файлов для сортировки
    for i in range(1, nflows + 1):
        file_name = "sort" + str(i) + ".txt"
        file_names.append(file_name)
        open(file_name, "w", encoding="utf-8").close()
    cmp = lambda a, b: key(a) <= key(b)
    if reverse:
        cmp = lambda a, b: key(a) >= key(b)
    level, zero_series = first_distribution(src, nflows - 1, file_names[:len(file_names) - 1], cmp)
    if level != -1 and zero_series != -1:
        first = lambda a: min(a)
        cmp = lambda a, b: a <= b
        if reverse:
            cmp = lambda a, b: a >= b
            first = lambda a: max(a)
        zero_series.append(0)
        output_file_index = nflows
        while level != 0:
            output_file_index = (output_file_index - 1)
            if output_file_index < 0:
                output_file_index = nflows - 1
            input_files_indexes_1 = [i for i in range(0, nflows)]
            input_files_indexes_1.remove(output_file_index)
            flag_2 = True
            while flag_2:
                if min([zero_series[i] for i in input_files_indexes_1]) != 0:
                    for i in input_files_indexes_1:
                        zero_series[i] -= 1
                    zero_series[output_file_index] += 1
                    continue
                input_files_indexes_2 = []
                for i in input_files_indexes_1:
                    if zero_series[i] == 0:
                        input_files_indexes_2.append(i)
                    else:
                        zero_series[i] -= 1
                while len(input_files_indexes_2) != 0:
                    elements = []
                    for i in input_files_indexes_2.copy():
                        with open(file_names[i], "r") as f:
                            line = f.readline()
                            if line and line != "" and line != "\n":
                                elements.append(key(line.replace("\n", "")))
                            else:
                                input_files_indexes_2.remove(i)
                    if len(elements) == 0:
                        break
                    elem = first(elements)
                    elem_file_index = input_files_indexes_2[elements.index(elem)]
                    with open(file_names[output_file_index], "a") as output_file:
                        output_file.write(str(elem) + "\n")
                    with open(file_names[elem_file_index], "r") as f:
                        f.readline()
                        with open('stream1.txt', "w") as tempf:
                            line = f.readline()
                            while line:
                                tempf.write(line)
                                line = f.readline()
                    os.replace('stream1.txt', file_names[elem_file_index])
                    with open(file_names[elem_file_index], "r") as f:
                        line = f.readline()
                        if not line:
                            input_files_indexes_2.remove(elem_file_index)
                        elif not cmp(elem, key(line.replace("\n", ""))):
                            input_files_indexes_2.remove(elem_file_index)
                with open(file_names[output_file_index - 1], "r") as f:
                    if zero_series[output_file_index - 1] == 0 and not f.readline():
                        flag_2 = False
                        level -= 1
    else:
        delete_files(file_names, src)
        return

    if not output:
        output = src
    with open(output, "w") as result_file:
        with open(file_names[output_file_index], "r") as output_file:
            while True:
                line = output_file.readline()
                if line:
                    result_file.write(line)
                else:
                    break
    delete_files(file_names, src)


def multiphase_sort_csv(src: Union[PathType, list[PathType]], output: PathType = None, reverse: bool = False,
                        key_opt: Optional[Callable] = lambda a: a, key_csv: str = "", nflows: int = 3,
                        type_data: str = "i") -> None:
    """
    Многофазная фибоначчиевая сортировка csv-файлов
    :param src: исходные файлы
    :param output: выходные файлы
    :param reverse: обратная сортировка
    :param key_opt: функция, вычисляющая значение, на основе которого будет производится сортировка.
    :param key_csv: столбец для csv по которому производится сортировка
    :param nflows: количество файлов многофазной сортировки
    :param type_data: тип сортируемых данных
    """
    if not key_opt:
        key_opt = lambda a: a
    if nflows < 3:
        raise ValueError("количество лент должно быть не меньше 3")
    if type_data == "i":
        key = lambda a: key_opt(int(a))
    elif type_data == "f":
        key = lambda a: key_opt(float(a))
    elif type_data == "s":
        key = lambda a: key_opt(a)
    else:
        raise ValueError("Некорректный тип")
    file_names = []
    for i in range(1, nflows + 1):
        file_name = "sort" + str(i) + ".csv"
        file_names.append(file_name)
        open(file_name, "w", encoding="utf-8").close()
    cmp = lambda a, b: key(a) <= key(b)
    if reverse:
        cmp = lambda a, b: key(a) >= key(b)
    if not key_csv:
        raise ValueError("Не указан key_csv")
    csv_column = key_csv
    level, d, csv_column_index = first_distribution_csv(src, nflows - 1, file_names[:len(file_names) - 1], cmp,
                                                        csv_column)
    if level != -1 and d != -1:
        with open(file_names[-1], "w") as f:
            f_writer = csv.writer(f, delimiter=",", lineterminator="\r")
            with open(file_names[0], "r") as file:
                file_reader = csv.reader(file, delimiter=",")
                row = next(file_reader)
                f_writer.writerow(row)
        cmp = lambda a, b: a <= b
        if reverse:
            cmp = lambda a, b: a >= b
        d.append(0)
        first = lambda a: min(a)
        if reverse:
            first = lambda a: max(a)
        output_file_index = nflows
        while level != 0:
            output_file_index = (output_file_index - 1)
            if output_file_index < 0:
                output_file_index = nflows - 1
            input_files_indexes_1 = [i for i in range(0, nflows)]
            input_files_indexes_1.remove(output_file_index)
            flag_2 = True
            while flag_2:
                if min([d[i] for i in input_files_indexes_1]) != 0:
                    for i in input_files_indexes_1:
                        d[i] -= 1
                    d[output_file_index] += 1
                    continue
                input_files_indexes_2 = []
                for i in input_files_indexes_1:
                    if d[i] == 0:
                        input_files_indexes_2.append(i)
                    else:
                        d[i] -= 1
                while len(input_files_indexes_2) != 0:
                    elements = []
                    for i in input_files_indexes_2:
                        with open(file_names[i], "r") as file_csv:
                            f_reader = csv.reader(file_csv, delimiter=",")
                            next(f_reader, False)
                            row = next(f_reader, False)
                            if row:
                                line = row[csv_column_index]
                            if row and line != "":
                                elements.append(key(line))
                            else:
                                input_files_indexes_2.remove(i)
                    if len(elements) == 0:
                        break
                    elem = first(elements)
                    elem_file_index = input_files_indexes_2[elements.index(elem)]
                    with open(file_names[output_file_index], "a") as output_file:
                        output_file_writer = csv.writer(output_file, delimiter=",", lineterminator="\r")
                        with open(file_names[elem_file_index], "r") as file_csv:
                            f_reader = csv.reader(file_csv, delimiter=",")
                            next(f_reader)
                            row = next(f_reader)
                            output_file_writer.writerow(row)
                    with open(file_names[elem_file_index], "r") as file_csv:
                        f_reader = csv.reader(file_csv, delimiter=",")
                        with open('stream1.csv', "w") as tempf:
                            tempf_writer = csv.writer(tempf, delimiter=",", lineterminator="\r")
                            row = next(f_reader, False)
                            tempf_writer.writerow(row)
                            next(f_reader)
                            row = next(f_reader, False)
                            while row:
                                tempf_writer.writerow(row)
                                row = next(f_reader, False)
                    with open('stream1.csv', "r") as file_csv:
                        f_reader = csv.reader(file_csv, delimiter=",")
                        row = next(f_reader, False)
                        while row:
                            row = next(f_reader, False)
                    os.replace('stream1.csv', file_names[elem_file_index])
                    with open(file_names[elem_file_index], "r") as file_csv:
                        f_reader = csv.reader(file_csv, delimiter=",")
                        row = next(f_reader, False)
                        while row:
                            row = next(f_reader, False)
                    with open(file_names[elem_file_index], "r") as file_csv:
                        f_reader = csv.reader(file_csv, delimiter=",")
                        next(f_reader, False)
                        row = next(f_reader, False)
                        if row:
                            line = row[csv_column_index]
                        if not row:
                            input_files_indexes_2.remove(elem_file_index)
                        elif not cmp(elem, key(line)):
                            input_files_indexes_2.remove(elem_file_index)
                with open(file_names[output_file_index - 1], "r") as file_csv:
                    f_reader = csv.reader(file_csv, delimiter=",")
                    next(f_reader, False)
                    if d[output_file_index - 1] == 0 and not next(f_reader, False):
                        flag_2 = False
                        level -= 1
    else:
        delete_files(file_names, src)
        return

    if not output:
        output = src
    with open(output, "w") as result_file:
        result_file_writer = csv.writer(result_file, delimiter=",", lineterminator="\r")
        with open(file_names[output_file_index], "r") as output_file:
            output_file_reader = csv.reader(output_file, delimiter=",")
            while True:
                row = next(output_file_reader, False)
                if row:
                    result_file_writer.writerow(row)
                else:
                    break
    delete_files(file_names, src)


def first_distribution_csv(src: PathType, sequence: int, file_names, cmp, csv_column):
    """
    Первичное фибоначчиевое распределение csv
    :param csv_column:
    :param src: Исходный файл
    :param sequence: Количество файлов (последовательностей)
    :param file_names: Имена файлов
    :param cmp: Лямбда функция сравнения
    """
    flag = True
    line_order = [1] * sequence
    line_order_copy = line_order.copy()
    last_lines = [0] * sequence
    with open(src, "r") as source:
        source_reader = csv.reader(source, delimiter=",")
        head = next(source_reader, False)
        if not head:
            return -1, -1, -1
        for i in range(0, len(head)):
            if head[i] == csv_column:
                csv_column_index = i
                break
        row = next(source_reader, False)
        if row:
            try:
                cmp(row[csv_column_index], row[csv_column_index])
            except ValueError:
                raise ValueError("Неккоректный тип относительно типа столбца сравнения")
        if not row:
            return -1, -1, -1
        line = row[csv_column_index]
        for i in range(sequence):
            with open(file_names[i], "a") as file:
                file_writer = csv.writer(file, delimiter=",", lineterminator="\r")
                file_writer.writerow(head)
                file_writer.writerow(row)
                last_lines[i] = line
                row = next(source_reader, False)
                if not row:
                    line_order_copy[i] -= 1
                    return 1, line_order_copy, csv_column_index
                line = row[csv_column_index]
                while cmp(last_lines[i], line):
                    file_writer.writerow(row)
                    last_lines[i] = line
                    row = next(source_reader, False)
                    if not row:
                        line_order_copy[i] -= 1
                        return 1, line_order_copy, csv_column_index
                    line = row[csv_column_index]
                line_order_copy[i] -= 1
                level = 1

        if not row:
            flag = False
        while flag:
            line_order_copy = line_order.copy()
            line_order = line_order_next(line_order)
            line_order_copy = [(line_order[i] - line_order_copy[i]) for i in range(sequence)]
            level += 1
            i = 0
            while max(line_order_copy) > 0:
                with open(file_names[i], "a") as file:
                    if cmp(last_lines[i], line):
                        line_order_copy[i] += 1
                    file_writer = csv.writer(file, delimiter=",", lineterminator="\r")
                    file_writer.writerow(row)
                    last_lines[i] = line
                    row = next(source_reader, False)
                    if not row:
                        line_order_copy[i] -= 1
                        flag = False
                        break
                    line = row[csv_column_index]
                    while cmp(last_lines[i], line):
                        file_writer.writerow(row)
                        last_lines[i] = line
                        row = next(source_reader, False)
                        if not row:
                            line_order_copy[i] -= 1
                            flag = False
                            break
                        line = row[csv_column_index]
                    if flag:
                        line_order_copy[i] -= 1
                        if (i != sequence - 1) and line_order_copy[i + 1] > line_order_copy[i]:
                            i += 1
                        else:
                            i = line_order_copy.index(line_order_copy[i])
                    else:
                        break
    return level, line_order_copy, csv_column_index


def delete_files(file_list, src):
    """
    После сортировки удаляем пустые файлы
    :param file_list: Список файлов
    :param src: Лямбда функция сравнения
    """
    for i in file_list:
        open(i, "r").close()
        os.unlink(i)
    if src.count("new_source") == 1:
        open(src, "r").close()
        os.unlink(src)


def line_order_next(line_order_prev):
    """
    Получение следующего уровня распределения
    :param line_order_prev: Строка предыдущего уровня распределения
    :return: Следующий уровень распределения
    """
    line_order = [0] * len(line_order_prev)
    for i in range(len(line_order_prev) - 1):
        line_order[i] = line_order_prev[0] + line_order_prev[i + 1]
    line_order[len(line_order) - 1] = line_order_prev[0]
    return line_order


if __name__ == "__main__":
    multiphase_sort("test1.csv", "sorted.csv", key_csv="sort")
    print("Data was sorted!")
