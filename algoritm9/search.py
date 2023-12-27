"""
Inaccurate string search using the extended selection algorithm
"""
from __future__ import annotations

import string as s
from typing import Optional

ENGLISH_ALPHABET = s.ascii_lowercase + s.ascii_uppercase
RUSSIAN_ALPHABET = ''.join(chr(1072 + i) for i in range(32)) + "ё" + ''.join(chr(1040 + i) for i in range(32)) + "Ё"


def expand_selection(string: str, case_sensitivity: bool):
    """
    Generate a list of expanded selections for a given string
    :param: string: The input string
    :param: case_sensitivity: Whether the expansion should be case-sensitive (True) or not (False)
    :return: A list of expanded selections
    """
    selection = [string]
    len_string = len(string)
    if not case_sensitivity:
        alphabet = ENGLISH_ALPHABET[:27] + RUSSIAN_ALPHABET[:34]
    else:
        alphabet = ENGLISH_ALPHABET + RUSSIAN_ALPHABET
    for i in range(len_string):
        new_string = list(string)
        new_string.pop(i)
        selection.append("".join(new_string))
        for j in list(alphabet):
            new_string = list(string)
            new_string.insert(i, j)
            selection.append("".join(new_string))
            new_string.pop(i)
            new_string[i] = j
            selection.append("".join(new_string))
    return selection


def search(substring: str, text: list[str], case_sensitivity: bool = False, count: Optional[int] = None,
           method: str = "first") -> (str, list[int]):
    """
    Perform a fuzzy search for a substring within a list of text strings
    :param: substring: The substring to search for
    :param: text: A list of text strings to search within
    :param: case_sensitivity: Whether the search should be case-sensitive (True) or not (False)
    :param: count: The maximum number of occurrences to find (default is None to find all)
    :param: method: The search method ('first' or 'last', default is 'first')
    :return: A tuple containing the substring and a list of indexes where it was found
    """
    indexes = []
    len_text = len(text)
    if method == "last":
        sequence = reversed(range(len_text))
    else:
        sequence = range(len_text)
    dub_text = text
    if not case_sensitivity:
        dub_text = [dub_text[i].lower() for i in range(len_text)]
    selection = expand_selection(substring, case_sensitivity)
    counter = 0
    index = build_string_index(selection)
    if not count:
        count = float("inf")
    for i in sequence:
        if counter < count:
            if search_string_index(index, selection, dub_text[i]):
                indexes.append(i)
                counter += 1
        else:
            break
    return substring, indexes


def build_string_index(data: list[str]) -> dict[int, list[int]]:
    """
    Build a string index for fast searching.
    :param: data: A list of strings to index.
    :return: A dictionary representing the string index.
    """
    index = {}  # Хеш-таблица для индексации строк
    for i, string in enumerate(data):
        hash_value = hash(string)
        if hash_value in index:
            index[hash_value].append(i)
        else:
            index[hash_value] = [i]
    return index


def search_string_index(index: dict[int, list[int]], data: list[str], query: str) -> list[str]:
    """
    Search for a query in a string index.
    :param: index: The string index dictionary.
    :param: data: The original data as a list of strings.
    :param: query: The query string to search for.
    :return: A list of matching strings.
    """
    hash_value = hash(query)
    if hash_value in index:
        positions = index[hash_value]
        results = [data[i] for i in positions]
        return results
    else:
        return []


def write_to_file(file: str, text: list[str], result: dict):
    """
    Write search results to a file.
    :param: file: The path to the file where results will be saved.
    :param: text: The original text as a list of strings.
    :param: result: A dictionary containing search results.
    """
    with open(file, "w", encoding='utf-8') as file:
        file.write("Source text: " + " ".join(text) + "\n")
        file.write("Search results:\n")
        for key, value in result.items():
            values = [text[val] for val in value]
            file.write(f'{key}: {values}\n')
