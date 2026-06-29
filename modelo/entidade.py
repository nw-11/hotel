from abc import ABC


class Entidade(ABC):
    def __init__(self, id=None):
        self.id = id

    def __eq__(self, other):
        if isinstance(other, Entidade):
            return self.id == other.id
        return False
    
    def __gt__(self, other):
        return self.id > other.id

    def __lt__(self, other):
        return self.id < other.id

    def __hash__(self):
        return hash(self.id)