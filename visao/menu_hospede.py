from modelo.banco_de_dados import Bancodedados
from modelo.hospede import Hospede
 

class Menu_Hospede:
    def __init__(self):
        pass

    # ------------------------------------------------------------------
    # Métodos internos
    # ------------------------------------------------------------------

    def _criar_hospede(self):
        nome     = input("Nome: ")
        cpf      = input("CPF: ")
        email    = input("E-mail: ")
        telefone = input("Telefone: ")
        return Hospede(nome, cpf, email, telefone)

    def _buscar_por_id(self):
        try:
            tid = int(input("ID do hóspede: "))
            h = Bancodedados.busca_hospede(tid)
            if h is None:
                print("Hóspede não encontrado.")
            return h
        except ValueError:
            print("ID inválido.")
            return None

    # ------------------------------------------------------------------
    # Ações
    # ------------------------------------------------------------------

    def _adicionar(self):
        h = self._criar_hospede()
        h.salvar()
        print(f"\nHóspede '{h.nome}' cadastrado com ID {h.id}.")

    def _editar(self):
        h = self._buscar_por_id()
        if h is None:
            return
        while True:
            print("\nO que deseja alterar?")
            print("1 - Nome")
            print("2 - CPF")
            print("3 - E-mail")
            print("4 - Telefone")
            print("5 - Concluir")
            try:
                op = int(input("Escolha: "))
            except ValueError:
                print("Opção inválida.")
                continue
            if op == 1:
                h.nome = input("Novo nome: ")
            elif op == 2:
                h.cpf = input("Novo CPF: ")
            elif op == 3:
                h.email = input("Novo e-mail: ")
            elif op == 4:
                h.telefone = input("Novo telefone: ")
            elif op == 5:
                h.atualizar()
                print("Hóspede atualizado com sucesso.")
                break
            else:
                print("Opção inválida.")

    def _remover(self):
        h = self._buscar_por_id()
        if h is None:
            return
        confirma = input(f"Confirma remoção de '{h.nome}'? (s/n): ").lower()
        if confirma == "s":
            if h.apagar():
                print("Hóspede removido com sucesso.")
            else:
                print("Erro ao remover hóspede.")

    def _listar_todos(self):
        hospedes = Bancodedados.lista_hospedes()
        if not hospedes:
            print("Nenhum hóspede cadastrado.")
            return
        for h in hospedes:
            print()
            print(h)
            print("-" * 30)

    def _buscar_por_nome(self):
        nome = input("Nome (ou parte do nome): ")
        hospedes = Bancodedados.busca_hospedes_por_nome(nome)
        if not hospedes:
            print("Nenhum hóspede encontrado.")
            return
        for h in hospedes:
            print()
            print(h)
            print("-" * 30)

    # ------------------------------------------------------------------
    # Menu principal
    # ------------------------------------------------------------------

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
                h = self._buscar_por_id()
                if h:
                    print("\n" + str(h))
            elif op == 5:
                print("\nLISTA DE HÓSPEDES:\n")
                self._listar_todos()
            elif op == 6:
                self._buscar_por_nome()
            elif op == 7:
                break
            else:
                print("Opção inválida.")