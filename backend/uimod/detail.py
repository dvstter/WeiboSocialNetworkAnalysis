from tkinter.ttk import *

class DetailTable(Frame):
    IMG_WIDTH = 540
    IMG_HEIGHT = 540
    TABLE_HEIGHT = 10

    def __init__(self, master=None):
        super().__init__(master)
        self.grid()

        #self.__yscroller = None
        #self.__xscroller = None
        self.__table = None
        self.__data = []

        self.__create_widgets()
        self.__place_widgets()

    def __init_table(self):
        if self.__table is not None:
            self.__table.grid_forget()

        self.__table = Treeview(self, height=type(self).TABLE_HEIGHT, show="headings", column=("a", "b", "c", "d", "e", "f", "g", "h", "i"), selectmode="none")

        for x in ["a", "b", "c", "d", "e", "f", "g", "h", "i"]:
            self.__table.column(x, anchor="center")

        self.__table.column("a", width=20, stretch=False)
        self.__table.column("b", width=100, stretch=False)
        self.__table.column("c", width=200, stretch=False)
        self.__table.column("d", width=100, stretch=False)
        self.__table.column("e", width=100, stretch=False)
        self.__table.column("f", width=100, stretch=False)
        self.__table.column("g", width=80, stretch=False)
        self.__table.column("h", width=80, stretch=False)
        self.__table.column("i", width=80, stretch=False)

        self.__table.heading("a", text="#")
        self.__table.heading("b", text="用户身份号")
        self.__table.heading("c", text="昵称")
        self.__table.heading("d", text="粉丝数")
        self.__table.heading("e", text="关注数")
        self.__table.heading("f", text="博客数")
        self.__table.heading("g", text="点赞率")
        self.__table.heading("h", text="评论率")
        self.__table.heading("i", text="转发率")

    def add_related_person(self, id_, name, followers, attentions, blogs, star_ratio, comment_ratio, repost_ratio):
        self.__data += [(id_, name, followers, attentions, blogs, star_ratio, comment_ratio, repost_ratio)]

    def sort_data(self, key_value, reverse):
        self.__data = sorted(self.__data, key=key_value, reverse=reverse)

    def get_data(self):
        return self.__data

    def update_table(self):
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
                                        self.__data[idx][5],
                                        self.__data[idx][6],
                                        self.__data[idx][7]))

        self.__place_widgets()

    def clear_table(self):
        self.__data = []
        self.__init_table()
        self.__place_widgets()

    def __create_widgets(self):
        self.__init_table()

        #self.__yscroller = Scrollbar(self, orient="vertical", command=self.__table.yview)
        #self.__xscroller = Scrollbar(self, orient="horizontal", command=self.__table.xview)
        #self.__table.configure(yscrollcommand = self.__yscroller.set, xscrollcommand = self.__xscroller.set)

    def __place_widgets(self):
        self.__table.grid(row=0, column=0, sticky="we")
        #self.__yscroller.grid(row=0, column=1, sticky="ns")
        #self.__xscroller.grid(row=1, column=0, sticky="ew")