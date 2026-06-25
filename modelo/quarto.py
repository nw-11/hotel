from modelo.entidade import Entidade


class Quarto(Entidade):
    def __init__(self, numero, tipo, diaria, disponivel=True, id=None):
        super().__init__(id)
        self.numero = numero
        self.tipo = tipo
        self.diaria = float(diaria)
        self.disponivel = disponivel

    def __str__(self):
        status = "Disponível" if self.disponivel else "Ocupado"

        return (
            f"ID: {self.id}\n"
            f"Número: {self.numero}\n"
            f"Tipo: {self.tipo}\n"
            f"Diária: R$ {self.diaria:.2f}\n"
            f"Status: {status}"
        )