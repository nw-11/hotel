from modelo.produto import Produto
from persistencia.persistence_exception import PersistenceException
from persistencia.arquivo_utils import *


class ProdutoDAO:

    def salvar(self, produto):

        linhas = ler_linhas(ARQ_PRODUTOS)

        for linha in linhas:

            if int(linha[0]) == produto.id:

                raise PersistenceException(
                    "salvar",
                    "Produto já existe",
                    produto.id
                )

        linhas.append([
            produto.id,
            produto.nome,
            produto.preco,
            produto.categoria
        ])

        escrever_linhas(
            ARQ_PRODUTOS,
            linhas
        )

    def atualizar(self, produto):

        linhas = ler_linhas(
            ARQ_PRODUTOS
        )

        encontrou = False

        for i, linha in enumerate(linhas):

            if int(linha[0]) == produto.id:

                linhas[i] = [
                    produto.id,
                    produto.nome,
                    produto.preco,
                    produto.categoria
                ]

                encontrou = True

        if not encontrou:

            raise PersistenceException(
                "atualizar",
                "Produto inexistente",
                produto.id
            )

        escrever_linhas(
            ARQ_PRODUTOS,
            linhas
        )

    def apagar(self, id):

        # verifica se produto está em alguma reserva

        itens = ler_linhas(
            ARQ_ITENS
        )

        for item in itens:

            if int(item[1]) == id:

                raise PersistenceException(
                    "apagar",
                    "Produto vinculado a reserva",
                    id
                )

        linhas = ler_linhas(
            ARQ_PRODUTOS
        )

        novas = [
            l for l in linhas
            if int(l[0]) != id
        ]

        if len(linhas) == len(novas):

            raise PersistenceException(
                "apagar",
                "Produto inexistente",
                id
            )

        escrever_linhas(
            ARQ_PRODUTOS,
            novas
        )

    def carregar(self, id):

        linhas = ler_linhas(
            ARQ_PRODUTOS
        )

        for linha in linhas:

            if int(linha[0]) == id:

                return Produto(
                    linha[1],
                    float(linha[2]),
                    linha[3],
                    int(linha[0])
                )

        raise PersistenceException(
            "carregar",
            "Produto não encontrado",
            id
        )

    def carregarTodos(self):

        linhas = ler_linhas(
            ARQ_PRODUTOS
        )

        if len(linhas) == 0:

            raise PersistenceException(
                "carregarTodos",
                "Nenhum produto salvo",
                None
            )

        produtos = []

        for linha in linhas:

            produtos.append(

                Produto(
                    linha[1],
                    float(linha[2]),
                    linha[3],
                    int(linha[0])
                )
            )

        produtos.sort()

        return produtos

    def carregarPorCategoria(
        self,
        categoria
    ):

        produtos = self.carregarTodos()

        return [

            p for p in produtos

            if p.categoria.lower() == categoria.lower()
        ] 