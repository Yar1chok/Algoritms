"""
Console implementation of working with a maze
Смолянинов Ярослав Евгеньевич, КИ21-17/2Б, Практическая работа №9
Алгоритм расширения выборки - Вариант 5
"""
from concurrent.futures import ThreadPoolExecutor
from search import search, write_to_file
from itertools import chain
import click


@click.command()
@click.option("--string", "-s", is_flag=True, help="Строка для поиска")
@click.option("--sub-string", "-ss", default=[], multiple=True, help="Подстрока для поиска")
@click.option("--case-sensitivity", "-cs", is_flag=True, help="Чувствительность к регистру")
@click.option("--method", "-m", default="first", type=click.Choice(["first", "last"]),
              help="Метод поиска")
@click.option("--count", "-c", default=None, type=click.INT, help="Количество вхождений")
@click.option("--data-file", "-df", type=str, default=None, help="Файл для поиска")
@click.option("--save-file", "-sf", type=str, default=None, help="Файл для сохранения результатов")
def console_search(string: str, sub_string: list[str], case_sensitivity: bool, method: str, count: int, data_file: str,
                   save_file: str):
    """
    Console implementation of approximate search with an extended selection algorithm
    :param string: The search string
    :param sub_string: Words to search for within the string
    :param case_sensitivity: Whether the search is case-sensitive (True) or not (False)
    :param method: The search method ('first' or 'last')
    :param count: Number of occurrences of a single word to consider
    :param data_file: Path to a file containing data for the search
    :param save_file: Path to a file to save the search results
    :return:
    """
    if count is not None and count <= 0:
        raise ValueError("Occurrences must be greater than 0")
    if string:
        string = click.prompt("Enter the search string")
        string = [string.strip("\n").split()]
    if data_file:
        if string:
            raise AttributeError("Both the file and the string are entered")
        string = []
        with open(data_file, "r", encoding='utf-8') as file:
            for line in file:
                string.append(line.strip("\n").split())
    if not string:
        raise ValueError("No data to search for")
    sub_string = list(set(sub_string))
    result = []
    args_for_search = [(ss, list(chain(*string)), case_sensitivity, count, method) for ss in sub_string]
    with ThreadPoolExecutor(len(sub_string)) as pool:
        finding = pool.map(search, *zip(*args_for_search))
        for k in finding:
            result.append(k)
    dict_result = dict()
    for k in range(len(result)):
        for (i, j) in result:
            dict_result[i] = j
    colors = ["blue", "red", "green", "yellow", "bright_black", "bright_cyan", "magenta"]
    dict_color = dict()
    num_col = 0
    for key in dict_result.keys():
        dict_color[key] = colors[num_col % len(colors)]
        num_col += 1
    if method == 'last':
        seq_i = range(len(string) - 1, -1, -1)
        counter_el = len(list(chain(*string))) - 1
    else:
        seq_i = range(len(string))
        counter_el = 0
    for i in seq_i:
        if method == 'last':
            seq_j = range(len(string[i]) - 1, -1, -1)
        else:
            seq_j = range(len(string[i]))
        for j in seq_j:
            flag = False
            if counter_el in list(chain(*list(dict_result.values()))):
                for key, value in dict_result.items():
                    if counter_el in value:
                        click.secho(" ", nl=False)
                        click.secho(string[i][j], bg=dict_color[key], nl=False)
                        click.secho(" ", nl=False)
                        flag = True
            if not flag:
                click.secho(" ", nl=False)
                click.secho(string[i][j], nl=False)
                click.secho(" ", nl=False)
            counter_el = counter_el + 1 if method == "first" else counter_el - 1
        click.secho("")
        if i == 9 and method == "first":
            break
        elif len(string) >= 10 and i == len(string) - 10 and method == "last":
            break
    click.echo("Results:")
    string = list(chain(*string))
    for key, value in dict_result.items():
        values = [string[val] for val in value]
        click.echo(f'{key}: {values}')
    if save_file:
        write_to_file(save_file, string, dict_result)
