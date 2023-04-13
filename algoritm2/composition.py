"""
Модуль с классом песни
"""

from tinytag import TinyTag


class Composition:
    """
    Класс песни
    """

    def __init__(self, path: str):
        """
        Конструктор класса
        :param path: Путь до файла c песней
        """
        audio = TinyTag.get(path, image=True)
        self.path: str = path
        self.artist = audio.artist
        self.album = audio.album
        self.title = audio.title
        self.duration = int(audio.duration)
        self.image = audio.get_image()
        self.name: str = path.split('/')[-1][0:-4]
        if not self.artist:
            self.artist = "Неизвестен"
        if not self.title:
            self.title = self.name
        if self.image:
            if self.title and self.artist:
                with open(f"songs_images/{self.artist.replace('/', ' ')}"
                          f" - {self.title.replace('/', ' ')}.jpeg", "wb") as image_file:
                    image_file.write(self.image)
                    self.image = f"songs_images/" \
                                 f"{self.artist.replace('/', ' ')} - {self.title.replace('/', ' ')}.jpeg"
            else:
                with open(f"songs_images/{self.name}.jpeg", "wb") as image_file:
                    image_file.write(self.image)
                    self.image = f"songs_images/{self.name}.jpeg"
