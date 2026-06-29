import unittest

from modelo.hospede import Hospede
from modelo.quarto import Quarto
from modelo.reserva import Reserva

from persistencia.dao_factory import DAOFactory
from persistencia.persistence_exception import PersistenceException


class TesteHospedeDAO(unittest.TestCase):

    def setUp(self):
        self.hospedeDAO = DAOFactory.getHospedeDAO()
        self.quartoDAO = DAOFactory.getQuartoDAO()
        self.produtoDAO = DAOFactory.getProdutoDAO()
        self.reservaDAO = DAOFactory.getReservaDAO()

        self.hospedeDAO.entidades.clear()
        self.quartoDAO.entidades.clear()
        self.produtoDAO.entidades.clear()
        self.reservaDAO.entidades.clear()

        self.dao = self.hospedeDAO

    # ---------------- SALVAR ----------------

    def test_salvar_id_novo(self):
        h = Hospede(
            "Pedro",
            "123",
            "pedro@gmail.com",
            "9999"
        )
        h.id = 5000

        self.dao.salvar(h)

        resultado = self.dao.carregar(5000)

        self.assertEqual(resultado.nome, "Pedro")

    def test_salvar_id_existente(self):
        h = Hospede(
            "Ana",
            "321",
            "ana@gmail.com",
            "8888"
        )
        h.id = 5001

        self.dao.salvar(h)

        with self.assertRaises(PersistenceException):
            self.dao.salvar(h)

    # ---------------- ATUALIZAR ----------------

    def test_atualizar_id_inexistente(self):
        h = Hospede(
            "Teste",
            "000",
            "teste@gmail.com",
            "1111"
        )
        h.id = 9999

        with self.assertRaises(PersistenceException):
            self.dao.atualizar(h)

    def test_atualizar_id_existente(self):
        h = Hospede(
            "Carlos",
            "555",
            "c@gmail.com",
            "2222"
        )
        h.id = 5002

        self.dao.salvar(h)

        h.nome = "Carlos Silva"

        self.dao.atualizar(h)

        novo = self.dao.carregar(5002)

        self.assertEqual(novo.nome, "Carlos Silva")

    # ---------------- APAGAR ----------------

    def test_apagar_id_inexistente(self):
        with self.assertRaises(PersistenceException):
            self.dao.apagar(8888)

    def test_apagar_id_existente_sem_reserva_ativa(self):
        h = Hospede(
            "Julia",
            "444",
            "j@gmail.com",
            "3333"
        )
        h.id = 5003

        self.dao.salvar(h)

        removido = self.dao.apagar(5003)

        self.assertEqual(removido.id, 5003)

        with self.assertRaises(PersistenceException):
            self.dao.carregar(5003)

    def test_nao_apagar_hospede_com_reserva_ativa(self):
        h = Hospede(
            "Marcos",
            "777",
            "marcos@gmail.com",
            "7777"
        )
        h.id = 5005
        self.hospedeDAO.salvar(h)

        q = Quarto(
            "201",
            "Suite",
            350.0
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
            self.hospedeDAO.apagar(5005)

        self.assertEqual(
            self.hospedeDAO.carregar(5005).nome,
            "Marcos"
        )

    # ---------------- CARREGAR ----------------

    def test_carregar_id_inexistente(self):
        with self.assertRaises(PersistenceException):
            self.dao.carregar(7777)

    def test_carregar_id_existente(self):
        h = Hospede(
            "Lucas",
            "999",
            "l@gmail.com",
            "4444"
        )
        h.id = 5004

        self.dao.salvar(h)

        resultado = self.dao.carregar(5004)

        self.assertEqual(resultado.nome, "Lucas")

    # ---------------- CARREGAR TODOS ----------------

    def test_carregar_todos_ordenado_por_id(self):
        h2 = Hospede("B", "2", "b@gmail.com", "2")
        h2.id = 2

        h1 = Hospede("A", "1", "a@gmail.com", "1")
        h1.id = 1

        self.dao.salvar(h2)
        self.dao.salvar(h1)

        resultado = self.dao.carregarTodos()

        self.assertEqual(
            [h.id for h in resultado],
            [1, 2]
        )


if __name__ == "__main__":
    unittest.main()
