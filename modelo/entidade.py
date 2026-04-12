from abc import ABC, abstractmethod

class Entidade(ABC):                      #classe entidade abstrata
    def __init__(self, id=None):
        self.id = id
        self.persistido = False

    @abstractmethod
    def salvar(self):
        pass

    @abstractmethod
    def atualizar(self):
        pass

    @abstractmethod
    def apagar(self):
        pass