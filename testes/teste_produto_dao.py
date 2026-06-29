import unittest

from modelo.produto import Produto

from persistencia.dao_factory import DAOFactory
from persistencia.persistence_exception import PersistenceException


class TesteProdutoDAO(unittest.TestCase):

    def setUp(self):
        self.hospedeDAO = DAOFactory.getHospedeDAO()
        self.quartoDAO = DAOFactory.getQuartoDAO()
        self.produtoDAO = DAOFactory.getProdutoDAO()
        self.reservaDAO = DAOFactory.getReservaDAO()

        self.hospedeDAO.entidades.clear()
        self.quartoDAO.entidades.clear()
        self.produtoDAO.entidades.clear()
        self.reservaDAO.entidades.clear()

        self.dao = self.produtoDAO

    # ---------------- SALVAR ----------------

    def test_salvar_id_novo(self):
        p = Produto("Água", 5.0, "Bebidas")
        p.id = 7000

        self.dao.salvar(p)

        resultado = self.dao.carregar(7000)

        self.assertEqual(resultado.nome, "Água")

    def test_salvar_id_existente(self):
        p = Produto("Café", 7.0, "Bebidas")
        p.id = 7001

        self.dao.salvar(p)

        with self.assertRaises(PersistenceException):
            self.dao.salvar(p)

    # ---------------- ATUALIZAR ----------------

    def test_atualizar_id_inexistente(self):
        p = Produto("Teste", 1.0, "Outros")
        p.id = 9999

        with self.assertRaises(PersistenceException):
            self.dao.atualizar(p)

    def test_atualizar_id_existente(self):
        p = Produto("Suco", 8.0, "Bebidas")
        p.id = 7002

        self.dao.salvar(p)

        p.preco = 10.0

        self.dao.atualizar(p)

        novo = self.dao.carregar(7002)

        self.assertEqual(novo.preco, 10.0)

    # ---------------- APAGAR ----------------

    def test_apagar_id_inexistente(self):
        with self.assertRaises(PersistenceException):
            self.dao.apagar(8888)

    def test_apagar_id_existente(self):
        p = Produto("Biscoito", 4.0, "Alimentação")
        p.id = 7003

        self.dao.salvar(p)

        removido = self.dao.apagar(7003)

        self.assertEqual(removido.id, 7003)

        with self.assertRaises(PersistenceException):
            self.dao.carregar(7003)

    # ---------------- CARREGAR ----------------

    def test_carregar_id_inexistente(self):
        with self.assertRaises(PersistenceException):
            self.dao.carregar(6666)

    def test_carregar_id_existente(self):
        p = Produto("Refrigerante", 9.0, "Bebidas")
        p.id = 7004

        self.dao.salvar(p)

        resultado = self.dao.carregar(7004)

        self.assertEqual(resultado.nome, "Refrigerante")

    # ---------------- FILTRAR POR CATEGORIA ----------------

    def test_carregar_produtos_por_categoria(self):
        p1 = Produto("Água", 5.0, "Bebidas")
        p1.id = 1

        p2 = Produto("Sabonete", 3.0, "Comodidades")
        p2.id = 2

        p3 = Produto("Suco", 8.0, "Bebidas")
        p3.id = 3

        self.produtoDAO.salvar(p1)
        self.produtoDAO.salvar(p2)
        self.produtoDAO.salvar(p3)

        bebidas = DAOFactory.carregarProdutosPorCategoria("Bebidas")

        self.assertEqual(
            [p.nome for p in bebidas],
            ["Água", "Suco"]
        )


if __name__ == "__main__":
    unittest.main()
