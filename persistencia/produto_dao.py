from modelo.produto import Produto
from persistencia.entidade_dao import EntidadeDAO
from persistencia.arquivo_utils import (
    ARQ_PRODUTOS,
    ler_linhas,
    escrever_linhas
)
from persistencia.persistence_exception import PersistenceException


class ProdutoDAO(EntidadeDAO[Produto]):
    def persistir(self):
        linhas = []

        for p in self._ordenadas_por_id():
            linhas.append([
                p.id,
                p.nome,
                p.preco,
                p.categoria
            ])

        escrever_linhas(
            ARQ_PRODUTOS,
            linhas
        )

    def recuperar(self):
        self.entidades.clear()

        for linha in ler_linhas(ARQ_PRODUTOS):
            produto = Produto(
                linha[1],
                float(linha[2]),
                linha[3],
                id=int(linha[0])
            )

            self.entidades.add(produto)

    def carregarPorCategoria(self, categoria):
        produtos = [
            p for p in self._ordenadas_por_id()
            if p.categoria.lower() == categoria.lower()
        ]

        if len(produtos) == 0:
            raise PersistenceException(
                "carregarTodos",
                "nenhum produto encontrado nessa categoria",
                categoria
            )

        return produtos
