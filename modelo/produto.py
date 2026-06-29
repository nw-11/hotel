from modelo.entidade import Entidade


class Produto(Entidade):

    CATEGORIAS = [
        "Alimentação",
        "Bebidas",
        "Lavanderia",
        "Comodidades",
        "Outros"
    ]

    def __init__(self, nome, preco, categoria="Outros", id=None):
        super().__init__(id)
        self.nome = nome
        self.preco = float(preco)
        self.categoria = categoria

    def __str__(self):
        return (
            f"ID: {self.id}\n"
            f"Nome: {self.nome}\n"
            f"Preço: R$ {self.preco:.2f}\n"
            f"Categoria: {self.categoria}"
        )