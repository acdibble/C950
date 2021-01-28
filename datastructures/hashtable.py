from typing import Generator, Generic, TypeVar
from utils import gen_primes

T = TypeVar('T')


class HashTable(Generic[T]):
    __max_bucket_size = 2
    size = 0
    __can_resize = True

    def __init__(self) -> None:
        self.__gen = gen_primes()
        self.__storage_size = next(self.__gen)
        self.__initialize_storage()

    def __initialize_storage(self) -> None:
        self.__storage = [[] for _ in range(self.__storage_size)]

    def __get_bucket(self, value: T) -> list[T]:
        index = hash(value) % self.__storage_size
        return self.__storage[index]

    def __resize(self) -> None:
        if not self.__can_resize:
            return
        self.__can_resize = False

        self.__storage_size = next(self.__gen)
        old_storage = self.__storage
        self.__initialize_storage()
        for bucket in old_storage:
            for (value) in bucket:
                self.put(value)
        self.__can_resize = True

    def put(self, value: T) -> None:
        bucket = self.__get_bucket(value)

        if not value in bucket:
            bucket.append(value)
            self.size += 1

        if len(bucket) > self.__max_bucket_size:
            self.__resize()

    def __contains__(self, value: T) -> bool:
        return value in self.__get_bucket(value)

    def __iter__(self) -> Generator[T, None, None]:
        for bucket in self.__storage:
            yield from bucket
