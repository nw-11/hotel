import unittest

from modelo.hospede import Hospede
from modelo.quarto import Quarto
from modelo.reserva import Reserva

from persistencia.dao_factory import DAOFactory
from persistencia.persistence_exception import PersistenceException


class TesteQuartoDAO(unittest.TestCase):

    def setUp(self):
        self.hospedeDAO = DAOFactory.getHospedeDAO()
        self.quartoDAO = DAOFactory.getQuartoDAO()
        self.produtoDAO = DAOFactory.getProdutoDAO()
        self.reservaDAO = DAOFactory.getReservaDAO()

        self.hospedeDAO.entidades.clear()
        self.quartoDAO.entidades.clear()
        self.produtoDAO.entidades.clear()
        self.reservaDAO.entidades.clear()

        self.dao = self.quartoDAO

    # ---------------- SALVAR ----------------

    def test_salvar_id_novo(self):
        q = Quarto("101", "Suite", 300.0)
        q.id = 6000

        self.dao.salvar(q)

        resultado = self.dao.carregar(6000)

        self.assertEqual(resultado.numero, "101")

    def test_salvar_id_existente(self):
        q = Quarto("102", "Luxo", 250.0)
        q.id = 6001

        self.dao.salvar(q)

        with self.assertRaises(PersistenceException):
            self.dao.salvar(q)

    # ---------------- ATUALIZAR ----------------

    def test_atualizar_id_inexistente(self):
        q = Quarto("999", "Suite", 100.0)
        q.id = 9999

        with self.assertRaises(PersistenceException):
            self.dao.atualizar(q)

    def test_atualizar_id_existente(self):
        q = Quarto("103", "Standard", 100.0)
        q.id = 6002

        self.dao.salvar(q)

        q.diaria = 150.0

        self.dao.atualizar(q)

        novo = self.dao.carregar(6002)

        self.assertEqual(novo.diaria, 150.0)

    # ---------------- APAGAR ----------------

    def test_apagar_id_inexistente(self):
        with self.assertRaises(PersistenceException):
            self.dao.apagar(8888)

    def test_apagar_id_existente_sem_reserva_ativa(self):
        q = Quarto("104", "Suite", 500.0)
        q.id = 6003

        self.dao.salvar(q)

        removido = self.dao.apagar(6003)

        self.assertEqual(removido.id, 6003)

        with self.assertRaises(PersistenceException):
            self.dao.carregar(6003)

    def test_nao_apagar_quarto_com_reserva_ativa(self):
        h = Hospede(
            "Pedro",
            "123",
            "pedro@gmail.com",
            "9999"
        )
        h.id = 8005
        self.hospedeDAO.salvar(h)

        q = Quarto(
            "301",
            "Luxo",
            400.0
        )
        q.id = 6005
        self.quartoDAO.salvar(q)

        reserva = Reserva(
            h,
            q,
            "10/06/2026",
            "12/06/2026"
        )
        reserva.id = 10005
        self.reservaDAO.salvar(reserva)

        with self.assertRaises(PersistenceException):
            self.quartoDAO.apagar(6005)

        self.assertEqual(
            self.quartoDAO.carregar(6005).numero,
            "301"
        )

    # ---------------- CARREGAR ----------------

    def test_carregar_id_inexistente(self):
        with self.assertRaises(PersistenceException):
            self.dao.carregar(7777)

    def test_carregar_id_existente(self):
        q = Quarto("105", "Luxo", 450.0)
        q.id = 6004

        self.dao.salvar(q)

        resultado = self.dao.carregar(6004)

        self.assertEqual(resultado.numero, "105")

    # ---------------- FILTRAR DISPONÍVEIS ----------------

    def test_carregar_quartos_disponiveis(self):
        q1 = Quarto("101", "Standard", 100.0, disponivel=True)
        q1.id = 1

        q2 = Quarto("102", "Luxo", 200.0, disponivel=False)
        q2.id = 2

        self.quartoDAO.salvar(q1)
        self.quartoDAO.salvar(q2)

        disponiveis = DAOFactory.carregarQuartosDisponiveis()

        self.assertEqual(len(disponiveis), 1)
        self.assertEqual(disponiveis[0].numero, "101")


if __name__ == "__main__":
    unittest.main()
