from modelo.produto import Produto

from persistencia.dao_factory import DAOFactory
from persistencia.id_manager import IDManager
from persistencia.persistence_exception import PersistenceException


class Menu_Produto:

    def __init__(self):

        self.dao = DAOFactory.getProdutoDAO()

    # ------------------------------------------------------------
    # métodos internos
    # ------------------------------------------------------------

    def _criar_produto(self):

        nome = input(
            "Nome do produto/serviço: "
        ).strip()

        try:

            preco = float(
                input(
                    "Preço unitário (R$): "
                )
            )

        except ValueError:

            print("Preço inválido.")
            return None

        print("\nCategorias disponíveis:")

        for i, cat in enumerate(
            Produto.CATEGORIAS,
            1
        ):

            print(
                f"  {i} - {cat}"
            )

        try:

            idx = int(

                input(
                    "Categoria (número): "
                )

            ) - 1

            if not (
                0 <= idx < len(
                    Produto.CATEGORIAS
                )
            ):

                raise ValueError

            categoria = Produto.CATEGORIAS[
                idx
            ]

        except ValueError:

            print(
                "Categoria inválida. Usando 'Outros'."
            )

            categoria = "Outros"

        return Produto(
            nome,
            preco,
            categoria
        )

    def _buscar_por_id(self):

        try:

            tid = int(
                input(
                    "ID do produto: "
                )
            )

            return self.dao.carregar(
                tid
            )

        except ValueError:

            print(
                "ID inválido."
            )

            return None

        except PersistenceException:

            print(
                "Produto não encontrado."
            )

            return None

    def _listar_todos(self):

        try:

            produtos = self.dao.carregarTodos()

            categorias = {}

            for p in produtos:

                categorias.setdefault(
                    p.categoria,
                    []
                ).append(p)

            for cat, lista in categorias.items():

                print(
                    f"\n  [{cat}]"
                )

                for p in lista:

                    print(

                        f"    ID {p.id:>3}"

                        f" | {p.nome:<30}"

                        f" | R$ {p.preco:>8.2f}"
                    )

        except PersistenceException:

            print(
                "Nenhum produto cadastrado."
            )

    # ------------------------------------------------------------
    # ações
    # ------------------------------------------------------------

    def _adicionar(self):

        p = self._criar_produto()

        if p is None:
            return

        p.id = IDManager.proximo_id_produto()

        self.dao.salvar(
            p
        )

        print(

            f"\nProduto '{p.nome}' "

            f"cadastrado com ID {p.id}."
        )

    def _editar(self):

        p = self._buscar_por_id()

        if p is None:
            return

        while True:

            print(
                f"\nEditando: {p.nome}"
            )

            print("1 - Nome")
            print("2 - Preço")
            print("3 - Categoria")
            print("4 - Concluir")

            try:

                op = int(
                    input(
                        "Escolha: "
                    )
                )

            except ValueError:

                print(
                    "Opção inválida."
                )

                continue

            if op == 1:

                p.nome = input(
                    "Novo nome: "
                ).strip()

            elif op == 2:

                try:

                    p.preco = float(
                        input(
                            "Novo preço (R$): "
                        )
                    )

                except ValueError:

                    print(
                        "Preço inválido."
                    )

            elif op == 3:

                print(
                    "\nCategorias disponíveis:"
                )

                for i, cat in enumerate(
                    Produto.CATEGORIAS,
                    1
                ):

                    print(
                        f"  {i} - {cat}"
                    )

                try:

                    idx = int(
                        input(
                            "Categoria (número): "
                        )
                    ) - 1

                    if 0 <= idx < len(
                        Produto.CATEGORIAS
                    ):

                        p.categoria = (
                            Produto.CATEGORIAS[idx]
                        )

                    else:

                        print(
                            "Opção inválida."
                        )

                except ValueError:

                    print(
                        "Opção inválida."
                    )

            elif op == 4:

                self.dao.atualizar(
                    p
                )

                print(
                    "Produto atualizado com sucesso."
                )

                break

            else:

                print(
                    "Opção inválida."
                )

    def _remover(self):

        p = self._buscar_por_id()

        if p is None:
            return

        confirma = input(

            f"Confirma remoção "

            f"de '{p.nome}'? (s/n): "

        ).lower()

        if confirma == "s":

            try:

                self.dao.apagar(
                    p.id
                )

                print(
                    "Produto removido com sucesso."
                )

            except PersistenceException:

                print(

                    "Não foi possível remover: "

                    "produto está associado "

                    "a uma ou mais reservas."
                )

    # ------------------------------------------------------------
    # menu principal
    # ------------------------------------------------------------

    def menu(self):

        while True:

            print("\n MENU DE PRODUTOS")

            print("1 - Cadastrar produto")
            print("2 - Editar produto")
            print("3 - Remover produto")
            print("4 - Visualizar por ID")
            print("5 - Listar todos os produtos")
            print("6 - Voltar")

            try:

                op = int(
                    input(
                        "\nEscolha: "
                    )
                )

            except ValueError:

                print(
                    "Opção inválida."
                )

                continue

            if op == 1:

                self._adicionar()

            elif op == 2:

                self._editar()

            elif op == 3:

                self._remover()

            elif op == 4:

                p = self._buscar_por_id()

                if p:

                    print(
                        "\n" + str(p)
                    )

            elif op == 5:

                print(
                    "\nLISTA DE PRODUTOS:\n"
                )

                self._listar_todos()

            elif op == 6:

                break

            else:

                print(
                    "Opção inválida."
                )