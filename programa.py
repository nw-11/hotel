from visao.menu_principal import Menu_Principal
from persistencia.dao_factory import DAOFactory
from persistencia.id_manager import IDManager


def main():

    IDManager.inicializar()

    DAOFactory.recuperarTodos()

    try:

        app = Menu_Principal()

        app.menu()

    finally:

        DAOFactory.persistirTodos()


if __name__ == "__main__":
    main()