from modelo.banco_de_dados import Bancodedados
from visao.menu_principal import Menu_Principal


def main():
    # Inicializa o banco (cria as tabelas se não existirem)
    Bancodedados.inicializar()

    # Inicia a interface
    app = Menu_Principal()
    app.menu()


if __name__ == "__main__":
    main()