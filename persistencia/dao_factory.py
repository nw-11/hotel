from persistencia.hospede_dao import HospedeDAO
from persistencia.quarto_dao import QuartoDAO
from persistencia.produto_dao import ProdutoDAO
from persistencia.reserva_dao import ReservaDAO


class DAOFactory:
    hospedeDAO = HospedeDAO()
    quartoDAO = QuartoDAO()
    produtoDAO = ProdutoDAO()
    reservaDAO = ReservaDAO(
        hospedeDAO,
        quartoDAO,
        produtoDAO
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
