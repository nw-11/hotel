from.entidade import Entidade

class Item_reserva(Entidade):
    def __init__(self, nome, price, id  = None):
        super().__init__(id)
        self.nome = nome
        self.price = float(price)