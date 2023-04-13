"""Пример использования модуля dynamic_array"""

import sys

import dynamic_array  # pylint: disable=E0401



x = dynamic_array.array('i', [1])

print(f'{x = }')
print(f'{x.length = }')
# x.append(12)
print(f'{x[0,5] = }')
# print(f'{x[1] = }')
# print(f'{x[2] = }')
# print(f'{x[3] = }')
# print(f'{x[4] = }')
print('-' * 50)