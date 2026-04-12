from .banco_de_dados import Bancodedados
from .entidade import Entidade

class Quarto(Entidade):
    def __init__(self, numero, tipo, diaria, disponivel = True, id = None):
        super().__init__(id)
        self.numero = numero
        self.tipo = tipo
        self.diaria = float(diaria)
        self.disponivel = disponivel

    def salvar(self):
        Bancodedados.salva_quarto(self)
    
    def atualizar(self):
        Bancodedados.atualiza_quarto(self)

    def apagar(self):
        Bancodedados.apaga_quarto(self)
        self.id = None
        self.persistido = False