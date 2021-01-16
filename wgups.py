from enum import Enum, auto


class Package:
    class Status(Enum):
        AT_HUB = auto()
        EN_ROUTE = auto()
        DELIVERED = auto()

    def __init__(self, id: str, address: str, city: str, state: str, zipcode: str, deadline: str, mass: str, notes: str):
        self.id = int(id)
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.mass = int(mass)
        self.notes = notes
        self.status = self.Status.AT_HUB

    def __str__(self) -> str:
        return f'id: {self.id}, address: {self.address}, status: {self.status}'


class Truck:
    pass
