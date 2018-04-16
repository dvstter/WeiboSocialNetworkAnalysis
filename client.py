from backend.graph import Person, RelationGraph
from tkinter import *
from backend.actualdrawingarea import ActualDrawingArea

class Client(Tk):
    def __init__(self, master=None):
        super().__init__(master)

if __name__ == "__main__":
    client = Client()
    client.title("Social Network Analysis")
    area = ActualDrawingArea(client)
    client.mainloop()