from __future__ import annotations
from typing import Generic, TYPE_CHECKING, TypeVar, Union
from datastructures.hashmap import HashMap
if TYPE_CHECKING:
    from wgups.place import Place

StrOrPlace = Union[str, 'Place']

T = TypeVar('T')


class Graph(Generic[T]):
    __edges: HashMap[T, HashMap[T, float]] = HashMap()

    def add_vertex(self, vertex: T) -> None:
        self.__edges.put(vertex, HashMap[T, float]())

    def add_edge(self, vertex1: T, vertex2: T, distance: float) -> None:
        self.__add_edge(vertex1, vertex2, distance)
        self.__add_edge(vertex2, vertex1, distance)

    def __add_edge(self, vertex1: T, vertex2: T, distance: float) -> None:
        self.__edges.get(vertex1).put(vertex2, distance)

    def distance_between(self, vertex1: T, vertex2: T) -> float:
        return self.__edges.get(vertex1).get(vertex2)
