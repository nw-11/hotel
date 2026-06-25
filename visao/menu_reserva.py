from modelo.banco_de_dados import Bancodedados
from modelo.reserva import Reserva
from datetime import datetime


class Menu_Reserva:
    def __init__(self):
        pass

    # ------------------------------------------------------------------
    # Métodos internos — busca
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
            print(f"  ID {q.id:>3} | Nº {q.numero} | "
                  f"{q.tipo:<10} | R$ {q.diaria:.2f}/diária")
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

    def _ler_data(self, campo):
        while True:
            data = input(f"{campo} (DD/MM/AAAA): ")
            try:
                datetime.strptime(data, "%d/%m/%Y")
                return data
            except ValueError:
                print("Data inválida. Use o formato DD/MM/AAAA.")

    # ------------------------------------------------------------------
    # Gerenciamento de itens extras
    # ------------------------------------------------------------------

    def _selecionar_produto(self):
        """
        Exibe os produtos disponíveis e retorna o escolhido pelo usuário.
        Retorna None se não houver produtos ou se a escolha for inválida.
        """
        produtos = Bancodedados.lista_produtos()
        if not produtos:
            print(
                "Nenhum produto cadastrado. "
                "Cadastre produtos no menu Produtos antes de adicioná-los."
            )
            return None

        print("\nProdutos disponíveis:")
        # Agrupa por categoria para facilitar a leitura
        categorias = {}
        for p in produtos:
            categorias.setdefault(p.categoria, []).append(p)

        for cat, lista in categorias.items():
            print(f"  [{cat}]")
            for p in lista:
                print(f"    ID {p.id:>3} | {p.nome:<28} | R$ {p.preco:.2f}")

        try:
            tid = int(input("ID do produto: "))
            produto = Bancodedados.busca_produto(tid)
            if produto is None:
                print("Produto não encontrado.")
            return produto
        except ValueError:
            print("ID inválido.")
            return None

    def _adicionar_item(self, reserva):
        produto = self._selecionar_produto()
        if produto is None:
            return
        try:
            quantidade = int(input(f"Quantidade de '{produto.nome}': "))
            if quantidade < 1:
                raise ValueError
        except ValueError:
            print("Quantidade inválida (mínimo: 1).")
            return
        item = reserva.adicionar_item(produto, quantidade)
        print(
            f"Adicionado: {item.produto.nome} "
            f"x{item.quantidade} = R$ {item.subtotal:.2f}"
        )

    def _remover_item(self, reserva):
        if not reserva.itens:
            print("Esta reserva não possui itens extras.")
            return
        print("\nItens desta reserva:")
        for i, item in enumerate(reserva.itens, 1):
            print(f"  {i}. {item}")
        try:
            idx = int(input("Número do item a remover: ")) - 1
            if 0 <= idx < len(reserva.itens):
                item = reserva.itens[idx]
                if reserva.remover_item(item):
                    print(f"Item '{item.produto.nome}' removido.")
                else:
                    print("Erro ao remover item.")
            else:
                print("Número inválido.")
        except ValueError:
            print("Entrada inválida.")

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

        try:
            reserva = Reserva(hospede, quarto, checkin, checkout)
        except ValueError as e:
            print(f"Erro nas datas: {e}")
            return

        reserva.salvar()
        print(f"\nReserva criada com sucesso! ID: {reserva.id}")

        # Oferecer adição de itens extras logo após a criação
        while True:
            add = input("\nDeseja adicionar um item extra? (s/n): ").lower()
            if add != "s":
                break
            self._adicionar_item(reserva)

    def _editar_reserva(self):
        reserva = self._buscar_reserva_por_id()
        if reserva is None:
            return
        while True:
            print(f"\nEditando reserva {reserva.id} — {reserva.hospede.nome}")
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
                nova = self._ler_data("Novo check-in")
                try:
                    Reserva.validar_datas(nova, reserva.checkout)
                    reserva.checkin = nova
                except ValueError as e:
                    print(f"Data inválida: {e}")
            elif op == 2:
                nova = self._ler_data("Novo check-out")
                try:
                    Reserva.validar_datas(reserva.checkin, nova)
                    reserva.checkout = nova
                except ValueError as e:
                    print(f"Data inválida: {e}")
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
        print(
            f"\nReserva {reserva.id} — {reserva.hospede.nome} "
            f"| Quarto {reserva.quarto.numero}"
        )
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
            # Resumo compacto na listagem
            print(f"ID {r.id} | {r.hospede.nome} | "
                  f"Qto {r.quarto.numero} | "
                  f"{r.checkin} → {r.checkout} | "
                  f"Total: R$ {r.total_geral():.2f}")
            print("=" * 60)

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
