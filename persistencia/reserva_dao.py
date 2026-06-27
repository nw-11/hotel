from modelo.reserva import Reserva
from modelo.item_reserva import ItemReserva
from persistencia.entidade_dao import EntidadeDAO
from persistencia.arquivo_utils import (
    ARQ_RESERVAS,
    ARQ_ITENS,
    ler_linhas,
    escrever_linhas
)


class ReservaDAO(EntidadeDAO[Reserva]):
    def __init__(self, hospedeDAO, quartoDAO, produtoDAO):
        super().__init__()
        self.hospedeDAO = hospedeDAO
        self.quartoDAO = quartoDAO
        self.produtoDAO = produtoDAO

    def salvar(self, reserva):
        super().salvar(reserva)

        reserva.quarto.disponivel = False
        self.quartoDAO.atualizar(reserva.quarto)

    def apagar(self, id):
        reserva = super().apagar(id)

        reserva.quarto.disponivel = True
        self.quartoDAO.atualizar(reserva.quarto)

        return reserva

    def persistir(self):
        linhas_reservas = []
        linhas_itens = []

        for r in self._ordenadas_por_id():
            linhas_reservas.append([
                r.id,
                r.hospede.id,
                r.quarto.id,
                r.checkin,
                r.checkout
            ])

            for item in r.itens:
                linhas_itens.append([
                    r.id,
                    item.produto.id,
                    item.quantidade
                ])

        escrever_linhas(
            ARQ_RESERVAS,
            linhas_reservas
        )

        escrever_linhas(
            ARQ_ITENS,
            linhas_itens
        )

    def recuperar(self):
        self.entidades.clear()

        linhas_itens = ler_linhas(ARQ_ITENS)

        for linha in ler_linhas(ARQ_RESERVAS):
            hospede = self.hospedeDAO.carregar(
                int(linha[1])
            )

            quarto = self.quartoDAO.carregar(
                int(linha[2])
            )

            reserva = Reserva(
                hospede,
                quarto,
                linha[3],
                linha[4],
                id=int(linha[0])
            )

            reserva.itens = self._recuperar_itens(
                reserva.id,
                linhas_itens
            )

            self.entidades.add(reserva)

    def _recuperar_itens(self, reserva_id, linhas_itens):
        itens = []

        for linha in linhas_itens:
            if int(linha[0]) == reserva_id:
                produto = self.produtoDAO.carregar(
                    int(linha[1])
                )

                itens.append(
                    ItemReserva(
                        produto,
                        int(linha[2])
                    )
                )

        return itens
