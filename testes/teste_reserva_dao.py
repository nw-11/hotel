import unittest

from modelo.hospede import Hospede
from modelo.quarto import Quarto
from modelo.produto import Produto
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

        self.dao = self.reservaDAO

    # ---------------- SALVAR ----------------

    def test_salvar_id_novo(self):
        reserva = Reserva(
            self.hospede,
            self.quarto,
            "10/06/2026",
            "12/06/2026"
        )
        reserva.id = 10000

        self.dao.salvar(reserva)

        resultado = self.dao.carregar(10000)

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

        self.dao.salvar(reserva)

        with self.assertRaises(PersistenceException):
            self.dao.salvar(reserva)

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
            self.dao.atualizar(reserva)

    def test_atualizar_id_existente(self):
        reserva = Reserva(
            self.hospede,
            self.quarto,
            "20/06/2026",
            "22/06/2026"
        )
        reserva.id = 10002

        self.dao.salvar(reserva)

        reserva.checkout = "25/06/2026"

        self.dao.atualizar(reserva)

        nova = self.dao.carregar(10002)

        self.assertEqual(nova.checkout, "25/06/2026")

    # ---------------- APAGAR ----------------

    def test_apagar_id_inexistente(self):
        with self.assertRaises(PersistenceException):
            self.dao.apagar(77777)

    def test_apagar_id_existente(self):
        reserva = Reserva(
            self.hospede,
            self.quarto,
            "05/08/2026",
            "08/08/2026"
        )
        reserva.id = 10003

        self.dao.salvar(reserva)

        removida = self.dao.apagar(10003)

        self.assertEqual(removida.id, 10003)
        self.assertTrue(removida.quarto.disponivel)

        with self.assertRaises(PersistenceException):
            self.dao.carregar(10003)

    # ---------------- CARREGAR ----------------

    def test_carregar_id_inexistente(self):
        with self.assertRaises(PersistenceException):
            self.dao.carregar(66666)

    def test_carregar_id_existente(self):
        reserva = Reserva(
            self.hospede,
            self.quarto,
            "10/09/2026",
            "15/09/2026"
        )
        reserva.id = 10004

        self.dao.salvar(reserva)

        resultado = self.dao.carregar(10004)

        self.assertEqual(resultado.id, 10004)

    # ---------------- ITENS DA RESERVA ----------------

    def test_reserva_com_item_extra(self):
        produto = Produto(
            "Água",
            5.0,
            "Bebidas"
        )
        produto.id = 7000
        self.produtoDAO.salvar(produto)

        reserva = Reserva(
            self.hospede,
            self.quarto,
            "10/10/2026",
            "12/10/2026"
        )
        reserva.id = 10006

        self.dao.salvar(reserva)

        reserva.adicionar_item(
            produto,
            3
        )

        self.dao.atualizar(reserva)

        carregada = self.dao.carregar(10006)

        self.assertEqual(len(carregada.itens), 1)
        self.assertEqual(carregada.itens[0].produto.nome, "Água")
        self.assertEqual(carregada.itens[0].quantidade, 3)


if __name__ == "__main__":
    unittest.main()
