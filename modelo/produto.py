from modelo.entidade import Entidade
from modelo.banco_de_dados import Bancodedados


class Produto(Entidade):
    """
    Representa um produto ou serviço oferecido pelo hotel
    (ex: água, café, lavanderia, minibar).

    Possui identidade própria, preço centralizado e persistência
    independente. ItemReserva referencia um Produto pelo ID,
    evitando duplicação de informações.
    """

    CATEGORIAS = ["Alimentação", "Bebidas", "Lavanderia", "Comodidades", "Outros"]

    def __init__(self, nome, preco, categoria="Outros", id=None):
        super().__init__(id)
        self.nome = nome
        self.preco = float(preco)
        self.categoria = categoria

    # ------------------------------------------------------------------
    # Implementação dos métodos abstratos de Entidade
    # ------------------------------------------------------------------

    def salvar(self):
        Bancodedados.salva_produto(self)
        self.persistido = True

    def atualizar(self):
        if not self.persistido:
            raise RuntimeError("Produto ainda não foi salvo. Use salvar() primeiro.")
        Bancodedados.atualiza_produto(self)

    def apagar(self):
        if Bancodedados.apaga_produto(self):
            self.id = None
            self.persistido = False
            return True
        return False

    def __str__(self):
        return (
            f"ID: {self.id}\n"
            f"Nome: {self.nome}\n"
            f"Categoria: {self.categoria}\n"
            f"Preço unitário: R$ {self.preco:.2f}"
        )
