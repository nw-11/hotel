from .entidade import Entidade
from .banco_de_dados import Bancodedados


class ItemReserva(Entidade):
    """
    Representa um item extra adicionado a uma reserva (ex: frigobar, serviço de quarto).
    Sempre pertence a uma Reserva — não existe de forma independente.
    """

    def __init__(self, nome, preco, id=None):
        super().__init__(id)
        self.nome = nome
        self.preco = float(preco)

    def salvar(self, reserva_id):
        """Itens precisam do ID da reserva pai para ser salvos."""
        Bancodedados.salva_item(self, reserva_id)
        self.persistido = True

    def atualizar(self):
        if not self.persistido:
            raise RuntimeError("Item ainda não foi salvo.")
        Bancodedados.atualiza_item(self)

    def apagar(self):
        if Bancodedados.apaga_item(self):
            self.id = None
            self.persistido = False
            return True
        return False

    def __str__(self):
        return f"{self.nome}: R$ {self.preco:.2f}"