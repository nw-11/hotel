class ItemReserva:
    """
    Representa a associação entre uma Reserva e um Produto consumido.

    Não é uma entidade: não possui ID próprio nem métodos de persistência.
    Pertence inteiramente à Reserva que o contém.

    O subtotal é calculado dinamicamente como produto.preco × quantidade,
    garantindo que alterações no preço do produto se reflitam apenas em
    novos consumos (o preço vigente é capturado no momento do consumo
    via snapshot armazenado junto ao item — ver BancoDeDados).
    """

    def __init__(self, produto, quantidade=1):
        """
        Parameters
        ----------
        produto   : Produto  — produto consumido (entidade com ID e preço)
        quantidade: int      — unidades consumidas (mínimo 1)
        """
        if quantidade < 1:
            raise ValueError("A quantidade deve ser pelo menos 1.")
        self.produto = produto
        self.quantidade = int(quantidade)

    @property
    def subtotal(self):
        """Valor total deste item: preço unitário × quantidade."""
        return self.produto.preco * self.quantidade

    def __str__(self):
        return (
            f"{self.produto.nome} "
            f"(x{self.quantidade}) "
            f"— R$ {self.produto.preco:.2f} un. "
            f"= R$ {self.subtotal:.2f}"
        )
