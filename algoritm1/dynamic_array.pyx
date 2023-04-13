# cython: language_level=3
# distutils: language = c

# Указываем компилятору, что используется Python 3 и целевой формат
# языка Си (во что компилируем, поддерживается Си и C++)


# Также понадобятся функции управления памятью
import array as ar
from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free
from cpython.float cimport PyFloat_FromDouble, PyFloat_AsDouble
from cpython.long cimport PyLong_FromLong, PyLong_AsLong


# Так как хотим использовать массив для разных типов, указывая только
# код типа без дополнительных замарочек, то используем самописный
# дескриптор. Он будет хранить функции получения и записи значения в
# массив для нужных типов.
cdef struct arraydescr:
    # код типа, один символ
    char* typecode

    # размер одного элемента массива
    int itemsize

    # функция получения элемента массива по индексу. Обратите внимание,
    # что она возвращает Python тип object. Вот так выглядит сигнатура на Си:
    # PyObject * (*getitem)(struct arrayobject *, Py_ssize_t)
    object (*getitem)(array, size_t)
    int (*setitem)(array, size_t, object)


cdef object double_getitem(array a, size_t index):
    # Функция получения значения из массива для типа double.
    # Обратите внимание, что Cython сам преобразует Сишное значение типа
    # double в аналогичны объект PyObject
    return (<double *> a.data)[index]


cdef object long_getitem(array a, size_t index):
    # Функция получения значения из массива для типа int.
    return (<long *> a.data)[index]


cdef int double_setitem(array a, size_t index, object obj):
    # Функция записи значения в массив для типа double. Здесь нужно
    # самими извлеч значение из объекта PyObject.
    if not isinstance(obj, int) and not isinstance(obj, float):
        return -1

    # Преобразования Python объекта в Сишный
    cdef double value = PyFloat_AsDouble(obj)

    if index >= 0:
        (<double *> a.data)[index] = value
    return 0


cdef int long_setitem(array a, size_t index, object obj):
    # Функция записи значения в массив для типа long.
    if not isinstance(obj, int):
        return -1

    cdef long value = PyLong_AsLong(obj)
    if index >= 0:
        (<long *> a.data)[index] = value
    return 0


# Массив с дескрипторами
cdef arraydescr[2] descriptors = [
    arraydescr("d", sizeof(double), double_getitem, double_setitem),
    arraydescr("i", sizeof(long), long_getitem, long_setitem)
]


# Перечисляемые типы для int и double
cdef enum TypeCode:
    DOUBLE = 0
    LONG = 1


# Преобразование строкового кода в число
cdef int char_typecode_to_int(str typecode):
    if typecode == "i":
        return TypeCode.LONG
    elif typecode == "d":
        return TypeCode.DOUBLE
    return -1


