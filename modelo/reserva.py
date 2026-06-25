from modelo.entidade import Entidade
from modelo.banco_de_dados import Bancodedados
from modelo.item_reserva import ItemReserva
from datetime import datetime


class Reserva(Entidade):
    def __init__(self, hospede, quarto, checkin, checkout, id=None):
        super().__init__(id)
        Reserva.validar_datas(checkin, checkout)
        self.hospede  = hospede
        self.quarto   = quarto
        self.checkin  = checkin
        self.checkout = checkout
        self.itens    = []

    # ------------------------------------------------------------------
    # Implementação dos métodos abstratos de Entidade
    # ------------------------------------------------------------------

    def salvar(self):
        Bancodedados.salva_reserva(self)
        self.persistido = True

    def atualizar(self):
        Bancodedados.atualiza_reserva(self)
        if self.persistido:
            Bancodedados.salva_itens_reserva(self)

    def apagar(self):
        return Bancodedados.apaga_reserva(self)

    # ------------------------------------------------------------------
    # Gerenciamento de itens
    # ------------------------------------------------------------------

    def adicionar_item(self, produto, quantidade=1):
        """
        Associa um Produto cadastrado à reserva com a quantidade informada.

        Se o mesmo produto já existir na lista, incrementa a quantidade
        em vez de criar um segundo item duplicado.

        Parameters
        ----------
        produto   : Produto — produto cadastrado no sistema
        quantidade: int     — unidades consumidas (mínimo 1)

        Returns
        -------
        ItemReserva adicionado ou atualizado.
        """
        if quantidade < 1:
            raise ValueError("A quantidade deve ser pelo menos 1.")

        # Verifica se o produto já está na lista (agrega quantidades)
        for item in self.itens:
            if item.produto.id == produto.id:
                item.quantidade += quantidade
                if self.persistido:
                    Bancodedados.salva_itens_reserva(self)
                return item

        # Produto ainda não está na lista: cria novo ItemReserva
        item = ItemReserva(produto, quantidade)
        self.itens.append(item)
        if self.persistido:
            Bancodedados.salva_itens_reserva(self)
        return item

    def remover_item(self, item):
        """
        Remove um ItemReserva da reserva.

        Parameters
        ----------
        item : ItemReserva — item a ser removido

        Returns
        -------
        True se removido, False se não encontrado.
        """
        if item in self.itens:
            self.itens.remove(item)
            if self.persistido:
                Bancodedados.salva_itens_reserva(self)
            return True
        return False

    # ------------------------------------------------------------------
    # Cálculos
    # ------------------------------------------------------------------

    def total_itens(self):
        """Soma dos subtotais (preco × quantidade) de todos os itens."""
        return sum(item.subtotal for item in self.itens)

    def total_geral(self):
        """
        Custo total da estadia:
          (número de noites × diária do quarto) + total de itens extras
        """
        entrada = datetime.strptime(self.checkin,  "%d/%m/%Y")
        saida   = datetime.strptime(self.checkout, "%d/%m/%Y")
        noites  = (saida - entrada).days
        return noites * self.quarto.diaria + self.total_itens()

    @property
    def numero_de_noites(self):
        entrada = datetime.strptime(self.checkin,  "%d/%m/%Y")
        saida   = datetime.strptime(self.checkout, "%d/%m/%Y")
        return (saida - entrada).days

    # ------------------------------------------------------------------
    # Validação
    # ------------------------------------------------------------------

    @staticmethod
    def validar_datas(checkin, checkout):
        """Garante que checkout > checkin."""
        entrada = datetime.strptime(checkin,  "%d/%m/%Y")
        saida   = datetime.strptime(checkout, "%d/%m/%Y")
        if saida <= entrada:
            raise ValueError("Checkout deve ser posterior ao checkin.")

    # ------------------------------------------------------------------
    # Representação
    # ------------------------------------------------------------------

    def __str__(self):
        linhas = [
            f"Reserva ID : {self.id}",
            f"Hóspede    : {self.hospede.nome}",
            f"Quarto     : {self.quarto.numero} ({self.quarto.tipo})",
            f"Check-in   : {self.checkin}",
            f"Check-out  : {self.checkout}",
            f"Noites     : {self.numero_de_noites}",
            f"Diária     : R$ {self.quarto.diaria:.2f}",
        ]
        if self.itens:
            linhas.append("Itens extras:")
            for item in self.itens:
                linhas.append(f"  • {item}")
        linhas.append(f"Total itens: R$ {self.total_itens():.2f}")
        linhas.append(f"TOTAL GERAL: R$ {self.total_geral():.2f}")
        return "\n".join(linhas)
