from tkinter.ttk import *

class DetailTable(Frame):
    IMG_WIDTH = 540
    IMG_HEIGHT = 540

    def __init__(self, master=None):
        super().__init__(master)
        self.grid()

        self.__table = None
        self.__data = []

        self.__create_widgets()
        self.__place_widgets()

    def __init_table(self):
        if self.__table is not None:
            self.__table.grid_forget()

        num_rows = len(self.__data)
        self.__table = Treeview(self, show="headings", column=("a", "b", "c", "d", "e", "f", "g"), height=num_rows, selectmode="none")

        for x in ["a", "b", "c", "d", "e", "f", "g"]:
            self.__table.column(x, anchor="center")

        self.__table.column("a", width=20, stretch=False)
        self.__table.column("b", width=100, stretch=False)
        self.__table.column("c", width=200, stretch=False)
        self.__table.column("d", width=100, stretch=False)
        self.__table.column("e", width=100, stretch=False)
        self.__table.column("f", width=100, stretch=False)
        self.__table.column("g", width=80, stretch=False)

        self.__table.heading("a", text="#")
        self.__table.heading("b", text="Id")
        self.__table.heading("c", text="Name")
        self.__table.heading("d", text="Followers")
        self.__table.heading("e", text="StarRatio")
        self.__table.heading("f", text="CommentRatio")
        self.__table.heading("g", text="Ralation")

    def add_related_person(self, id, name, followers, star_ratio, comment_ratio, relation):
        self.__data += [(id, name, followers, star_ratio, comment_ratio, relation)]

        self.__init_table()

        num_rows = len(self.__data)
        for idx in range(num_rows):
            self.__table.insert("", "end",
                                values=(str(idx + 1),
                                        self.__data[idx][0],
                                        self.__data[idx][1],
                                        self.__data[idx][2],
                                        self.__data[idx][3],
                                        self.__data[idx][4],
                                        self.__data[idx][5]))
        self.__place_widgets()

    def clear_table(self):
        self.__data = []
        self.__init_table()
        self.__place_widgets()

    def __create_widgets(self):
        self.__init_table()

    def __place_widgets(self):
        self.__table.grid(row=0, column=0, sticky="we")