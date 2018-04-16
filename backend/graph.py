import networkx as nx
import matplotlib.pyplot as plt

class Person:
    def __init__(self, name, intro = None, blogs = None, follows = None, fans = None):
        self.name = name
        self.intro = intro
        self.blogs = blogs
        self.follows = follows
        self.fans = fans

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return other.name == self.name

class RelationGraph:
    def __init__(self):
        self.__graph = nx.DiGraph()

    def add_person(self, person):
        if type(person) != Person:
            raise ValueError
        else:
            self.__graph.add_node(person, label=person.name)

    def add_persons(self, persons):
        for each in persons:
            if type(each) != Person:
                raise ValueError
            else:
                self.__graph.add_node(each)

    def add_relation(self, follower, be_followed, relation):
        if type(be_followed) != Person or type(follower) != Person:
            raise ValueError
        else:
            self.__graph.add_edge(follower, be_followed, attr={"relation":relation})

    def draw_graph(self, filename=None):
        labels = {}
        for each in self.__graph.nodes:
            labels[each] = each.name

        nx.draw(self.__graph, with_labels=True, labels=labels)
        if filename:
            plt.savefig(filename)
        else:
            plt.show()

if __name__ == "__main__":
    y = Person("Yang")
    k = Person("Kai")
    g = RelationGraph()

    g.add_persons([y, k])
    g.add_relation(y, k, 25)
    g.draw_graph()
