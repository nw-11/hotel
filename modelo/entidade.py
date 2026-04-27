from abc import ABC
     

class Entidade(ABC):                      
    def __init__(self, id=None):
        self.id = id
        self.persistido = False

    def is_persistido(self): return self.persistido

    
    def salvar(self):
        if self.persistido:
            return False
        self.persistido = True
        return True

    
    def atualizar(self):
        pass

    
    def apagar(self):
        pass