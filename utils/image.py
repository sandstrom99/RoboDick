import os
import random

IMG_EXTENSIONS = ["jpg", "jpeg", "png"]

class ImageDatasource():
    def __init__(self, path):
        self.path = path

    def get_random_path(self):
        files = os.listdir(self.path)
        random_image = ""
        extension = ""
        while not extension in IMG_EXTENSIONS:
            random_image = random.choice(files)
            extension = random_image.split(".")[-1]

        return os.path.join(self.path, random_image)

    def count(self):
        files = os.listdir(self.path)
        return len(files)
