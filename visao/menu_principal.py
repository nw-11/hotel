from visao.menu_hospede import Menu_Hospede
from visao.menu_quarto import Menu_Quarto
from visao.menu_reserva import Menu_Reserva


class Menu_Principal:
    def __init__(self):
        self.mh = Menu_Hospede()
        self.mq = Menu_Quarto()
        self.mr = Menu_Reserva()

    def menu(self):
        print("\nAdministrador Hoteleiro - v1.0\n")
        while True:
            print("MENU PRINCIPAL")
            print("\n1 - Hóspedes")
            print("2 - Quartos")
            print("3 - Reservas")
            print("4 - Sair")
            try:
                op = int(input("\nEscolha: "))
            except ValueError:
                print("Opção inválida.")
                continue

            if op == 1:
                self.mh.menu()
            elif op == 2:
                self.mq.menu()
            elif op == 3:
                self.mr.menu()
            elif op == 4:
                print("\nFIM DO PROGRAMA")
                break
            else:
                print("Opção inválida.")