from modelo.hospede import Hospede
from modelo.quarto import Quarto
from modelo.produto import Produto
from modelo.reserva import Reserva
from modelo.item_reserva import ItemReserva

from persistencia.entidade_dao import EntidadeDAO
from persistencia.persistence_exception import PersistenceException
from persistencia.arquivo_utils import (
    ARQ_HOSPEDES,
    ARQ_QUARTOS,
    ARQ_PRODUTOS,
    ARQ_RESERVAS,
    ARQ_ITENS,
    ler_linhas,
    escrever_linhas
)


def hospede_para_linha(h):
    return [h.id, h.nome, h.cpf, h.email, h.telefone]


def hospede_de_linha(linha):
    return Hospede(linha[1], linha[2], linha[3], linha[4], id=int(linha[0]))


def quarto_para_linha(q):
    return [q.id, q.numero, q.tipo, q.diaria, int(q.disponivel)]


def quarto_de_linha(linha):
    return Quarto(linha[1], linha[2], float(linha[3]), bool(int(linha[4])), id=int(linha[0]))


def produto_para_linha(p):
    return [p.id, p.nome, p.preco, p.categoria]


def produto_de_linha(linha):
    return Produto(linha[1], float(linha[2]), linha[3], id=int(linha[0]))


class DAOFactory:
    @staticmethod
    def _validar_hospede_sem_reserva_ativa(hospede):
        for reserva in DAOFactory.reservaDAO.entidades:
            if reserva.hospede.id == hospede.id:
                raise PersistenceException(
                    "apagar",
                    "não é possível apagar hóspede com reserva ativa",
                    hospede.id
                )

    @staticmethod
    def _validar_quarto_sem_reserva_ativa(quarto):
        for reserva in DAOFactory.reservaDAO.entidades:
            if reserva.quarto.id == quarto.id:
                raise PersistenceException(
                    "apagar",
                    "não é possível apagar quarto com reserva ativa",
                    quarto.id
                )

    @staticmethod
    def _apos_salvar_reserva(reserva):
        reserva.quarto.disponivel = False
        DAOFactory.quartoDAO.atualizar(reserva.quarto)

    @staticmethod
    def _apos_apagar_reserva(reserva):
        reserva.quarto.disponivel = True
        DAOFactory.quartoDAO.atualizar(reserva.quarto)

    @staticmethod
    def _persistir_reservas(dao):
        linhas_reservas = []
        linhas_itens = []

        for r in dao._ordenadas_por_id():
            linhas_reservas.append([r.id, r.hospede.id, r.quarto.id, r.checkin, r.checkout])

            for item in r.itens:
                linhas_itens.append([r.id, item.produto.id, item.quantidade])

        escrever_linhas(ARQ_RESERVAS, linhas_reservas)
        escrever_linhas(ARQ_ITENS, linhas_itens)

    @staticmethod
    def _recuperar_reservas(dao):
        dao.entidades.clear()
        linhas_itens = ler_linhas(ARQ_ITENS)

        for linha in ler_linhas(ARQ_RESERVAS):
            hospede = DAOFactory.hospedeDAO.carregar(int(linha[1]))
            quarto = DAOFactory.quartoDAO.carregar(int(linha[2]))

            reserva = Reserva(hospede, quarto, linha[3], linha[4], id=int(linha[0]))
            reserva.itens = DAOFactory._recuperar_itens(reserva.id, linhas_itens)

            dao.entidades.add(reserva)

    @staticmethod
    def _recuperar_itens(reserva_id, linhas_itens):
        itens = []

        for linha in linhas_itens:
            if int(linha[0]) == reserva_id:
                produto = DAOFactory.produtoDAO.carregar(int(linha[1]))
                itens.append(ItemReserva(produto, int(linha[2])))

        return itens

    hospedeDAO = EntidadeDAO(
        "Hospede",
        arquivo=ARQ_HOSPEDES,
        para_linha=hospede_para_linha,
        de_linha=hospede_de_linha,
        antes_apagar=_validar_hospede_sem_reserva_ativa.__func__
    )

    quartoDAO = EntidadeDAO(
        "Quarto",
        arquivo=ARQ_QUARTOS,
        para_linha=quarto_para_linha,
        de_linha=quarto_de_linha,
        antes_apagar=_validar_quarto_sem_reserva_ativa.__func__
    )

    produtoDAO = EntidadeDAO(
        "Produto",
        arquivo=ARQ_PRODUTOS,
        para_linha=produto_para_linha,
        de_linha=produto_de_linha
    )

    reservaDAO = EntidadeDAO(
        "Reserva",
        persistir_func=_persistir_reservas.__func__,
        recuperar_func=_recuperar_reservas.__func__,
        apos_salvar=_apos_salvar_reserva.__func__,
        apos_apagar=_apos_apagar_reserva.__func__
    )

    @staticmethod
    def getHospedeDAO():
        return DAOFactory.hospedeDAO

    @staticmethod
    def getQuartoDAO():
        return DAOFactory.quartoDAO

    @staticmethod
    def getProdutoDAO():
        return DAOFactory.produtoDAO

    @staticmethod
    def getReservaDAO():
        return DAOFactory.reservaDAO

    @staticmethod
    def carregarQuartosDisponiveis():
        return DAOFactory.quartoDAO.filtrar(lambda q: q.disponivel)

    @staticmethod
    def carregarProdutosPorCategoria(categoria):
        return DAOFactory.produtoDAO.filtrar(
            lambda p: p.categoria.lower() == categoria.lower()
        )

    @staticmethod
    def recuperarTodos():
        DAOFactory.hospedeDAO.recuperar()
        DAOFactory.quartoDAO.recuperar()
        DAOFactory.produtoDAO.recuperar()
        DAOFactory.reservaDAO.recuperar()

    @staticmethod
    def persistirTodos():
        DAOFactory.hospedeDAO.persistir()
        DAOFactory.quartoDAO.persistir()
        DAOFactory.produtoDAO.persistir()
        DAOFactory.reservaDAO.persistir()
