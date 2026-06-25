class PersistenceException(Exception):

    def __init__(self, operacao, problema, valor):

        mensagem = (
            f"Erro em {operacao}: "
            f"{problema}. "
            f"Valor: {valor}"
        )

        super().__init__(mensagem)