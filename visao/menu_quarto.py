from ..modelo.banco_de_dados import Bancodedados
from ..modelo.quarto import Quarto


class Menu_Quarto:
    def __init__(self):
        pass

    # ------------------------------------------------------------------
    # Métodos internos
    # ------------------------------------------------------------------

    def _criar_quarto(self):
        numero = input("Número do quarto: ")
        print("Tipos disponíveis: Standard, Luxo, Suite")
        tipo = input("Tipo: ")
        diaria = float(input("Valor da diária (R$): "))
        return Quarto(numero, tipo, diaria)

    def _buscar_por_id(self):
        try:
            tid = int(input("ID do quarto: "))
            quarto = Bancodedados.busca_quarto(tid)
            if quarto is None:
                print("Quarto não encontrado.")
            return quarto
        except ValueError:
            print("ID inválido.")
            return None

    def _listar_todos(self):
        quartos = Bancodedados.lista_quartos()
        if not quartos:
            print("Nenhum quarto cadastrado.")
            return
        for q in quartos:
            print()
            print(q)
            print("-" * 30)

    # ------------------------------------------------------------------
    # Ações
    # ------------------------------------------------------------------

    def _adicionar(self):
        quarto = self._criar_quarto()
        quarto.salvar()
        print(f"\nQuarto {quarto.numero} cadastrado com ID {quarto.id}.")

    def _editar(self):
        quarto = self._buscar_por_id()
        if quarto is None:
            return
        while True:
            print("\nO que deseja alterar?")
            print("1 - Número")
            print("2 - Tipo")
            print("3 - Diária")
            print("4 - Disponibilidade")
            print("5 - Concluir")
            try:
                op = int(input("Escolha: "))
            except ValueError:
                print("Opção inválida.")
                continue

            if op == 1:
                quarto.numero = input("Novo número: ")
            elif op == 2:
                quarto.tipo = input("Novo tipo: ")
            elif op == 3:
                quarto.diaria = float(input("Nova diária (R$): "))
            elif op == 4:
                quarto.disponivel = not quarto.disponivel
                status = "Disponível" if quarto.disponivel else "Ocupado"
                print(f"Status alterado para: {status}")
            elif op == 5:
                quarto.atualizar()
                print("Quarto atualizado com sucesso.")
                break
            else:
                print("Opção inválida.")

    def _remover(self):
        quarto = self._buscar_por_id()
        if quarto is None:
            return
        confirma = input(f"Confirma remoção do quarto {quarto.numero}? (s/n): ").lower()
        if confirma == "s":
            if quarto.apagar():
                print("Quarto removido com sucesso.")
            else:
                print("Erro ao remover quarto.")

    def _listar_disponiveis(self):
        quartos = Bancodedados.lista_quartos_disponiveis()
        if not quartos:
            print("Nenhum quarto disponível no momento.")
            return
        print(f"\n{len(quartos)} quarto(s) disponível(is):\n")
        for q in quartos:
            print(q)
            print("-" * 30)

    # ------------------------------------------------------------------
    # Menu principal
    # ------------------------------------------------------------------

    def menu(self):
        while True:
            print("\n MENU DE QUARTOS")
            print("1 - Cadastrar quarto")
            print("2 - Editar quarto")
            print("3 - Remover quarto")
            print("4 - Visualizar por ID")
            print("5 - Listar todos os quartos")
            print("6 - Listar quartos disponíveis")
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
                q = self._buscar_por_id()
                if q:
                    print("\n" + str(q))
            elif op == 5:
                print("\nLISTA DE QUARTOS:\n")
                self._listar_todos()
            elif op == 6:
                self._listar_disponiveis()
            elif op == 7:
                break
            else:
                print("Opção inválida.")