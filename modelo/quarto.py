from modelo.entidade import Entidade
from modelo.banco_de_dados import Bancodedados


class Quarto(Entidade):
    def __init__(self, numero, tipo, diaria, disponivel=True, id=None):
        super().__init__(id)
        self.numero = numero
        self.tipo = tipo
        self.diaria = float(diaria)
        self.disponivel = disponivel

    def salvar(self):
        Bancodedados.salva_quarto(self)
        self.persistido = True

    def atualizar(self):
        if not self.persistido:
            raise RuntimeError("Quarto ainda não foi salvo. Use salvar() primeiro.")
        Bancodedados.atualiza_quarto(self)

    def apagar(self):
        if Bancodedados.apaga_quarto(self):
            self.id = None
            self.persistido = False
            return True
        return False

    def __str__(self):
        status = "Disponível" if self.disponivel else "Ocupado"
        return (
            f"ID: {self.id}\n"
            f"Número: {self.numero}\n"
            f"Tipo: {self.tipo}\n"
            f"Diária: R$ {self.diaria:.2f}\n"
            f"Status: {status}"
        )