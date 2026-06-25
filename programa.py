from visao.menu_principal import Menu_Principal
from persistencia.id_manager import IDManager


def main():

    # garante criação/controle do arquivo de ids
    IDManager.inicializar()

    app = Menu_Principal()

    app.menu()


if __name__ == "__main__":
    main()