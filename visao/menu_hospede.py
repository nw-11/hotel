from modelo.hospede import Hospede

from persistencia.dao_factory import DAOFactory
from persistencia.id_manager import IDManager
from persistencia.persistence_exception import PersistenceException


class Menu_Hospede:

    def __init__(self):

        self.dao = DAOFactory.getHospedeDAO()

    # ------------------------------------------------------------
    # métodos internos
    # ------------------------------------------------------------

    def _criar_hospede(self):

        nome = input(
            "Nome: "
        )

        cpf = input(
            "CPF: "
        )

        email = input(
            "E-mail: "
        )

        telefone = input(
            "Telefone: "
        )

        return Hospede(
            nome,
            cpf,
            email,
            telefone
        )

    def _buscar_por_id(self):

        try:

            tid = int(
                input(
                    "ID do hóspede: "
                )
            )

            return self.dao.carregar(
                tid
            )

        except ValueError:

            print("ID inválido.")
            return None

        except PersistenceException:

            print(
                "Hóspede não encontrado."
            )

            return None

    # ------------------------------------------------------------
    # ações
    # ------------------------------------------------------------

    def _adicionar(self):

        h = self._criar_hospede()

        h.id = IDManager.proximo_id_hospede()

        self.dao.salvar(
            h
        )

        print(

            f"\nHóspede '{h.nome}' "

            f"cadastrado com ID {h.id}."
        )

    def _editar(self):

        h = self._buscar_por_id()

        if h is None:
            return

        while True:

            print(
                "\nO que deseja alterar?"
            )

            print("1 - Nome")
            print("2 - CPF")
            print("3 - E-mail")
            print("4 - Telefone")
            print("5 - Concluir")

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

                h.nome = input(
                    "Novo nome: "
                )

            elif op == 2:

                h.cpf = input(
                    "Novo CPF: "
                )

            elif op == 3:

                h.email = input(
                    "Novo e-mail: "
                )

            elif op == 4:

                h.telefone = input(
                    "Novo telefone: "
                )

            elif op == 5:

                self.dao.atualizar(
                    h
                )

                print(
                    "Hóspede atualizado com sucesso."
                )

                break

            else:

                print(
                    "Opção inválida."
                )

    def _remover(self):

        h = self._buscar_por_id()

        if h is None:
            return

        confirma = input(

            f"Confirma remoção "

            f"de '{h.nome}'? (s/n): "

        ).lower()

        if confirma == "s":

            try:

                self.dao.apagar(
                    h.id
                )

                print(
                    "Hóspede removido com sucesso."
                )

            except PersistenceException:

                print(
                    "Erro ao remover hóspede."
                )

    def _listar_todos(self):

        try:

            hospedes = self.dao.carregarTodos()

        except PersistenceException:

            print(
                "Nenhum hóspede cadastrado."
            )

            return

        for h in hospedes:

            print()
            print(h)
            print("-" * 30)

    def _buscar_por_nome(self):

        nome = input(
            "Nome (ou parte do nome): "
        ).lower()

        try:

            hospedes = self.dao.carregarTodos()

        except PersistenceException:

            print(
                "Nenhum hóspede cadastrado."
            )

            return

        encontrados = [

            h for h in hospedes

            if nome in h.nome.lower()
        ]

        if not encontrados:

            print(
                "Nenhum hóspede encontrado."
            )

            return

        for h in encontrados:

            print()
            print(h)
            print("-" * 30)

    # ------------------------------------------------------------
    # menu principal
    # ------------------------------------------------------------

    def menu(self):

        while True:

            print("\n MENU DE HÓSPEDES")

            print("1 - Cadastrar hóspede")
            print("2 - Editar hóspede")
            print("3 - Remover hóspede")
            print("4 - Visualizar por ID")
            print("5 - Listar todos os hóspedes")
            print("6 - Buscar por nome")
            print("7 - Voltar")

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

                h = self._buscar_por_id()

                if h:

                    print(
                        "\n" + str(h)
                    )

            elif op == 5:

                print(
                    "\nLISTA DE HÓSPEDES:\n"
                )

                self._listar_todos()

            elif op == 6:

                self._buscar_por_nome()

            elif op == 7:

                break

            else:

                print(
                    "Opção inválida."
                )