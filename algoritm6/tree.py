"""
Смолянинов Ярослав КИ21-17/2Б сжатие картинки с помощью квадродерева
"""
import threading
import warnings
from PIL import Image
from numpy import array_split, mean, tile, ndarray, vstack, uint8, hstack, concatenate
from numpy import all as numpall


class QuadTree:
    """
    Класс квадродерева
    """
    def __init__(self, img: ndarray, level: int = 0):
        """
        Инициализация квадродерева
        :param img: список с данными о картинке
        :param level: уровень нормирования
        """
        self.level = level
        self.img = img
        self.top_left = None
        self.top_right = None
        self.bottom_left = None
        self.bottom_right = None
        self.final = True

    def sameness(self) -> bool:
        """
        Проверка на различность цвета пикселей в картинке
        :return: True - все одинаковые, False - разные
        """
        same_px = [numpall(i == self.img[0]) for i in self.img]
        return all(same_px)

    def subdivide(self) -> None:
        """
        Рекурсивное разделение картинки на 4 части в 4 потоках
        """
        if not self.sameness():
            self.final = False
            split = split_by_4(self.img)
            self.make_child(split)
            if self.level == 0:
                threads = []
                th1 = threading.Thread(target=self.top_left.subdivide)
                threads.append(th1)
                th2 = threading.Thread(target=self.top_right.subdivide)
                threads.append(th2)
                th3 = threading.Thread(target=self.bottom_left.subdivide)
                threads.append(th3)
                th4 = threading.Thread(target=self.bottom_right.subdivide)
                threads.append(th4)
                for thread in threads:
                    thread.start()
                    thread.join()
            else:
                self.top_left.subdivide()
                self.top_right.subdivide()
                self.bottom_left.subdivide()
                self.bottom_right.subdivide()

    def make_child(self, split: array_split) -> None:
        """
        Создание потомков
        :param split: разделённая картинка на 4 части
        """
        self.top_left = QuadTree(split[0], self.level + 1)
        self.top_right = QuadTree(split[1], self.level + 1)
        self.bottom_left = QuadTree(split[2], self.level + 1)
        self.bottom_right = QuadTree(split[3], self.level + 1)

    def check_axis(self, coord: int, axis: int) -> bool:
        """
        Проверить координату на вхождение в картинку
        :param coord: значение координаты
        :param axis: ось (0 = y, 1 = x)
        :return: входит (True) / не входит (False)
        """
        if coord < 0 or coord > self.img.shape[axis]:
            return False
        return True

    def insert(self, point: list, x_coor: int = None, y_coor: int = None):
        """
        Вставить линию в список с данными о картинке
        :param point: цвет линии
        :param x_coor: значение оси x
        :param y_coor: значение оси y
        """
        if not (y_coor is None) and self.check_axis(y_coor, 0):
            if y_coor not in (self.img.shape[0] - 1, 0):
                first = self.img[0:y_coor, 0:self.img.shape[1]]
                second = self.img[y_coor:self.img.shape[0], 0:self.img.shape[1]]
                first = vstack([first, [[point] * self.img.shape[1]]])
                self.img = vstack([first, second])
            elif y_coor == 0:
                self.img = vstack([[[point] * self.img.shape[1]], self.img])
            elif y_coor == self.img.shape[0] - 1:
                self.img = vstack([self.img, [[point] * self.img.shape[1]]])

        if not (x_coor is None) and self.check_axis(x_coor, 1):
            if x_coor not in (self.img.shape[1] - 1, 0):
                first = self.img[0:self.img.shape[0], 0:x_coor]
                second = self.img[0:self.img.shape[0], x_coor:self.img.shape[1]]
                first = hstack([first, [[point]] * self.img.shape[0]])
                self.img = hstack([first, second])
            elif x_coor == 0:
                self.img = hstack([[[point]] * self.img.shape[0], self.img])
            elif x_coor == self.img.shape[0] - 1:
                self.img = hstack([self.img, [[point]] * self.img.shape[0]])
        self.subdivide()

    def delete(self, x_coor: int = None, y_coor: int = None):
        """
        Удалить линию из списка с данными о картинке
        :param x_coor: значение оси x
        :param y_coor: значение оси y
        """
        if not (y_coor is None) and self.check_axis(y_coor, 0):
            if y_coor not in (self.img.shape[0] - 1, 0):
                first = self.img[0:y_coor, 0:self.img.shape[1]]
                second = self.img[y_coor + 1:self.img.shape[0], 0:self.img.shape[1]]
                self.img = vstack([first, second])
            elif y_coor == 0:
                self.img = self.img[1:self.img.shape[0], 0:self.img.shape[1]]
            elif y_coor == self.img.shape[0] - 1:
                self.img = self.img[0:self.img.shape[0] - 1, 0:self.img.shape[1]]

        if not (x_coor is None) and self.check_axis(x_coor, 1):
            if x_coor not in (self.img.shape[1] - 1, 0):
                first = self.img[0:self.img.shape[0], 0:x_coor]
                second = self.img[0:self.img.shape[0], x_coor + 1:self.img.shape[1]]
                self.img = hstack([first, second])
            elif x_coor == 0:
                self.img = self.img[0:self.img.shape[0], 1:self.img.shape[1]]
            elif x_coor == self.img.shape[0] - 1:
                self.img = self.img[0:self.img.shape[0], 0:self.img.shape[1] - 1]

        self.subdivide()

    def get_image(self, level: int) -> array_split:
        """
        Получить картинку определённого уровня нормирования
        :param level: уровень нормирования
        :return: список с данными о картинке
        """
        if self.final or self.level == level:
            return tile(mean_all(self.img), (self.img.shape[0], self.img.shape[1], 1))
        return connect_4(self.top_left.get_image(level), self.top_right.get_image(level),
                         self.bottom_left.get_image(level), self.bottom_right.get_image(level))

    def area(self, x_start: int, y_start: int, x_finish: int, y_finish: int):
        """
        Выделить область в списке с данными о картинке
        :param x_start: начальная координата оси x
        :param y_start: начальная координата оси y
        :param x_finish: конечная координата оси x
        :param y_finish: конечная координата оси y
        """
        if not self.check_axis(x_start, 1) or not self.check_axis(x_finish, 1) \
                or not self.check_axis(y_start, 0) or not self.check_axis(y_finish, 0):
            raise ValueError("Зона вне картинки")
        if (x_start >= x_finish) or (y_start >= y_finish):
            raise ValueError("Некорректный ввод")
        self.img = self.img[y_start:y_finish, x_start:x_finish]
        self.subdivide()


