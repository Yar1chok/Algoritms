"""Модуль "заглушка" для тестов"""


class LinkedListItem:
    """Узел связного списка"""

    def __init__(self, data=None):
        """
        Метод для инициализации связного списка
        @param data: данные узла
        """
        self.data = data
        self.next = None
        self.previous = None

    @property
    def next_item(self):
        """
        Получение следующиего элемента
        @return: следующий элемент
        """
        return self.next

    @next_item.setter
    def next_item(self, value):
        """
        Сеттер для следующего узла
        @param value: следующий узел
        """
        self.next = value
        if value:
            self.next.previous = self

    @property
    def previous_item(self):
        """
        Получение предыдущего элемента
        @return: предыдущий элемент
        """
        return self.previous

    @previous_item.setter
    def previous_item(self, value):
        """
        Сеттер для предыдущего узла
        @param value: предыдущий узел
        """
        self.previous = value
        if value:
            self.previous.next = self

    def __repr__(self):
        """
        Метод для строкового представления данных узла
        @return: строковое представление данных узла
        """
        return str(self.data)


class LinkedList:
    """Связный список"""
    def __init__(self, first_item=None):
        """
        Метод для инициализации связного списка
        :param first_item: первый элемент
        """
        self.last_element = None
        self.iter_num = 0
        if first_item:
            self.first_item = first_item
            self.head = first_item
            self.length = 1
            item = first_item
            while item.next_item != self.head:
                self.length += 1
                item = item.next_item
            self.head.previous_item = item
        else:
            self.first_item = None
            self.head = None
            self.length = 0

    @staticmethod
    def checking_node_type(item: object):
        """
        Метод для проверки объекта на принадлежность к типу LinkedListItem
        :param item: объект
        :return: узел
        """
        if isinstance(item, LinkedListItem):
            return item
        return LinkedListItem(item)

    @property
    def last(self):
        """
        Получение последнего узла списка
        :return: последний узел
        """
        if self.head:
            return self.head.previous_item
        return None

    def append_in_empty(self, node: LinkedListItem):
        """
        Метод для добавления узла в пустой список
        :param node: узел
        """
        self.first_item = node
        self.head = self.first_item
        self.head.next_item = self.first_item
        self.head.previous_item = self.first_item

    def append_left(self, item):
        """
        Метод для добавления узла в начало списка
        :param item: объект
        """
        node = self.checking_node_type(item)
        if not self.head:
            self.append_in_empty(node)
        else:
            node.previous_item = self.last
            node.next_item = self.head
            self.head = self.first_item = node
        self.length += 1

    def append_right(self, item):
        """
        Метод для добавления узла в конец списка
        :param item: объект
        """
        node = self.checking_node_type(item)
        if not self.head:
            self.append_in_empty(node)
        else:
            self.last.next_item = node
            node.next_item = self.head
        self.length += 1

    def append(self, item):
        """
        Алиас для добавления справа
        :param item: объект
        """
        self.append_right(item)

    def remove(self, item):
        """
        Метод для удаления узла
        :param item: узел или объект
        :return: индекс удаленного элемента
        """
        temp = self.head
        for index in range(self.length):
            if temp.data == item or temp == item:
                if self.length == 1:
                    self.head = None
                    self.length = 0
                    return index
                if temp == self.head:
                    last = self.last
                    self.head = temp.next_item
                    self.head.previous_item = last
                    self.length -= 1
                    return index
                temp.previous_item.next_item = temp.next_item
                self.length -= 1
                return index
            temp = temp.next_item
        raise ValueError

    def insert(self, previous, item):
        """
        Метод для вставки элемента по индексу
        :param previous: элемент после которого надо вставить item
        :param item: элемент для вставки
        """
        item = self.checking_node_type(item)
        temp = self.head
        for _ in range(previous):
            temp = temp.next_item
        item.previous_item = temp.previous_item
        item.next_item = temp
        if previous == 0:
            self.head = item
            self.first_item = item
        self.length += 1

    def __len__(self):
        """
        Получение длины списка
        :return: длина списка
        """
        return self.length

    def __iter__(self):
        """
        Метод для поддержки итерации
        :return: список
        """
        temp = self.head
        for i in range(self.length):
            yield temp
            temp = temp.next_item

    def __getitem__(self, index):
        """
        Метод для получения элемента по индексу
        :param index: индекс
        :return: элемент
        """
        temp = self.head
        if index >= self.length or index < -self.length or type(index) != int:
            raise IndexError
        if index < 0:
            index = self.length - abs(index)
        for i in range(self.length):
            if i == index:
                return temp
            temp = temp.next_item

    def __contains__(self, item):
        """
        Поддержка оператора in
        :param item: Элемент связного списка
        :return: True/False
        """
        temp = self.head
        for i in range(self.length):
            if temp.data == item:
                return True
            temp = temp.next_item
        return False

    def __reversed__(self):
        """
        Переворот списка
        :return: перевернутый список
        """
        return reversed([item.data for item in self])

    def __next__(self, item):
        """
        Получение следующего элемента списка от заданного
        :param: item - заданный элемент списка
        """
        return item.next_item
