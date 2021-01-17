from typing import Union
from wgups import Place
from datastructures.hashmap import HashMap

StrOrPlace = Union[str, Place]


class Graph:
    __vertices: HashMap[StrOrPlace, Place] = HashMap()
    __edges: HashMap[StrOrPlace, HashMap[StrOrPlace, float]] = HashMap()

    def add_vertex(self, vertex: Place) -> None:
        self.__vertices.put(vertex, vertex)
        self.__edges.put(vertex, HashMap[StrOrPlace, float]())

    def add_edge(self, vertex1: Place, vertex2: Place, distance: float) -> None:
        self.__add_edge(vertex1, vertex2, distance)
        self.__add_edge(vertex2, vertex1, distance)

    def __add_edge(self, vertex1: Place, vertex2: Place, distance: float) -> None:
        if (hashmap := self.__edges.get(vertex1)) == None:
            hashmap = HashMap[StrOrPlace, float]()
            self.__edges.put(vertex1, hashmap)

        hashmap.put(vertex2, distance)

    def get_distance(self, vertex1: StrOrPlace, vertex2: StrOrPlace) -> float:
        return self.__edges.get(vertex1).get(vertex2)
