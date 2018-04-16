from tkinter.ttk import *
from .graph import *
from .uimod.detail import DetailTable
from .uimod.image import PreviewImage

class ActualDrawingArea(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()

        self.__table = None
        self.__image = None

        self.__create_widgets()
        self.set_table_data()
        self.set_image_data()
        self.__place_widgets()

    def set_table_data(self):
        with open("result.txt", encoding="utf-8") as fh:
            for line in fh:
                id_, name, attentions, fans, blogs = line.strip().split("\t")
                self.__table.add_related_person(id_, name, fans, attentions, blogs, "-", "-", "-")

        self.__table.update_table()

    def set_image_data(self):
        graph = RelationGraph()
        key_p = Person("锤子科技")
        graph.add_person(key_p)

        counter = 20
        with open("result.txt", encoding="utf-8") as fh:
            for line in fh:
                _, name, _, _, _ = line.strip().split("\t")

                if not counter == 0:
                    p = Person(name)
                    graph.add_person(p)
                    graph.add_relation(p, key_p)
                    counter -= 1

        graph.draw_graph("resource/relation.jpg")
        self.__image.load("resource/relation.jpg")

    def __create_widgets(self):
        self.__table = DetailTable()
        self.__image = PreviewImage()

    def __place_widgets(self):
        self.__table.grid(row=0, column=0, sticky="we")
        self.__image.grid(row=1, column=0, sticky="we")