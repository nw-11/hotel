from visao.menu_principal_interface import Janela
from persistencia.dao_factory import DAOFactory
from persistencia.id_manager import IDManager


def main():
    IDManager.inicializar()
    DAOFactory.recuperarTodos()

    try:
        app = Janela()
        app.janela.mainloop()
    finally:
        DAOFactory.persistirTodos()


if __name__ == "__main__":
    main()