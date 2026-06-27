import unittest

from modelo.hospede import Hospede
from persistencia.dao_factory import DAOFactory
from persistencia.persistence_exception import PersistenceException


class TesteHospedeDAO(unittest.TestCase):

    def setUp(self):
        self.dao = DAOFactory.getHospedeDAO()
        self.dao.entidades.clear()

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

    def test_apagar_id_existente(self):
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


if __name__ == "__main__":
    unittest.main()
