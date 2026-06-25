from abc import ABC, abstractmethod


class Entidade(ABC):
    def __init__(self, id=None):
        self.id = id
        self.persistido = False

    def is_persistido(self):
        return self.persistido

    @abstractmethod
    def salvar(self):
        pass

    @abstractmethod
    def atualizar(self):
        pass

    @abstractmethod
    def apagar(self):
        pass
