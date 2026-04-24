from .menu_hospede import Menu_Hospede
from .menu_quarto import Menu_Quarto
from .menu_reserva import Menu_Reserva


class Menu_Principal:
    def __init__(self):
        self.mh = Menu_Hospede()
        self.mq = Menu_Quarto()
        self.mr = Menu_Reserva()

    def menu(self):
        print("\nAdministrador Hoteleiro - v0.0.1\n")
        while True:
            print("MENU PRINCIPAL")
            print("\n1 - Hóspede")
            print("2 - Quarto")
            print("3 - Reserva")
            print("4 - Sair")
            escolha = int(input("\nDigite sua escolha: "))
            if escolha == 1:
                self.mh.menu()
            elif escolha == 2:
                self.mq.menu()
            elif escolha == 3:
                self.mr.menu()
            elif escolha == 4:
                print("\nFIM DO PROGRAMA")
                break
            else:
                print("Escolha um número válido!")

#teste
a = Menu_Principal()
a.menu()