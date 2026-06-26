from tkinter import *

#Frames Quartos---------------------------------------------------------------                

class FrameQuartos(Frame):
    def __init__(self, container, container2):
        super().__init__(container)


        Button(self, text="Cadastrar\nQuarto", width=10, height=2, command=self.Chama_QCad).pack(side="left")
        Button(self, text="Editar\nQuarto", width=10, height=2, command=self.Chama_QEdit).pack(side="left")
        Button(self, text="Remover\nQuartos", width=10, height=2, command=self.Chama_QRemove).pack(side="left")
        Button(self, text="Visualizar\npor ID", width=10, height=2, command=self.Chama_QVisual).pack(side="left")
        Button(self, text="Listar\nQuartos", width=10, height=2, command=self.Chama_QList).pack(side="left")
        Button(self, text="Listar\ndisponíveis", width=10, height=2, command=self.Chama_QDisponiveis).pack(side="left")

        #argumentos da lista de frames de quartos
        self.cad = FrameQCad(container2)
        self.edit = FrameQEdit(container2)
        self.remove = FrameQRemove(container2)
        self.visual = FrameQVisual(container2)
        self.list = FrameQList(container2)
        self.disponiveis = FrameQDisponiveis(container2)

        self.frames = {self.cad, self.edit, self.remove, self.visual, self.list, self.disponiveis}

    def Chama_QCad(self):
        for i in self.frames:
            i.pack_forget()

        self.cad.pack(fill="both", expand=True)

    def Chama_QEdit(self):
        for i in self.frames:
            i.pack_forget()

        self.edit.pack(fill="both", expand=True)

    def Chama_QRemove(self):
        for i in self.frames:
            i.pack_forget()

        self.remove.pack(fill="both", expand=True)

    def Chama_QVisual(self):
        for i in self.frames:
            i.pack_forget()

        self.visual.pack(fill="both", expand=True)

    def Chama_QList(self):
        for i in self.frames:
            i.pack_forget()

        self.list.pack(fill="both", expand=True)

    def Chama_QDisponiveis(self):
        for i in self.frames:
            i.pack_forget()

        self.disponiveis.pack(fill="both", expand=True)

class FrameQCad(Frame):
    def __init__(self, container):
        super().__init__(container)

        linha_num = Frame(self)
        linha_num.pack(anchor="w", pady=5)

        Label(linha_num, text="Número:", width=12, anchor="e").pack(side="left")
        self.Enum = Entry(linha_num, width=10)
        self.Enum.pack(side="left")

        #por estética, limitei à 3 tipos de quarto
        linha_tipo = Frame(self)
        linha_tipo.pack(anchor="w", pady=5)

        Label(linha_tipo, text="Tipo:", width=12, anchor="e").pack(side="left")
        self.tipo = StringVar(value="Standard")
        OptionMenu(linha_tipo, self.tipo, "Standard", "Luxo", "Master").pack(side="left")

        linha_valor = Frame(self)
        linha_valor.pack(anchor="w", pady=5)

        Label(linha_valor, text="Valor:", width=12, anchor="e").pack(side="left")
        self.Evalor = Entry(linha_valor, width=15)
        self.Evalor.pack(side="left")

        Button(self, text="Salvar", command=self.save).pack(pady=10)

        self.msg = Label(self)
        self.msg.pack()

    def save(self):
        self.numero = self.Enum.get()
        self.tipo = self.tipo.get()
        self.valor = self.Evalor.get()

        if self.numero == "" or self.tipo == "" or self.valor == "":
            self.msg.config(text="Erro: Informações insuficientes.")
        else:
            self.msg.config(text="Quarto cadastrado com sucesso.")
            self.after(3000, lambda: self.msg.config(text=""))

            self.Enum.delete(0, END)
            self.Etipo.delete(0, END)
            self.Evalor.delete(0, END)

class FrameQEdit(Frame):
    def __init__(self, container):
        super().__init__(container)

        linha_id = Frame(self)
        linha_id.pack(anchor="w", pady=5)

        Label(linha_id, text="ID:", width=12, anchor="e").pack(side="left")
        self.Eid = Entry(linha_id, width=10)
        self.Eid.pack(side="left")

        #por estética, limitei à 3 tipos de quarto
        linha_tipo = Frame(self)
        linha_tipo.pack(anchor="w", pady=5)

        Label(linha_tipo, text="Tipo:", width=12, anchor="e").pack(side="left")
        self.tipo = StringVar(value="Standard")
        OptionMenu(linha_tipo, self.tipo, "Standard", "Luxo", "Master").pack(side="left")

        linha_valor = Frame(self)
        linha_valor.pack(anchor="w", pady=5)

        Label(linha_valor, text="Valor:", width=12, anchor="e").pack(side="left")
        self.Evalor = Entry(linha_valor, width=15)
        self.Evalor.pack(side="left")

        Button(self, text="Salvar Alterações", command=self.save).pack(pady=10)

        self.msg = Label(self)
        self.msg.pack()

    def save(self):
        self.msg.config(text="Quarto atualizado com sucesso.")
        self.after(3000, lambda: self.msg.config(text=""))

class FrameQRemove(Frame):
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
            self.msg.config(text="Quarto removido com sucesso.")
            self.Eid.delete(0, END)

        self.after(3000, lambda: self.msg.config(text=""))

class FrameQVisual(Frame):
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

class FrameQList(Frame):
    def __init__(self, container):
        super().__init__(container)

        Button(self, text="Listar Quartos", command=self.listar).pack(pady=10)

        self.lista = Listbox(self, width=60, height=15)
        self.lista.pack()

    def listar(self):
        self.lista.delete(0, END)

class FrameQDisponiveis(Frame):
    def __init__(self, container):
        super().__init__(container)

        Button(self, text="Listar Disponíveis", command=self.listar).pack(pady=10)

        self.lista = Listbox(self, width=60, height=15)
        self.lista.pack()

    def listar(self):
        self.lista.delete(0, END)