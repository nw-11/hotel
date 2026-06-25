from modelo.banco_de_dados import Bancodedados
from modelo.produto import Produto


class Menu_Produto:
    def __init__(self):
        pass

    # ------------------------------------------------------------------
    # Métodos internos
    # ------------------------------------------------------------------

    def _criar_produto(self):
        nome = input("Nome do produto/serviço: ").strip()
        try:
            preco = float(input("Preço unitário (R$): "))
        except ValueError:
            print("Preço inválido.")
            return None

        print("\nCategorias disponíveis:")
        for i, cat in enumerate(Produto.CATEGORIAS, 1):
            print(f"  {i} - {cat}")
        try:
            idx = int(input("Categoria (número): ")) - 1
            if not (0 <= idx < len(Produto.CATEGORIAS)):
                raise ValueError
            categoria = Produto.CATEGORIAS[idx]
        except ValueError:
            print("Categoria inválida. Usando 'Outros'.")
            categoria = "Outros"

        return Produto(nome, preco, categoria)

    def _buscar_por_id(self):
        try:
            tid = int(input("ID do produto: "))
            p = Bancodedados.busca_produto(tid)
            if p is None:
                print("Produto não encontrado.")
            return p
        except ValueError:
            print("ID inválido.")
            return None

    def _listar_todos(self):
        produtos = Bancodedados.lista_produtos()
        if not produtos:
            print("Nenhum produto cadastrado.")
            return
        # Agrupa por categoria para melhor visualização
        categorias = {}
        for p in produtos:
            categorias.setdefault(p.categoria, []).append(p)

        for cat, lista in categorias.items():
            print(f"\n  [{cat}]")
            for p in lista:
                print(f"    ID {p.id:>3} | {p.nome:<30} | R$ {p.preco:>8.2f}")

    # ------------------------------------------------------------------
    # Ações
    # ------------------------------------------------------------------

    def _adicionar(self):
        p = self._criar_produto()
        if p is None:
            return
        p.salvar()
        print(f"\nProduto '{p.nome}' cadastrado com ID {p.id}.")

    def _editar(self):
        p = self._buscar_por_id()
        if p is None:
            return
        while True:
            print(f"\nEditando: {p.nome}")
            print("1 - Nome")
            print("2 - Preço")
            print("3 - Categoria")
            print("4 - Concluir")
            try:
                op = int(input("Escolha: "))
            except ValueError:
                print("Opção inválida.")
                continue

            if op == 1:
                p.nome = input("Novo nome: ").strip()
            elif op == 2:
                try:
                    p.preco = float(input("Novo preço (R$): "))
                except ValueError:
                    print("Preço inválido.")
            elif op == 3:
                print("\nCategorias disponíveis:")
                for i, cat in enumerate(Produto.CATEGORIAS, 1):
                    print(f"  {i} - {cat}")
                try:
                    idx = int(input("Categoria (número): ")) - 1
                    if 0 <= idx < len(Produto.CATEGORIAS):
                        p.categoria = Produto.CATEGORIAS[idx]
                    else:
                        print("Opção inválida.")
                except ValueError:
                    print("Opção inválida.")
            elif op == 4:
                p.atualizar()
                print("Produto atualizado com sucesso.")
                break
            else:
                print("Opção inválida.")

    def _remover(self):
        p = self._buscar_por_id()
        if p is None:
            return
        confirma = input(
            f"Confirma remoção de '{p.nome}'? (s/n): "
        ).lower()
        if confirma == "s":
            if p.apagar():
                print("Produto removido com sucesso.")
            else:
                print(
                    "Não foi possível remover: produto está associado "
                    "a uma ou mais reservas ativas."
                )

    # ------------------------------------------------------------------
    # Menu principal
    # ------------------------------------------------------------------

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
                op = int(input("\nEscolha: "))
            except ValueError:
                print("Opção inválida.")
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
                    print("\n" + str(p))
            elif op == 5:
                print("\nLISTA DE PRODUTOS:\n")
                self._listar_todos()
            elif op == 6:
                break
            else:
                print("Opção inválida.")
