from modelo.entidade import Entidade


class Hospede(Entidade):
    def __init__(self, nome, cpf, email, telefone, id=None):
        super().__init__(id)
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone

    def __str__(self):
        return (
            f"ID: {self.id}\n"
            f"Nome: {self.nome}\n"
            f"CPF: {self.cpf}\n"
            f"E-mail: {self.email}\n"
            f"Telefone: {self.telefone}"
        )