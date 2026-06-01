from modelo.entidade import Entidade
from modelo.banco_de_dados import Bancodedados
from modelo.item_reserva import ItemReserva

class Reserva(Entidade):
    def __init__(self, hospede, quarto, checkin, checkout, id=None):
        super().__init__(id)
        self.hospede = hospede
        self.quarto = quarto
        self.checkin = checkin
        self.checkout = checkout
        self.itens = []

    def salvar(self):
        Bancodedados.salva_reserva(self)
        self.persistido = True

    def atualizar(self):
        Bancodedados.atualiza_reserva(self)

    def apagar(self):
        return Bancodedados.apaga_reserva(self)

    def adicionar_item(self, nome, preco):
        item = ItemReserva(nome, preco)
        self.itens.append(item)
        if self.persistido:
            Bancodedados.salva_itens_reserva(self)
        return item

    def remover_item(self, item):
        if item in self.itens:
            self.itens.remove(item)
            if self.persistido:
                Bancodedados.salva_itens_reserva(self)
            return True
        return False

    def total_itens(self):
        return sum(i.preco for i in self.itens)

    def total_geral(self):
        return self.quarto.diaria + self.total_itens()

    def __str__(self):
        return f"Reserva {self.id} - {self.hospede.nome}"
