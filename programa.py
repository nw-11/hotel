from visao.menu_principal_interface import *
from persistencia.id_manager import IDManager


def main():

    # garante criação/controle do arquivo de ids
    IDManager.inicializar()

    bob = Janela()
    bob.janela.mainloop()


if __name__ == "__main__":
    main()