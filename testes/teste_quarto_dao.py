import unittest

from modelo.quarto import Quarto
from persistencia.dao_factory import DAOFactory
from persistencia.persistence_exception import PersistenceException


class TesteQuartoDAO(unittest.TestCase):

    def setUp(self):
        self.dao = DAOFactory.getQuartoDAO()
        self.dao.entidades.clear()

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

    def test_apagar_id_existente(self):
        q = Quarto("104", "Suite", 500.0)
        q.id = 6003

        self.dao.salvar(q)

        removido = self.dao.apagar(6003)

        self.assertEqual(removido.id, 6003)

        with self.assertRaises(PersistenceException):
            self.dao.carregar(6003)

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


if __name__ == "__main__":
    unittest.main()
