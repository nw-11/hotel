from modelo.entidade import Entidade
from modelo.item_reserva import ItemReserva
from datetime import datetime


class Reserva(Entidade):

    def __init__(self, hospede, quarto, checkin, checkout, id=None):

        super().__init__(id)

        Reserva.validar_datas(
            checkin,
            checkout
        )

        self.hospede = hospede
        self.quarto = quarto
        self.checkin = checkin
        self.checkout = checkout
        self.itens = []

    # ------------------------------------------------------------
    # gerenciamento de itens
    # ------------------------------------------------------------

    def adicionar_item(
        self,
        produto,
        quantidade=1
    ):

        if quantidade < 1:

            raise ValueError(
                "A quantidade deve ser pelo menos 1."
            )

        # se já existe produto, soma quantidade

        for item in self.itens:

            if item.produto.id == produto.id:

                item.quantidade += quantidade

                return item

        # cria novo item

        item = ItemReserva(
            produto,
            quantidade
        )

        self.itens.append(item)

        return item

    def remover_item(self, item):

        if item in self.itens:

            self.itens.remove(item)

            return True

        return False

    # ------------------------------------------------------------
    # cálculos
    # ------------------------------------------------------------

    def total_itens(self):

        return sum(

            item.subtotal

            for item in self.itens
        )

    def total_geral(self):

        entrada = datetime.strptime(
            self.checkin,
            "%d/%m/%Y"
        )

        saida = datetime.strptime(
            self.checkout,
            "%d/%m/%Y"
        )

        noites = (
            saida - entrada
        ).days

        return (

            noites
            *
            self.quarto.diaria

            +

            self.total_itens()
        )

    @property
    def numero_de_noites(self):

        entrada = datetime.strptime(
            self.checkin,
            "%d/%m/%Y"
        )

        saida = datetime.strptime(
            self.checkout,
            "%d/%m/%Y"
        )

        return (
            saida - entrada
        ).days

    # ------------------------------------------------------------
    # validação
    # ------------------------------------------------------------

    @staticmethod
    def validar_datas(
        checkin,
        checkout
    ):

        entrada = datetime.strptime(
            checkin,
            "%d/%m/%Y"
        )

        saida = datetime.strptime(
            checkout,
            "%d/%m/%Y"
        )

        if saida <= entrada:

            raise ValueError(
                "Checkout deve ser posterior ao checkin."
            )

    # ------------------------------------------------------------
    # representação
    # ------------------------------------------------------------

    def __str__(self):

        linhas = [

            f"Reserva ID : {self.id}",

            f"Hóspede    : {self.hospede.nome}",

            f"Quarto     : {self.quarto.numero} ({self.quarto.tipo})",

            f"Check-in   : {self.checkin}",

            f"Check-out  : {self.checkout}",

            f"Noites     : {self.numero_de_noites}",

            f"Diária     : R$ {self.quarto.diaria:.2f}"
        ]

        if self.itens:

            linhas.append(
                "Itens extras:"
            )

            for item in self.itens:

                linhas.append(
                    f"  • {item}"
                )

        linhas.append(
            f"Total itens: R$ {self.total_itens():.2f}"
        )

        linhas.append(
            f"TOTAL GERAL: R$ {self.total_geral():.2f}"
        )

        return "\n".join(
            linhas
        )