def make_gif(quadtree: QuadTree):
    """
    Создает гифку, показывающую процесс разбиения квадродерева.
    :param quadtree: объект QuadTree
    """
    images = [Image.fromarray((quadtree.get_image(level)).astype(uint8), 'RGB') for level in range(0, 15)]
    images[0].save('qt.gif', save_all=True, append_images=images[1:], optimize=True, duration=1000, loop=0)


def split_by_4(img: ndarray) -> ndarray:
    """
    Разделить картинку на 4 части
    :param img: список с данными о картинке
    :return: список с частями картинки
    """
    split = array_split(img, 2, axis=0)
    first = array_split(split[0], 2, axis=1)
    second = array_split(split[1], 2, axis=1)
    first.append(second[0])
    first.append(second[1])
    return first


def connect_4(tleft: array_split, tright: array_split, bleft: array_split, bright: array_split) -> ndarray:
    """
    Соединить 4 части картинки
    :param tleft: верхняя левая часть
    :param tright: верхняя правая часть
    :param bleft: нижняя левая часть
    :param bright: нижняя правая часть
    :return: соединённая картинка
    """
    top = concatenate((tleft, tright), axis=1)
    bottom = concatenate((bleft, bright), axis=1)
    return concatenate((top, bottom), axis=0)


def mean_all(img: ndarray) -> ndarray:
    """
    Нахождение среднего цвета
    :param img: Список с данными о картинке
    :return: Средний цвет пикселей
    """
    if len(img) == 0:
        raise ValueError("Input image is empty.")

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        return mean(img, axis=(0, 1)).astype(int)


def save_img(quadtree: object, level: int) -> None:
    """
    Сохраняет изображение с заданным уровнем нормирования в файл в формате jpg.
    :param quadtree: Экземпляр класса QuadTree
    :param level: Уровень нормирования изображения
    """
    image = Image.fromarray((quadtree.get_image(level)).astype(uint8), 'RGB')
    image.save(f"qt-{level}.jpg")
