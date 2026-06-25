from modelo.reserva import Reserva
from datetime import datetime

from persistencia.dao_factory import DAOFactory
from persistencia.id_manager import IDManager
from persistencia.persistence_exception import PersistenceException


class Menu_Reserva:

    def __init__(self):

        self.hospedeDAO = DAOFactory.getHospedeDAO()
        self.quartoDAO = DAOFactory.getQuartoDAO()
        self.produtoDAO = DAOFactory.getProdutoDAO()
        self.reservaDAO = DAOFactory.getReservaDAO()

    # ------------------------------------------------------------
    # busca
    # ------------------------------------------------------------

    def _buscar_hospede(self):

        try:

            tid = int(input("ID do hóspede: "))

            return self.hospedeDAO.carregar(tid)

        except ValueError:

            print("ID inválido.")
            return None

        except PersistenceException:

            print("Hóspede não encontrado.")
            return None

    def _buscar_quarto_disponivel(self):

        try:

            quartos = self.quartoDAO.carregarDisponiveis()

        except PersistenceException:

            print("Não há quartos disponíveis.")
            return None

        print("\nQuartos disponíveis:")

        for q in quartos:

            print(
                f"ID {q.id} | Nº {q.numero} | "
                f"{q.tipo} | R$ {q.diaria:.2f}"
            )

        try:

            tid = int(
                input("ID do quarto desejado: ")
            )

            quarto = self.quartoDAO.carregar(tid)

            if not quarto.disponivel:

                print("Quarto indisponível.")
                return None

            return quarto

        except:

            print("Quarto inválido.")
            return None

    def _buscar_reserva_por_id(self):

        try:

            tid = int(
                input("ID da reserva: ")
            )

            return self.reservaDAO.carregar(tid)

        except ValueError:

            print("ID inválido.")
            return None

        except PersistenceException:

            print("Reserva não encontrada.")
            return None

    def _ler_data(self, campo):

        while True:

            data = input(
                f"{campo} (DD/MM/AAAA): "
            )

            try:

                datetime.strptime(
                    data,
                    "%d/%m/%Y"
                )

                return data

            except ValueError:

                print("Data inválida.")

    # ------------------------------------------------------------
    # produtos extras
    # ------------------------------------------------------------

    def _selecionar_produto(self):

        try:

            produtos = self.produtoDAO.carregarTodos()

        except PersistenceException:

            print("Nenhum produto cadastrado.")
            return None

        print("\nProdutos disponíveis:")

        for p in produtos:

            print(
                f"ID {p.id} | {p.nome} "
                f"| R$ {p.preco:.2f}"
            )

        try:

            tid = int(
                input("ID do produto: ")
            )

            return self.produtoDAO.carregar(tid)

        except:

            print("Produto inválido.")
            return None

    def _adicionar_item(self, reserva):

        produto = self._selecionar_produto()

        if produto is None:
            return

        try:

            quantidade = int(
                input(
                    f"Quantidade de '{produto.nome}': "
                )
            )

            if quantidade < 1:
                raise ValueError

        except ValueError:

            print("Quantidade inválida.")
            return

        item = reserva.adicionar_item(
            produto,
            quantidade
        )

        print(
            f"Adicionado: "
            f"{item.produto.nome} x{item.quantidade}"
        )

    def _remover_item(self, reserva):

        if not reserva.itens:

            print("Sem itens extras.")
            return

        print("\nItens:")

        for i, item in enumerate(
            reserva.itens,
            1
        ):

            print(
                f"{i} - {item}"
            )

        try:

            idx = int(
                input(
                    "Número do item: "
                )
            ) - 1

            if 0 <= idx < len(reserva.itens):

                item = reserva.itens[idx]

                reserva.remover_item(
                    item
                )

                print("Item removido.")

            else:

                print("Número inválido.")

        except ValueError:

            print("Entrada inválida.")

    # ------------------------------------------------------------
    # ações
    # ------------------------------------------------------------

    def _criar_reserva(self):

        print("\n--- NOVA RESERVA ---")

        hospede = self._buscar_hospede()

        if hospede is None:
            return

        quarto = self._buscar_quarto_disponivel()

        if quarto is None:
            return

        checkin = self._ler_data(
            "Check-in"
        )

        checkout = self._ler_data(
            "Check-out"
        )

        try:

            reserva = Reserva(
                hospede,
                quarto,
                checkin,
                checkout
            )

        except ValueError as e:

            print(f"Erro: {e}")
            return

        reserva.id = IDManager.proximo_id_reserva()

        self.reservaDAO.salvar(
            reserva
        )

        print(
            f"\nReserva criada. ID {reserva.id}"
        )

        while True:

            add = input(
                "Adicionar item extra? (s/n): "
            ).lower()

            if add != "s":
                break

            self._adicionar_item(
                reserva
            )

        self.reservaDAO.atualizar(
            reserva
        )

    def _editar_reserva(self):

        reserva = self._buscar_reserva_por_id()

        if reserva is None:
            return

        while True:

            print(
                f"\nEditando reserva {reserva.id}"
            )

            print("1 - Check-in")
            print("2 - Check-out")
            print("3 - Adicionar item")
            print("4 - Remover item")
            print("5 - Concluir")

            try:

                op = int(
                    input("Escolha: ")
                )

            except ValueError:

                print("Opção inválida.")
                continue

            if op == 1:

                nova = self._ler_data(
                    "Novo check-in"
                )

                try:

                    Reserva.validar_datas(
                        nova,
                        reserva.checkout
                    )

                    reserva.checkin = nova

                except ValueError as e:

                    print(e)

            elif op == 2:

                nova = self._ler_data(
                    "Novo check-out"
                )

                try:

                    Reserva.validar_datas(
                        reserva.checkin,
                        nova
                    )

                    reserva.checkout = nova

                except ValueError as e:

                    print(e)

            elif op == 3:

                self._adicionar_item(
                    reserva
                )

            elif op == 4:

                self._remover_item(
                    reserva
                )

            elif op == 5:

                self.reservaDAO.atualizar(
                    reserva
                )

                print(
                    "Reserva atualizada."
                )

                break

            else:

                print("Opção inválida.")

    def _cancelar_reserva(self):

        reserva = self._buscar_reserva_por_id()

        if reserva is None:
            return

        confirma = input(
            "Cancelar reserva? (s/n): "
        ).lower()

        if confirma == "s":

            self.reservaDAO.apagar(
                reserva.id
            )

            print(
                "Reserva cancelada."
            )

    def _visualizar_reserva(self):

        reserva = self._buscar_reserva_por_id()

        if reserva:

            print("\n" + str(reserva))

    def _listar_todas(self):

        try:

            reservas = self.reservaDAO.carregarTodos()

        except PersistenceException:

            print("Nenhuma reserva cadastrada.")
            return

        for r in reservas:

            print()

            print(
                f"ID {r.id} | "
                f"{r.hospede.nome} | "
                f"Quarto {r.quarto.numero} | "
                f"Total R$ {r.total_geral():.2f}"
            )

            print("=" * 50)

    # ------------------------------------------------------------
    # menu
    # ------------------------------------------------------------

    def menu(self):

        while True:

            print("\n MENU DE RESERVAS")

            print("1 - Nova reserva")
            print("2 - Editar reserva")
            print("3 - Cancelar reserva")
            print("4 - Visualizar reserva por ID")
            print("5 - Listar reservas")
            print("6 - Voltar")

            try:

                op = int(
                    input("\nEscolha: ")
                )

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
                self._listar_todas()

            elif op == 6:
                break

            else:
                print("Opção inválida.")