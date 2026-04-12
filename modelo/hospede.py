from.entidade import Entidade
from.banco_de_dados import Bancodedados

class Hospede(Entidade):
    def __init__(self, nome, cpf, email, telefone, id = None):
        super().__init__(id)
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone

    def salvar(self):
        Bancodedados.salva_hospede(self)
    
    def atualizar(self):
        Bancodedados.atualiza_hospede(self)
    
    def apagar(self):
        Bancodedados.apaga_hospede(self)
        self.id = None
        self.persistido = False
