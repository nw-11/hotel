from tkinter import *

class FrameProdutos(Frame):
    def __init__(self, container, container2):
        super().__init__(container)

        Button(self, text="Cadastrar\nProduto", width=10, height=2, command=self.Chama_PCad).pack(side="left")
        Button(self, text="Editar\nProduto", width=10, height=2, command=self.Chama_PEdit).pack(side="left")
        Button(self, text="Remover\nProdutos", width=10, height=2, command=self.Chama_PRemove).pack(side="left")
        Button(self, text="Visualizar\npor ID", width=10, height=2, command=self.Chama_PVisual).pack(side="left")
        Button(self, text="Listar\nProdutos", width=10, height=2, command=self.Chama_PList).pack(side="left")

        self.cad = FramePCad(container2)
        self.edit = FramePEdit(container2)
        self.remove = FramePRemove(container2)
        self.visual = FramePVisual(container2)
        self.lista = FramePList(container2)

        self.frames = {self.cad, self.edit, self.remove, self.visual, self.lista}

    def Chama_PCad(self):
        for i in self.frames:
            i.pack_forget()

        self.cad.pack(fill="both", expand=True)

    def Chama_PEdit(self):
        for i in self.frames:
            i.pack_forget()

        self.edit.pack(fill="both", expand=True)

    def Chama_PRemove(self):
        for i in self.frames:
            i.pack_forget()

        self.remove.pack(fill="both", expand=True)

    def Chama_PVisual(self):
        for i in self.frames:
            i.pack_forget()

        self.visual.pack(fill="both", expand=True)

    def Chama_PList(self):
        for i in self.frames:
            i.pack_forget()

        self.lista.pack(fill="both", expand=True)

class FramePCad(Frame):
    def __init__(self, container):
        super().__init__(container)

        linha_nome = Frame(self)
        linha_nome.pack(anchor="w", pady=5)

        Label(linha_nome, text="Nome:", width=12, anchor="e").pack(side="left")
        self.Enome = Entry(linha_nome, width=30)
        self.Enome.pack(side="left")

        linha_preco = Frame(self)
        linha_preco.pack(anchor="w", pady=5)

        Label(linha_preco, text="Preço:", width=12, anchor="e").pack(side="left")
        self.Epreco = Entry(linha_preco, width=15)
        self.Epreco.pack(side="left")

        Button(self, text="Salvar", command=self.save).pack(pady=10)

        self.msg = Label(self)
        self.msg.pack()

    def save(self):
        self.nome = self.Enome.get()
        self.preco = self.Epreco.get()

        if self.nome == "" or self.preco == "":
            self.msg.config(text="Erro: Informações insuficientes.")
        else:
            self.msg.config(text="Produto cadastrado com sucesso.")
            self.after(3000, lambda: self.msg.config(text=""))

            self.Enome.delete(0, END)
            self.Epreco.delete(0, END)

class FramePEdit(Frame):
    def __init__(self, container):
        super().__init__(container)

        linha_id = Frame(self)
        linha_id.pack(anchor="w", pady=5)

        Label(linha_id, text="ID:", width=12, anchor="e").pack(side="left")
        self.Eid = Entry(linha_id, width=10)
        self.Eid.pack(side="left")

        linha_nome = Frame(self)
        linha_nome.pack(anchor="w", pady=5)

        Label(linha_nome, text="Nome:", width=12, anchor="e").pack(side="left")
        self.Enome = Entry(linha_nome, width=30)
        self.Enome.pack(side="left")

        linha_preco = Frame(self)
        linha_preco.pack(anchor="w", pady=5)

        Label(linha_preco, text="Preço:", width=12, anchor="e").pack(side="left")
        self.Epreco = Entry(linha_preco, width=15)
        self.Epreco.pack(side="left")

        Button(self, text="Salvar Alterações", command=self.save).pack(pady=10)

        self.msg = Label(self)
        self.msg.pack()

    def save(self):
        self.msg.config(text="Produto atualizado com sucesso.")
        self.after(3000, lambda: self.msg.config(text=""))

class FramePRemove(Frame):
    def __init__(self, container):
        super().__init__(container)

        linha_id = Frame(self)
        linha_id.pack(anchor="w", pady=5)

        Label(linha_id, text="ID:", width=12, anchor="e").pack(side="left")
        self.Eid = Entry(linha_id, width=10)
        self.Eid.pack(side="left")

        Button(self, text="Remover", command=self.remove).pack(pady=10)

        self.msg = Label(self)
        self.msg.pack()

    def remove(self):
        if self.Eid.get() == "":
            self.msg.config(text="Informe um ID.")
        else:
            self.msg.config(text="Produto removido com sucesso.")
            self.Eid.delete(0, END)

        self.after(3000, lambda: self.msg.config(text=""))

class FramePVisual(Frame):
    def __init__(self, container):
        super().__init__(container)

        linha_id = Frame(self)
        linha_id.pack(anchor="w", pady=5)

        Label(linha_id, text="ID:", width=12, anchor="e").pack(side="left")
        self.Eid = Entry(linha_id, width=10)
        self.Eid.pack(side="left")

        Button(self, text="Visualizar", command=self.visualizar).pack(pady=10)

        self.resultado = Label(self, justify="left")
        self.resultado.pack(anchor="w")

    def visualizar(self):
        pass

class FramePList(Frame):
    def __init__(self, container):
        super().__init__(container)

        Button(self, text="Listar Produtos", command=self.listar).pack(pady=10)

        self.lista = Listbox(self, width=60, height=15)
        self.lista.pack()

    def listar(self):
        self.lista.delete(0, END)