"""Модуль с плеером"""

import json
import os
import shutil
import sys
from pathlib import Path


from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox, QInputDialog
from pygame import mixer

from player_interface import *
from playlist import Playlist

mixer.init()


class Player(Ui_MainWindow):
    """
    Плеер
    """
    def __init__(self):
        """
        Конструктор класса
        """
        super().__init__()
        self.playlist_array = list()
        self.playlist = None
        self.playing_track = None
        self.playing_playlist = None
        self.is_music_playing = False
        self.is_track_initialized = False

        self.app = QtWidgets.QApplication(sys.argv)
        self.GenerateWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.GenerateWindow)
        self.GenerateWindow.show()
        self.ui.pause_button.clicked.connect(self.start_stop_song)
        self.ui.previous_song_button.clicked.connect(self.previous)
        self.ui.next_song_button.clicked.connect(self.next)
        self.ui.add_song_button.clicked.connect(self.add_track)
        self.ui.songs.itemClicked.connect(self.set_current_track)
        self.ui.songs.itemDoubleClicked.connect(self.track_init)
        self.ui.songs.dropEvent = self.dropEvent
        self.ui.remove_song_button.clicked.connect(self.delete_track)
        self.ui.add_playlist_button.clicked.connect(self.add_playlist)
        self.ui.remove_playlist_button.clicked.connect(self.delete_playlist)
        self.ui.playlists.itemClicked.connect(self.set_current_playlist)
        self.ui.playlists.itemDoubleClicked.connect(self.track_init)
        self.make_playlist_from_data()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_track_progress)
        self.app.exec_()
        self.write_data_in_json()
        sys.exit()

    @staticmethod
    def message_box(title, informative_text):
        """
        Сообщение об ошибке
        :param title: Заголовок
        :param informative_text: Описание ошибки
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(title)
        msg.setInformativeText(informative_text)
        msg.setWindowTitle("Music Player")
        msg.setWindowIcon(QIcon("icons/player.png"))
        msg.exec_()

    @staticmethod
    def get_time(time: int) -> str:
        """
        Получение времени трека
        :param time: Полное время песни в секундах
        :return: Время песни (минуты:секунды)
        """
        minutes = str(time // 60)
        seconds = str(round(time % 60))
        if len(minutes) == 1:
            minutes = "0" + minutes
        if len(seconds) == 1:
            seconds = "0" + seconds
        return minutes + ":" + seconds

    def update_track_progress(self):
        """
        Вывод времени на экран
        """
        if self.playlist is not None and self.playlist.current_track is not None:
            seconds = mixer.music.get_pos() // 1000
            self.ui.time.setText(self.get_time(seconds))
            self.ui.time_slider.setValue(seconds)
            if seconds >= self.playlist.current_track.data.duration:
                self.next()

    def next(self):
        """
        Переключение на следующую песню
        """
        if self.is_current_track_not_none("Не удается воспроизвести следующий трек"):
            self.playlist.next_track()
            self.track_init()

    def previous(self):
        """
        Переключение на предыдущую песню
        """
        if self.is_current_track_not_none("Не удается воспроизвести предыдущий трек"):
            self.playlist.previous_track()
            self.track_init()

    def dropEvent(self, event):
        """
        Переопределение метода dropEvent для корректной работы перемещения треков
        :param event: Перемещение
        """
        insert_pos = event.pos()
        from_list = event.source()
        insert_index = from_list.row(self.ui.songs.itemAt(insert_pos))
        drop_index = self.ui.songs.currentRow()
        self.playlist[insert_index].data, self.playlist[drop_index].data = \
            self.playlist[drop_index].data, self.playlist[insert_index].data
        if self.playing_track == self.playlist[insert_index]:
            self.playlist.current_track = self.playlist[drop_index]
            self.playing_track = self.playlist[drop_index]
        elif self.playing_track == self.playlist[drop_index]:
            self.playlist.current_track = self.playlist[insert_index]
            self.playing_track = self.playlist[insert_index]
        self.update_track_list()
        self.update_track_list()

    def set_current_track(self, item):
        """
        Установка выбранного трека как нанешнего
        :param item: Выбранный трек
        """
        for song in self.playlist:
            if song.data.name == item.text():
                self.playlist.current_track = song
                self.is_track_initialized = False

    def set_current_playlist(self, item):
        """
        Установка выбранного плейлиста как нынешнего
        :param item: Выбранный плейлист
        """
        for playlist in self.playlist_array:
            if playlist.name == item.text():
                self.playlist = playlist
                self.update_track_list()
                if not self.is_music_playing:
                    self.is_track_initialized = False

    def is_current_track_not_none(self, text: str) -> bool:
        """
        Проверка наличия нынешнего трека
        :param text: Сообщение описывающее ошибку
        :return: Наличие ошибки
        """
        if self.playlist_chosen():
            if self.playlist.current_track is None:
                self.message_box(text, "Добавьте песню")
                return False
            return True
        return False

    def playlist_chosen(self):
        """
        Проверка выбран ли плейлист
        :return: Результат проверки
        """
        if self.playlist is not None:
            return True
        else:
            self.message_box("Не удается воспроизвести текущий трек", "Выберит плейлист")
            return False

    def track_init(self):
        """
        Инициализация песни
        """
        if self.is_current_track_not_none("Не удается воспроизвести текущий трек"):
            self.update_track_list()
            self.timer.start()
            self.playing_track = self.playlist.current_track
            self.playing_playlist = self.playlist
            if self.playing_track.data.image:
                self.ui.image_song.setPixmap(QPixmap(self.playing_track.data.image).scaled(81, 81))
            else:
                self.ui.image_song.setPixmap(QPixmap("icons/without_logo.png").scaled(81, 81))
            if self.playing_track.data.title and self.playing_track.data.artist:
                self.ui.name_song.setText(self.playing_track.data.artist + " - " + self.playing_track.data.title)
            else:
                self.ui.name_song.setText(self.playing_track.data.name)
            self.ui.time_slider.setRange(0, self.playlist.current_track.data.duration)
            audio_path = self.playlist.current_track.data.path
            self.playlist.play_all(audio_path)
            self.is_music_playing = True
            self.is_track_initialized = True
            self.ui.pause_button.setIcon(QIcon("icons/pause.png"))

    def start_stop_song(self):
        """
        Проигрывание песни при инициализации. Пауза, если песня проинициализирована
        """
        if not self.is_music_playing and self.is_track_initialized:
            self.unpause()
        elif not self.is_music_playing and not self.is_track_initialized:
            self.track_init()
            self.is_track_initialized = True
        else:
            self.pause()

    def pause(self):
        """
        Остановка песни
        """
        if self.is_current_track_not_none("Не удается воспроизвести текущий трек"):
            mixer.music.pause()
            self.is_music_playing = False
            self.ui.pause_button.setIcon(QIcon("icons/play.png"))

    def unpause(self):
        """
        Снятие песни с паузы
        """
        if self.is_current_track_not_none("Не удается воспроизвести текущий трек"):
            mixer.music.unpause()
            self.is_music_playing = True
            self.ui.pause_button.setIcon(QIcon("icons/pause.png"))

    def add_track(self):
        """
        Добавление песни
        """
        if self.playlist is not None:
            directory_path = "./songs/"
            file_path = QtWidgets.QFileDialog.getOpenFileName(None, "Выберите файл", ".", "Sound Files (*.mp3)")[0]
            if file_path != '':
                if directory_path[2:] not in file_path:
                    shutil.copy(file_path, directory_path)
                file_path = directory_path + file_path.split('/')[-1]
                if self.playlist is not None:
                    if file_path not in self.playlist.__str__():
                        self.playlist.add_track(file_path)
                    else:
                        self.message_box("Такой файл уже есть", "Выберите другой")
                self.update_track_list()
        else:
            self.message_box("Не удается добавить трек", "Выберите плейлист")

    def delete_track(self):
        """
        Удаление песни
        """
        if self.is_current_track_not_none("Нечего удалять"):
            if self.playlist.current_track == self.playing_track:
                self.playlist.delete_track()
                if self.playlist.length > 0:
                    self.track_init()
                else:
                    self.playlist.current_track = None
                    self.ui.pause_button.setIcon(QIcon("icons/play.png"))
                    self.ui.name_song.setText('')
                    self.ui.image_song.setPixmap(QPixmap(''))
                    self.ui.time.setText('')
                    self.ui.time_slider.setValue(0)
                    self.is_track_initialized = False
                    mixer.music.stop()
            else:
                if self.playlist.length > 0:
                    self.playlist.delete_track()
                    self.playlist.current_track = self.playing_track
                if self.playlist.length == 0:
                    self.playlist.current_track = None
                    self.ui.name_song.setText('')
                    self.ui.image_song.setPixmap(QPixmap(''))
                    self.ui.time.setText('')
                    self.ui.time_slider.setValue(0)
                    self.is_track_initialized = False
                    mixer.music.stop()
            self.update_track_list()

    @staticmethod
    def input_box():
        """
        Окно ввода названия плейлиста
        """
        msg = QInputDialog()
        msg.setWindowIcon(QIcon("icons/player.png"))
        text, ok = QInputDialog.getText(msg, 'Music Player', 'Введите название плейлиста:')
        if ok:
            return text

    def update_track_list(self):
        """
        Обновление списка песен
        """
        self.ui.songs.clear()
        for track in self.playlist:
            self.ui.songs.addItem(track.data.name)

    def update_playlists(self):
        """
        Обновление списка плейлистов
        """
        self.ui.playlists.clear()
        for i in self.playlist_array:
            self.ui.playlists.addItem(i.name)

    def add_playlist(self):
        """
        Добавление плейлиста
        """
        playlist_name = self.input_box()
        if playlist_name:
            if not (playlist_name in [playlist.name for playlist in self.playlist_array]):
                new_playlist = Playlist(name=playlist_name)
                self.playlist_array.append(new_playlist)
                self.update_playlists()
                self.playlist = new_playlist
            else:
                self.message_box("Плейлист с таким названием уже есть", "Введите другое название")
        else:
            self.message_box("Введена пустая строка", "Напишите название плейлиста")

    def delete_playlist(self):
        """
        Удаление плейлиста
        """
        if self.playlist_array:
            if self.playlist is not None:
                if self.playlist == self.playing_playlist:
                    self.pause()
                    self.ui.name_song.setText('')
                    self.ui.image_song.setPixmap(QPixmap(''))
                    self.ui.name_song.setText('')
                    self.ui.time_slider.setValue(0)
                    self.ui.time.setText('')
                    self.is_track_initialized = False
                self.playlist_array.remove(self.playlist)
                self.playlist = None
                self.update_playlists()
                self.ui.songs.clear()
            else:
                self.message_box("Нечего удалять", "Не выбран плейлист")
        else:
            self.message_box("Нечего удалять", "Список плейлистов пустой")

    @staticmethod
    def read_data_from_json() -> list:
        """
        Чтение данных из файла json
        """
        data = None
        if not os.stat('player_data.json').st_size == 0:
            dir_path = Path.cwd()
            path = Path(dir_path, 'player_data.json')
            with open(path, encoding="utf-8") as outfile:
                data = json.load(outfile)
        return data

    def write_data_in_json(self):
        """
        Запись данных в файл json
        """
        data = []
        if len(self.playlist_array) > 0:
            for item in self.playlist_array:
                tracks = []
                current_track = item.head
                for i in range(item.length):
                    tracks.append(current_track.data.path)
                    current_track = current_track.next_item

                data.append({
                    'name': item.name,
                    'tracks': tracks
                })
        with open('player_data.json', 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, indent=2)

    def make_playlist_from_data(self):
        """
        Создание плейлистов с существующими данными
        """
        data = self.read_data_from_json()
        for playlist in data:
            name = playlist['name']
            new_playlist = Playlist(name=name)
            for song in playlist['tracks']:
                new_playlist.add_track(song)
            if name != '':
                self.playlist_array.append(new_playlist)
            else:
                self.playlist = new_playlist
                self.playlist_array.append(new_playlist)
                self.update_track_list()
        self.update_playlists()
        self.ui.songs.setCurrentRow(0)