cdef class array:
    # Класс статического массива.
    # В поле length сохраняем длину массива, а в поле data будем хранить
    # данные. Обратите внимание, что для data используем тип char,
    # занимающий 1 байт. Далее мы будем выделять сразу несколько ячеек
    # этого типа для одного значения другого типа. Например, для
    # хранения одного double используем 8 ячеек для char.
    cdef public size_t length
    cdef char* data
    cdef arraydescr* descr
    cdef size_t capacity

    # Аналог метода __init__
    def __cinit__(self, str typecode, list array):
        self.length = len(array)
        self.capacity = 2 * self.length
        if typecode != 'd' and typecode != 'i':
            raise TypeError("The code can be either d or i")
        cdef int mtypecode = char_typecode_to_int(typecode)
        self.descr = &descriptors[mtypecode]
        # Выделяем память для массива
        self.data = <char*> PyMem_Malloc(self.capacity * self.descr.itemsize)
        if not self.data:
            raise MemoryError()
        for i in range(len(array)):
            self.__setitem__(i, array[i])

    # Метод возвращает длину массива
    def __len__(self):
        return self.length

    # Не забываем освобаждать память. Привязываем это действие к объекту
    # Python. Это позволяет освободить память во время сборки мусора.
    def __dealloc__(self):
        PyMem_Free(self.data)

    # Метод добавляет объект в конец массива
    def append(self, object value):
        if isinstance(value, float) and self.descr.typecode == b'i':
            raise TypeError('The type must be integer')
        if self.length >= self.capacity:
            self.capacity = 2 * self.length
            self.data = <char*> PyMem_Realloc(self.data, self.capacity * self.descr.itemsize)
        self.length += 1
        if self.descr.typecode == b'd':
            (<double *> self.data)[self.length - 1] = value
        if self.descr.typecode == b'i':
            (<long *> self.data)[self.length - 1] = value

    # Метод добавляет объект массив по индексу
    def insert(self, int index, object value):
        if index < 0 or index > self.length:
            if self.length > 0:
                if index < 0:
                    if abs(index) > self.length:
                        index = 0
                    else:
                        index = index % self.length
                elif index >= self.length:
                    index = self.length
            else:
                raise IndexError()
        cdef object first_time_number
        cdef object second_time_number
        if self.length >= self.capacity:
            self.capacity = 2 * self.length
            self.data = <char*> PyMem_Realloc(self.data, self.capacity * self.descr.itemsize)
        self.length += 1
        for i in range(index, self.length):
            if i == index:
                first_time_number = self.__getitem__(i)
                self.__setitem__(i, value)
            else:
                second_time_number = self.__getitem__(i)
                self.__setitem__(i, first_time_number)
                first_time_number = second_time_number

    # Метод удаляет объект из массива по значению
    def remove(self, object obj):
        cdef int flag = 0
        for i in range(self.length - 1):
            if flag == 1:
                self.__setitem__(i, self.__getitem__(i + 1))
            if obj == self.__getitem__(i) and flag != 1:
                self.__setitem__(i, self.__getitem__(i + 1))
                flag = 1
        if self.__getitem__((self.length - 1)) == obj:
            flag = 1
        if flag == 0:
            raise ValueError("There is no such value.")
        self.length -= 1
        if self.length >= self.capacity:
            self.capacity = 2 * self.length
            self.data = <char*> PyMem_Realloc(self.data, self.capacity * self.descr.itemsize)

    # Метод удаляет объект в массиве по индексу
    def pop(self, object index = None):
        if index is None:
            index = self.length - 1
        if not isinstance(index, int):
            raise TypeError()
        if index < 0:
            if abs(index) > self.length:
                raise IndexError()
            else:
                index = self.get_absolute_index(index)
        cdef object item = self.__getitem__(index)
        if (self.length - 1) == index:
            self.length -= 1
            if self.descr.typecode == b'i':
                return int(item)
            if self.descr.typecode == b'd':
                return float(item)
        elif 0 <= index < self.length - 1:
            for i in range(index, self.length - 1):
                self.__setitem__(i, self.__getitem__(i + 1))
            self.length -= 1
            if self.length >= self.capacity:
                self.capacity = 2 * self.length
                self.data = <char*> PyMem_Realloc(self.data, self.capacity * self.descr.itemsize)
            if self.descr.typecode == b'i':
                return int(item)
            if self.descr.typecode == b'd':
                return float(item)

    # Разворачивание массива
    def __reversed__(self):
        for i in range(self.length):
            yield self.descr.getitem(self, self.length - i - 1)

    # Сравнение двух экземпляров элементов
    def __eq__(self, other):
        if isinstance(other, ar.array):
            if other.typecode.encode('utf-8') == self.descr.typecode:
                if list(self) == list(other):
                    return True
        return False

    # Определение занимаемого размера массива в байтах.
    def __sizeof__(self):
        return self.capacity * self.descr.itemsize

    # Возвращение абсолютного индекса (Аналог для индексов в python [-1], [-2]...)
    def get_absolute_index(self, object index):
        return self.length - abs(index)

    # Возвращает значение элемента массива по индексу
    def __getitem__(self, object index):
        if not isinstance(index, int) or index % 1 != 0 :
            raise TypeError("The index must be an integer")
        else:
            index = int(index)
        if index < 0:
            index = self.get_absolute_index(index)
        if 0 <= index < self.length:
            return self.descr.getitem(self, index)
        raise IndexError("Array index out of range")

    # Присваивает значение элементу массива по индексу
    def __setitem__(self, object index, object value):
        if isinstance(index, int) and abs(value) > 2147483647:
            raise OverflowError()
        index = int(index)
        if index < 0:
            index = self.get_absolute_index(index)
        if 0 <= index < self.length:
            self.descr.setitem(self, index, value)
        else:
            raise IndexError()
