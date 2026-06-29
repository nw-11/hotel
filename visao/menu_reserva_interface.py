from tkinter import *

class FrameReservas(Frame):
    def __init__(self, container, container2):
        super().__init__(container)

        Button(self, text="Nova\nReserva", width=10, height=2, command=self.Chama_RCad).pack(side="left")
        Button(self, text="Editar\nReserva", width=10, height=2, command=self.Chama_REdit).pack(side="left")
        Button(self, text="Cancelar\nReserva", width=10, height=2, command=self.Chama_RRemove).pack(side="left")
        Button(self, text="Visualizar\npor ID", width=10, height=2, command=self.Chama_RVisual).pack(side="left")
        Button(self, text="Listar\nReservas", width=10, height=2, command=self.Chama_RList).pack(side="left")

        self.cad = FrameRCad(container2)
        self.edit = FrameREdit(container2)
        self.remove = FrameRRemove(container2)
        self.visual = FrameRVisual(container2)
        self.lista = FrameRList(container2)

        self.frames = {self.cad, self.edit, self.remove, self.visual, self.lista}

    def Chama_RCad(self):
        for i in self.frames:
            i.pack_forget()

        self.cad.pack(fill="both", expand=True)

    def Chama_REdit(self):
        for i in self.frames:
            i.pack_forget()

        self.edit.pack(fill="both", expand=True)

    def Chama_RRemove(self):
        for i in self.frames:
            i.pack_forget()

        self.remove.pack(fill="both", expand=True)

    def Chama_RVisual(self):
        for i in self.frames:
            i.pack_forget()

        self.visual.pack(fill="both", expand=True)

    def Chama_RList(self):
        for i in self.frames:
            i.pack_forget()

        self.lista.pack(fill="both", expand=True)

class FrameRCad(Frame):
    def __init__(self, container):
        super().__init__(container)

        linha_hospede = Frame(self)
        linha_hospede.pack(anchor="w", pady=5)

        Label(linha_hospede, text="Hóspede ID:", width=12, anchor="e").pack(side="left")
        self.Ehospede = Entry(linha_hospede, width=10)
        self.Ehospede.pack(side="left")

        linha_quarto = Frame(self)
        linha_quarto.pack(anchor="w", pady=5)

        Label(linha_quarto, text="Quarto ID:", width=12, anchor="e").pack(side="left")
        self.Equarto = Entry(linha_quarto, width=10)
        self.Equarto.pack(side="left")

        linha_entrada = Frame(self)
        linha_entrada.pack(anchor="w", pady=5)

        Label(linha_entrada, text="Entrada:", width=12, anchor="e").pack(side="left")
        self.Eentrada = Entry(linha_entrada, width=15)
        self.Eentrada.pack(side="left")

        linha_saida = Frame(self)
        linha_saida.pack(anchor="w", pady=5)

        Label(linha_saida, text="Saída:", width=12, anchor="e").pack(side="left")
        self.Esaida = Entry(linha_saida, width=15)
        self.Esaida.pack(side="left")

        Button(self, text="Salvar", command=self.save).pack(pady=10)

        self.msg = Label(self)
        self.msg.pack()

    def save(self):
        self.hospede = self.Ehospede.get()
        self.quarto = self.Equarto.get()
        self.entrada = self.Eentrada.get()
        self.saida = self.Esaida.get()

        if self.hospede == "" or self.quarto == "" or self.entrada == "" or self.saida == "":
            self.msg.config(text="Erro: Informações insuficientes.")
        else:
            self.msg.config(text="Reserva cadastrada com sucesso.")
            self.after(3000, lambda: self.msg.config(text=""))

            self.Ehospede.delete(0, END)
            self.Equarto.delete(0, END)
            self.Eentrada.delete(0, END)
            self.Esaida.delete(0, END)

class FrameREdit(Frame):
    def __init__(self, container):
        super().__init__(container)

        linha_id = Frame(self)
        linha_id.pack(anchor="w", pady=5)

        Label(linha_id, text="ID:", width=12, anchor="e").pack(side="left")
        self.Eid = Entry(linha_id, width=10)
        self.Eid.pack(side="left")

        linha_entrada = Frame(self)
        linha_entrada.pack(anchor="w", pady=5)

        Label(linha_entrada, text="Entrada:", width=12, anchor="e").pack(side="left")
        self.Eentrada = Entry(linha_entrada, width=15)
        self.Eentrada.pack(side="left")

        linha_saida = Frame(self)
        linha_saida.pack(anchor="w", pady=5)

        Label(linha_saida, text="Saída:", width=12, anchor="e").pack(side="left")
        self.Esaida = Entry(linha_saida, width=15)
        self.Esaida.pack(side="left")

        Button(self, text="Salvar Alterações", command=self.save).pack(pady=10)

        self.msg = Label(self)
        self.msg.pack()

    def save(self):
        self.msg.config(text="Reserva atualizada com sucesso.")
        self.after(3000, lambda: self.msg.config(text=""))

class FrameRRemove(Frame):
    def __init__(self, container):
        super().__init__(container)

        linha_id = Frame(self)
        linha_id.pack(anchor="w", pady=5)

        Label(linha_id, text="ID:", width=12, anchor="e").pack(side="left")
        self.Eid = Entry(linha_id, width=10)
        self.Eid.pack(side="left")

        Button(self, text="Cancelar Reserva", command=self.remove).pack(pady=10)

        self.msg = Label(self)
        self.msg.pack()

    def remove(self):
        if self.Eid.get() == "":
            self.msg.config(text="Informe um ID.")
        else:
            self.msg.config(text="Reserva cancelada com sucesso.")
            self.Eid.delete(0, END)

        self.after(3000, lambda: self.msg.config(text=""))

class FrameRVisual(Frame):
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

class FrameRList(Frame):
    def __init__(self, container):
        super().__init__(container)

        Button(self, text="Listar Reservas", command=self.listar).pack(pady=10)

        self.lista = Listbox(self, width=60, height=15)
        self.lista.pack()

    def listar(self):
        self.lista.delete(0, END)