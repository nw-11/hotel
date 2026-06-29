import unittest

from modelo.hospede import Hospede
from modelo.quarto import Quarto
from modelo.reserva import Reserva

from persistencia.dao_factory import DAOFactory
from persistencia.persistence_exception import PersistenceException


class TesteReservaDAO(unittest.TestCase):

    def setUp(self):
        self.hospedeDAO = DAOFactory.getHospedeDAO()
        self.quartoDAO = DAOFactory.getQuartoDAO()
        self.produtoDAO = DAOFactory.getProdutoDAO()
        self.reservaDAO = DAOFactory.getReservaDAO()

        self.hospedeDAO.entidades.clear()
        self.quartoDAO.entidades.clear()
        self.produtoDAO.entidades.clear()
        self.reservaDAO.entidades.clear()

        self.hospede = Hospede(
            "Pedro",
            "123456789",
            "pedro@gmail.com",
            "99999999"
        )
        self.hospede.id = 8000
        self.hospedeDAO.salvar(self.hospede)

        self.quarto = Quarto(
            "201",
            "Suite",
            350.0
        )
        self.quarto.id = 9000
        self.quartoDAO.salvar(self.quarto)

    # ---------------- SALVAR ----------------

    def test_salvar_id_novo(self):
        reserva = Reserva(
            self.hospede,
            self.quarto,
            "10/06/2026",
            "12/06/2026"
        )
        reserva.id = 10000

        self.reservaDAO.salvar(reserva)

        resultado = self.reservaDAO.carregar(10000)

        self.assertEqual(resultado.id, 10000)
        self.assertFalse(resultado.quarto.disponivel)

    def test_salvar_id_existente(self):
        reserva = Reserva(
            self.hospede,
            self.quarto,
            "15/06/2026",
            "18/06/2026"
        )
        reserva.id = 10001

        self.reservaDAO.salvar(reserva)

        with self.assertRaises(PersistenceException):
            self.reservaDAO.salvar(reserva)

    # ---------------- ATUALIZAR ----------------

    def test_atualizar_id_inexistente(self):
        reserva = Reserva(
            self.hospede,
            self.quarto,
            "01/07/2026",
            "05/07/2026"
        )
        reserva.id = 99999

        with self.assertRaises(PersistenceException):
            self.reservaDAO.atualizar(reserva)

    def test_atualizar_id_existente(self):
        reserva = Reserva(
            self.hospede,
            self.quarto,
            "20/06/2026",
            "22/06/2026"
        )
        reserva.id = 10002

        self.reservaDAO.salvar(reserva)

        reserva.checkout = "25/06/2026"

        self.reservaDAO.atualizar(reserva)

        nova = self.reservaDAO.carregar(10002)

        self.assertEqual(nova.checkout, "25/06/2026")

    # ---------------- APAGAR ----------------

    def test_apagar_id_inexistente(self):
        with self.assertRaises(PersistenceException):
            self.reservaDAO.apagar(77777)

    def test_apagar_id_existente(self):
        reserva = Reserva(
            self.hospede,
            self.quarto,
            "05/08/2026",
            "08/08/2026"
        )
        reserva.id = 10003

        self.reservaDAO.salvar(reserva)

        removida = self.reservaDAO.apagar(10003)

        self.assertEqual(removida.id, 10003)
        self.assertTrue(removida.quarto.disponivel)

        with self.assertRaises(PersistenceException):
            self.reservaDAO.carregar(10003)

    # ---------------- CARREGAR ----------------

    def test_carregar_id_inexistente(self):
        with self.assertRaises(PersistenceException):
            self.reservaDAO.carregar(66666)

    def test_carregar_id_existente(self):
        reserva = Reserva(
            self.hospede,
            self.quarto,
            "10/09/2026",
            "15/09/2026"
        )
        reserva.id = 10004

        self.reservaDAO.salvar(reserva)

        resultado = self.reservaDAO.carregar(10004)

        self.assertEqual(resultado.id, 10004)


if __name__ == "__main__":
    unittest.main()
