from typing import Generator, Generic, TypeVar

Key = TypeVar('Key')
Value = TypeVar('Value')


def gen_primes() -> Generator[int, None, None]:
    primes = [2]

    while True:
        prime = primes[-1]
        yield prime
        while any(map(lambda p: prime % p == 0, primes)):
            prime += 1

        primes.append(prime)


class HashMap(Generic[Key, Value]):
    __max_bucket_size = 5
    __storage: list[list[tuple[Key, Value]]]

    def __init__(self) -> None:
        self.__gen = gen_primes()
        self.__storage_size = next(self.__gen)
        self.__initialize_storage()
        self.size = 0
        self.__can_resize = True

    def put(self, key: Key, value: Value) -> None:
        bucket = self.__get_bucket(key)
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket[i] = (key, value)
                break
        else:
            bucket.append((key, value))
            if self.__can_resize:
                self.size += 1

        if len(bucket) >= self.__max_bucket_size:
            self.__resize()

    def get(self, key: Key) -> Value:
        for (bucket_key, value) in self.__get_bucket(key):
            if bucket_key == key:
                return value

        raise KeyError

    def __get_bucket(self, key: Key) -> list[tuple[Key, Value]]:
        index = hash(key) % self.__storage_size
        return self.__storage[index]

    def __initialize_storage(self) -> None:
        self.__storage = [[] for _ in range(self.__storage_size)]

    def __resize(self) -> None:
        if not self.__can_resize:
            return
        self.__can_resize = False

        self.__storage_size = next(self.__gen)
        old_storage = self.__storage
        self.__initialize_storage()
        for bucket in old_storage:
            for (key, value) in bucket:
                self.put(key, value)
        self.__can_resize = True

    def __contains__(self, key: Key):
        for bucket in self.__storage:
            for (k, _) in bucket:
                if k == key:
                    return True

        return False
