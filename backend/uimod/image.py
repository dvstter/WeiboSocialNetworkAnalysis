from PIL import Image, ImageTk
from tkinter import *

class PreviewImage(Frame):
    IMG_WIDTH = 700
    IMG_HEIGHT = 700

    def __init__(self, master=None):
        super().__init__(master)
        self.grid()

        self.__image = None

        self.__create_widgets()
        self.__place_widgets()

    def __create_widgets(self):
        img = PhotoImage(width=type(self).IMG_WIDTH, height=type(self).IMG_HEIGHT)
        self.__image = Label(self, image=img)
        self.__image.image = img

    def __place_widgets(self):
        assert self.__image is not None

        self.__image.grid(row=0, column=0, sticky="we")

    @staticmethod
    def zoom_image(image):
        width, height = image.size
        ratio = float(width) / height
        t_width = PreviewImage.IMG_WIDTH
        t_height = PreviewImage.IMG_HEIGHT

        if width > height:
            t_height = int(t_width / ratio)
        else:
            t_width = int(t_height *ratio)

        image = image.resize((t_width, t_height), Image.ANTIALIAS)

        return image