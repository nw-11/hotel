from ..modelo.banco_de_dados import Bancodedados
from ..modelo.reserva import Reserva


class Menu_Reserva:
    def __init__(self):
        pass

    # ------------------------------------------------------------------
    # Métodos internos
    # ------------------------------------------------------------------

    def _buscar_hospede(self):
        try:
            tid = int(input("ID do hóspede: "))
            h = Bancodedados.busca_hospede(tid)
            if h is None:
                print("Hóspede não encontrado.")
            return h
        except ValueError:
            print("ID inválido.")
            return None

    def _buscar_quarto_disponivel(self):
        quartos = Bancodedados.lista_quartos_disponiveis()
        if not quartos:
            print("Não há quartos disponíveis no momento.")
            return None
        print("\nQuartos disponíveis:")
        for q in quartos:
            print(f"  ID {q.id} | Nº {q.numero} | {q.tipo} | R$ {q.diaria:.2f}/diária")
        try:
            tid = int(input("ID do quarto desejado: "))
            quarto = Bancodedados.busca_quarto(tid)
            if quarto is None or not quarto.disponivel:
                print("Quarto inválido ou indisponível.")
                return None
            return quarto
        except ValueError:
            print("ID inválido.")
            return None

    def _buscar_reserva_por_id(self):
        try:
            tid = int(input("ID da reserva: "))
            r = Bancodedados.busca_reserva(tid)
            if r is None:
                print("Reserva não encontrada.")
            return r
        except ValueError:
            print("ID inválido.")
            return None

    def _ler_data(self, label):
        while True:
            data = input(f"{label} (DD/MM/AAAA): ")
            partes = data.split("/")
            if len(partes) == 3 and all(p.isdigit() for p in partes):
                return data
            print("Formato inválido. Use DD/MM/AAAA.")

    # ------------------------------------------------------------------
    # Ações
    # ------------------------------------------------------------------

    def _criar_reserva(self):
        print("\n--- NOVA RESERVA ---")
        hospede = self._buscar_hospede()
        if hospede is None:
            return

        quarto = self._buscar_quarto_disponivel()
        if quarto is None:
            return

        checkin  = self._ler_data("Check-in")
        checkout = self._ler_data("Check-out")

        reserva = Reserva(hospede, quarto, checkin, checkout)
        reserva.salvar()
        print(f"\nReserva criada com sucesso! ID: {reserva.id}")

        # oferecer adição de itens extras logo após criação
        while True:
            add = input("Deseja adicionar um item extra? (s/n): ").lower()
            if add != "s":
                break
            self._adicionar_item(reserva)

    def _adicionar_item(self, reserva):
        nome  = input("Nome do item: ")
        try:
            preco = float(input("Preço (R$): "))
        except ValueError:
            print("Preço inválido.")
            return
        item = reserva.adicionar_item(nome, preco)
        print(f"Item '{item.nome}' adicionado (R$ {item.preco:.2f}).")

    def _remover_item(self, reserva):
        if not reserva.itens:
            print("Esta reserva não possui itens extras.")
            return
        print("\nItens desta reserva:")
        for i, item in enumerate(reserva.itens, 1):
            print(f"  {i}. {item} (ID {item.id})")
        try:
            idx = int(input("Número do item a remover: ")) - 1
            if 0 <= idx < len(reserva.itens):
                item = reserva.itens[idx]
                if reserva.remover_item(item):
                    print("Item removido.")
                else:
                    print("Erro ao remover item.")
            else:
                print("Número inválido.")
        except ValueError:
            print("Entrada inválida.")

    def _editar_reserva(self):
        reserva = self._buscar_reserva_por_id()
        if reserva is None:
            return
        while True:
            print("\nO que deseja alterar?")
            print("1 - Check-in")
            print("2 - Check-out")
            print("3 - Adicionar item extra")
            print("4 - Remover item extra")
            print("5 - Concluir")
            try:
                op = int(input("Escolha: "))
            except ValueError:
                print("Opção inválida.")
                continue

            if op == 1:
                reserva.checkin = self._ler_data("Novo check-in")
            elif op == 2:
                reserva.checkout = self._ler_data("Novo check-out")
            elif op == 3:
                self._adicionar_item(reserva)
            elif op == 4:
                self._remover_item(reserva)
            elif op == 5:
                reserva.atualizar()
                print("Reserva atualizada com sucesso.")
                break
            else:
                print("Opção inválida.")

    def _cancelar_reserva(self):
        reserva = self._buscar_reserva_por_id()
        if reserva is None:
            return
        print(f"\nReserva de {reserva.hospede.nome} — Quarto {reserva.quarto.numero}")
        confirma = input("Confirmar cancelamento? (s/n): ").lower()
        if confirma == "s":
            if reserva.apagar():
                print("Reserva cancelada. Quarto liberado.")
            else:
                print("Erro ao cancelar reserva.")

    def _visualizar_reserva(self):
        reserva = self._buscar_reserva_por_id()
        if reserva:
            print("\n" + str(reserva))

    def _listar_todas(self):
        reservas = Bancodedados.lista_reservas()
        if not reservas:
            print("Nenhuma reserva cadastrada.")
            return
        for r in reservas:
            print()
            print(r)
            print("=" * 40)

    # ------------------------------------------------------------------
    # Menu principal
    # ------------------------------------------------------------------

    def menu(self):
        while True:
            print("\n MENU DE RESERVAS")
            print("1 - Nova reserva")
            print("2 - Editar reserva")
            print("3 - Cancelar reserva")
            print("4 - Visualizar reserva por ID")
            print("5 - Listar todas as reservas")
            print("6 - Voltar")

            try:
                op = int(input("\nEscolha: "))
            except ValueError:
                print("Opção inválida.")
                continue

            if op == 1:
                self._criar_reserva()
            elif op == 2:
                self._editar_reserva()
            elif op == 3:
                self._cancelar_reserva()
            elif op == 4:
                self._visualizar_reserva()
            elif op == 5:
                print("\nLISTA DE RESERVAS:\n")
                self._listar_todas()
            elif op == 6:
                break
            else:
                print("Opção inválida.")