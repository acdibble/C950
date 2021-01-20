from __future__ import annotations
from typing import TYPE_CHECKING, Union
from datastructures.hashmap import HashMap
if TYPE_CHECKING:
    from wgups.place import Place

StrOrPlace = Union[str, 'Place']


class Graph:
    __edges: HashMap[StrOrPlace, HashMap[StrOrPlace, float]] = HashMap()

    def add_vertex(self, vertex: Place) -> None:
        self.__edges.put(vertex, HashMap[StrOrPlace, float]())

    def add_edge(self, vertex1: Place, vertex2: Place, distance: float) -> None:
        self.__add_edge(vertex1, vertex2, distance)
        self.__add_edge(vertex2, vertex1, distance)

    def __add_edge(self, vertex1: Place, vertex2: Place, distance: float) -> None:
        self.__edges.get(vertex1).put(vertex2, distance)

    def get_distance(self, vertex1: StrOrPlace, vertex2: StrOrPlace) -> float:
        return self.__edges.get(vertex1).get(vertex2)

    def debug(self):
        pass

    def edges(self):
        return self.__edges
