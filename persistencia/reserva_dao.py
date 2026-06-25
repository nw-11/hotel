from modelo.reserva import Reserva
from modelo.item_reserva import ItemReserva

from persistencia.persistence_exception import PersistenceException
from persistencia.arquivo_utils import *

from persistencia.hospede_dao import HospedeDAO
from persistencia.quarto_dao import QuartoDAO
from persistencia.produto_dao import ProdutoDAO


class ReservaDAO:

    def __init__(self):

        self.hospedeDAO = HospedeDAO()
        self.quartoDAO = QuartoDAO()
        self.produtoDAO = ProdutoDAO()

    # -------------------------------------------------------------
    # salvar
    # -------------------------------------------------------------

    def salvar(self, reserva):

        linhas = ler_linhas(ARQ_RESERVAS)

        for linha in linhas:

            if int(linha[0]) == reserva.id:

                raise PersistenceException(
                    "salvar",
                    "Reserva já existe",
                    reserva.id
                )

        linhas.append([
            reserva.id,
            reserva.hospede.id,
            reserva.quarto.id,
            reserva.checkin,
            reserva.checkout
        ])

        escrever_linhas(
            ARQ_RESERVAS,
            linhas
        )

        # marca quarto como ocupado

        reserva.quarto.disponivel = False

        self.quartoDAO.atualizar(
            reserva.quarto
        )

        # salva itens da reserva

        self.salvarItens(
            reserva
        )

    # -------------------------------------------------------------
    # atualizar
    # -------------------------------------------------------------

    def atualizar(self, reserva):

        linhas = ler_linhas(
            ARQ_RESERVAS
        )

        encontrou = False

        for i, linha in enumerate(linhas):

            if int(linha[0]) == reserva.id:

                linhas[i] = [
                    reserva.id,
                    reserva.hospede.id,
                    reserva.quarto.id,
                    reserva.checkin,
                    reserva.checkout
                ]

                encontrou = True

        if not encontrou:

            raise PersistenceException(
                "atualizar",
                "Reserva inexistente",
                reserva.id
            )

        escrever_linhas(
            ARQ_RESERVAS,
            linhas
        )

        # reescreve itens

        self.salvarItens(
            reserva
        )

    # -------------------------------------------------------------
    # apagar
    # -------------------------------------------------------------

    def apagar(self, id):

        reserva = self.carregar(id)

        linhas = ler_linhas(
            ARQ_RESERVAS
        )

        novas = [
            l for l in linhas
            if int(l[0]) != id
        ]

        if len(novas) == len(linhas):

            raise PersistenceException(
                "apagar",
                "Reserva inexistente",
                id
            )

        escrever_linhas(
            ARQ_RESERVAS,
            novas
        )

        # remove itens

        itens = ler_linhas(
            ARQ_ITENS
        )

        novas_itens = [

            i for i in itens

            if int(i[0]) != id
        ]

        escrever_linhas(
            ARQ_ITENS,
            novas_itens
        )

        # libera quarto

        reserva.quarto.disponivel = True

        self.quartoDAO.atualizar(
            reserva.quarto
        )

    # -------------------------------------------------------------
    # carregar
    # -------------------------------------------------------------

    def carregar(self, id):

        linhas = ler_linhas(
            ARQ_RESERVAS
        )

        for linha in linhas:

            if int(linha[0]) == id:

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
                    int(linha[0])
                )

                reserva.itens = self.carregarItens(
                    reserva.id
                )

                return reserva

        raise PersistenceException(
            "carregar",
            "Reserva não encontrada",
            id
        )

    # -------------------------------------------------------------
    # carregar todos
    # -------------------------------------------------------------

    def carregarTodos(self):

        linhas = ler_linhas(
            ARQ_RESERVAS
        )

        if len(linhas) == 0:

            raise PersistenceException(
                "carregarTodos",
                "Nenhuma reserva salva",
                None
            )

        reservas = []

        for linha in linhas:

            reservas.append(
                self.carregar(
                    int(linha[0])
                )
            )

        reservas.sort()

        return reservas

    # -------------------------------------------------------------
    # itens reserva
    # -------------------------------------------------------------

    def carregarItens(self, reserva_id):

        itens = []

        linhas = ler_linhas(
            ARQ_ITENS
        )

        for linha in linhas:

            if int(linha[0]) == reserva_id:

                produto = self.produtoDAO.carregar(
                    int(linha[1])
                )

                item = ItemReserva(
                    produto,
                    int(linha[2])
                )

                itens.append(item)

        return itens

    def salvarItens(self, reserva):

        # remove antigos

        linhas = ler_linhas(
            ARQ_ITENS
        )

        linhas = [

            l for l in linhas

            if int(l[0]) != reserva.id
        ]

        # adiciona atuais

        for item in reserva.itens:

            linhas.append([
                reserva.id,
                item.produto.id,
                item.quantidade
            ])

        escrever_linhas(
            ARQ_ITENS,
            linhas
        )