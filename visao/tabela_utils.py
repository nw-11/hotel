from tkinter import *
from tkinter import ttk


class TabelaOrdenavel(Frame):
    def __init__(self, container, colunas, altura=15):
        super().__init__(container)
        self.colunas = colunas
        self.linhas = []
        self.ordem_reversa = {}

        frame_tabela = Frame(self)
        frame_tabela.pack(fill="both", expand=True)

        barra_y = Scrollbar(frame_tabela, orient="vertical")
        barra_y.pack(side="right", fill="y")

        barra_x = Scrollbar(frame_tabela, orient="horizontal")
        barra_x.pack(side="bottom", fill="x")

        ids_colunas = [coluna[0] for coluna in colunas]
        self.tree = ttk.Treeview(
            frame_tabela,
            columns=ids_colunas,
            show="headings",
            height=altura,
            yscrollcommand=barra_y.set,
            xscrollcommand=barra_x.set
        )
        self.tree.pack(side="left", fill="both", expand=True)

        barra_y.config(command=self.tree.yview)
        barra_x.config(command=self.tree.xview)

        for id_coluna, titulo, largura, _ in colunas:
            self.tree.heading(
                id_coluna,
                text=titulo,
                command=lambda coluna=id_coluna: self.ordenar_por(coluna)
            )
            self.tree.column(id_coluna, width=largura, anchor="w", stretch=True)
            self.ordem_reversa[id_coluna] = False

    def limpar(self):
        self.linhas = []
        self._redesenhar()

    def carregar(self, linhas):
        self.linhas = list(linhas)
        self._redesenhar()

    def mostrar_erro(self, mensagem):
        self.linhas = []
        self._redesenhar()
        self.tree.insert("", END, values=[mensagem] + [""] * (len(self.colunas) - 1), tags=("erro",))
        self.tree.tag_configure("erro", foreground="red")

    def ordenar_por(self, id_coluna):
        coluna = next(coluna for coluna in self.colunas if coluna[0] == id_coluna)
        obter_valor = coluna[3]
        reverso = self.ordem_reversa[id_coluna]

        self.linhas.sort(
            key=lambda linha: self._valor_ordenacao(obter_valor(linha)),
            reverse=reverso
        )

        self.ordem_reversa[id_coluna] = not reverso
        self._redesenhar()

    def _redesenhar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for linha in self.linhas:
            self.tree.insert(
                "",
                END,
                values=[self._formatar(obter_valor(linha)) for _, _, _, obter_valor in self.colunas]
            )

    def _valor_ordenacao(self, valor):
        if valor is None:
            return ""
        if isinstance(valor, bool):
            return int(valor)
        if isinstance(valor, (int, float)):
            return valor
        return str(valor).lower()

    def _formatar(self, valor):
        if isinstance(valor, bool):
            return "Sim" if valor else "Nao"
        if isinstance(valor, float):
            return f"{valor:.2f}"
        return valor
