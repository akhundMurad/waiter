import uuid


def generate_uuid() -> uuid.UUID:
    return uuid.uuid4()


class Entity:
    def __init__(self, id: uuid.UUID = None):
        self.id = id or generate_uuid()

    def __eq__(self, other) -> bool:
        if isinstance(other, Entity):
            return self.id == other.id
        return False

    def __hash__(self) -> int:
        return hash(self.id)
