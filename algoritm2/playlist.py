"""
Модуль плелиста, наследуемый от LinkedList для работы с композициями
"""
from linked_list import *
from pygame import mixer
from composition import Composition


class Playlist(LinkedList):
    """
    Класс плейлист
    """
    def __init__(self, current_track=None, name=None):
        """
        Конструктор класса
        :param current_track: Нынешний трек
        :param name: Название плейлиста
        """
        super().__init__()
        self.name = name
        self.current_track = current_track

    @staticmethod
    def play_all(path):
        """
        Проигрывание музыкальной композиции
        :param path: Путь к файлу
        """
        mixer.music.load(path)
        mixer.music.play()

    def next_track(self):
        """
        Текущий трек принимает ссылку следующего трека
        """
        self.current_track = self.current_track.next_item

    def previous_track(self):
        """
        Текущий трек принимает ссылку предыдущего трека
        """
        self.current_track = self.current_track.previous_item

    def add_track(self, path):
        """
        Добавление трека
        :param path: Путь к файлу
        """
        self.append(Composition(path))
        self.current_track = self.first_item

    def switch_tracks(self, above=False):
        """
        Перестановка треков местами
        :param above: Перестановка выше или ниже по порядку
        """
        temp_track_data = self.current_track.data
        if above:
            self.current_track.data = self.current_track.previous_item.data
            self.current_track.previous_item.data = temp_track_data
        else:
            self.current_track.data = self.current_track.next_item.data
            self.current_track.next_item.data = temp_track_data

    def delete_track(self):
        """
        Удаление трека
        """
        temp = self.current_track
        self.remove(self.current_track.data)
        self.current_track = temp
        self.next_track()

    def find_track(self, num):
        """
        Метод для нахождения узла по померу песни
        @param num: номер песни
        @return: узел с песней
        """
        for temp in self:
            if temp.data.num == str(num):
                return temp
        return self.head

    @property
    def current(self):
        """
        Получение текущего трека
        @return: текущий трек
        """
        return self.current_track
