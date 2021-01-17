from typing import Generic, TypeVar

Key = TypeVar('Key')
Value = TypeVar('Value')


class HashMap(Generic[Key, Value]):
    __max_bucket_size = 5
    __storage: list[list[tuple[Key, Value]]]
    size = 0

    def __init__(self) -> None:
        self.__storage_size: int = 10
        self.__initialize_storage()

    def put(self, key: Key, value: Value) -> None:
        bucket = self.__get_bucket(key)

        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket[i] = (key, value)
                break
        else:
            bucket.append((key, value))
            self.size += 1

        if len(bucket) == self.__max_bucket_size:
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
        self.__storage = [[] for i in range(self.__storage_size)]

    def __resize(self):
        self.__storage_size *= 2
        old_storage = self.__storage
        self.__initialize_storage()
        for bucket in old_storage:
            for (key, value) in bucket:
                self.put(key, value)

    def __contains__(self, key: Key):
        for bucket in self.__storage:
            for (k, v) in bucket:
                if k == key:
                    return True

        return False
