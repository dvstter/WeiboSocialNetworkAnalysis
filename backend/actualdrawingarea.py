from tkinter.ttk import *
from backend.srvmod.dbs import Database
from .graph import *
from .uimod.detail import DetailTable
from .uimod.image import PreviewImage

class ActualDrawingArea(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()

        self.__table = None
        self.__image = None
        self.__dbs = Database()

        self.__create_widgets()
        # Notice: set_table_data() must be called before set_image_data()
        self.set_table_data()
        self.set_image_data()
        self.__place_widgets()

    def set_table_data(self):
        for id_ in self.__dbs.get_all_user_ids():
            name = self.__dbs.get_name(id_)
            attentions = self.__dbs.get_attentions(id_)
            fans = self.__dbs.get_fans(id_)
            blogs = self.__dbs.get_blogs(id_)
            s_ratio = self.__process_ratio_data(self.__dbs.get_star_ratio(id_))
            c_ratio = self.__process_ratio_data(self.__dbs.get_comment_ratio(id_))
            r_ratio = self.__process_ratio_data(self.__dbs.get_repost_ratio(id_))

            self.__table.add_related_person(id_, name, fans, attentions, blogs, s_ratio, c_ratio, r_ratio)

        self.__table.sort_data(lambda x:(float(x[5][:-1])+float(x[6][:-1])+float(x[7][:-1])), True)
        self.__table.update_table()

    def set_image_data(self):
        graph = RelationGraph()
        key_p = Person("锤子科技")
        graph.add_person(key_p)

        counter = 20 # only show the closest 20 persons
        data = self.__table.get_data()
        for each in data:
            name = each[1]
            #relation = float(each[5][:-1]) + float(each[6][:-1]) + float(each[7][:-1])

            p = Person(name)
            graph.add_person(p)
            graph.add_relation(p, key_p)
            counter -= 1
            if counter == 0:
                break

        graph.draw_graph("resource/relation.jpg")
        self.__image.load("resource/relation.jpg")

    def __process_ratio_data(self, ratio):
        ratio = float(ratio) * 100
        return "{:.2f}%".format(ratio)

    def __create_widgets(self):
        self.__table = DetailTable()
        self.__image = PreviewImage()

    def __place_widgets(self):
        self.__table.grid(row=0, column=0, sticky="we")
        self.__image.grid(row=1, column=0, sticky="we")