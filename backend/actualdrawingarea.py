from tkinter.ttk import *
from .uimod.detail import DetailTable
from .uimod.image import PreviewImage

class ActualDrawingArea(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()

        self.__table = None
        self.__image = None

        self.__create_widgets()
        self.__place_widgets()

    def __create_widgets(self):
        self.__table = DetailTable()
        self.__image = PreviewImage()

    def __place_widgets(self):
        self.__table.grid(row=0, column=0, sticky="we")
        self.__image.grid(row=1, column=0, sticky="we")