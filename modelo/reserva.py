from .entidade import Entidade
from .banco_de_dados import Bancodedados
from .item_reserva import ItemReserva


class Reserva(Entidade):
    """
    Representa uma reserva de quarto feita por um hóspede.

    Composição:
        - hospede  : Hospede  (quem reservou)
        - quarto   : Quarto   (qual quarto)
        - checkin  : str      (data no formato DD/MM/AAAA)
        - checkout : str      (data no formato DD/MM/AAAA)
        - itens    : list[ItemReserva]  (serviços e consumos extras)
    """

    def __init__(self, hospede, quarto, checkin, checkout, id=None):
        super().__init__(id)
        self.hospede = hospede
        self.quarto = quarto
        self.checkin = checkin
        self.checkout = checkout
        self.itens: list[ItemReserva] = []

    def salvar(self):
        Bancodedados.salva_reserva(self)
        self.persistido = True
        for item in self.itens:
            if not item.persistido:
                item.salvar(self.id)

    def atualizar(self):
        if not self.persistido:
            raise RuntimeError("Reserva ainda não foi salva. Use salvar() primeiro.")
        Bancodedados.atualiza_reserva(self)

    def apagar(self):
        if Bancodedados.apaga_reserva(self):
            self.id = None
            self.persistido = False
            self.itens.clear()
            return True
        return False

    def adicionar_item(self, nome, preco):
        """Cria e persiste um item extra nesta reserva."""
        item = ItemReserva(nome, preco)
        if self._persistido:
            item.salvar(self.id)
        self.itens.append(item)
        return item

    def remover_item(self, item):
        """Remove um item extra desta reserva."""
        if item in self.itens:
            item.apagar()
            self.itens.remove(item)
            return True
        return False


    def total_itens(self):
        return sum(item.preco for item in self.itens)

    def total_geral(self):
        """Soma diária do quarto + todos os itens extras."""
        return self.quarto.diaria + self.total_itens()

    def __str__(self):
        linhas = [
            f"ID da Reserva : {self.id}",
            f"Hóspede       : {self.hospede.nome} (ID {self.hospede.id})",
            f"Quarto        : {self.quarto.numero} — {self.quarto.tipo}",
            f"Check-in      : {self.checkin}",
            f"Check-out     : {self.checkout}",
            f"Diária        : R$ {self.quarto.diaria:.2f}",
        ]
        if self.itens:
            linhas.append("Itens extras  :")
            for item in self.itens:
                linhas.append(f"  • {item}")
        linhas.append(f"TOTAL GERAL   : R$ {self.total_geral():.2f}")
        return "\n".join(linhas)