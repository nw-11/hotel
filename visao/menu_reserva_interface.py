from tkinter import *
from modelo.reserva import Reserva
from persistencia.dao_factory import DAOFactory
from persistencia.id_manager import IDManager
from persistencia.persistence_exception import PersistenceException
from datetime import datetime

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
        
        self.edit.msg.config(text="")
        self.edit.pack(fill="both", expand=True)

    def Chama_RRemove(self):
        for i in self.frames:
            i.pack_forget()
        self.remove.msg.config(text="")
        self.remove.pack(fill="both", expand=True)

    def Chama_RVisual(self):
        for i in self.frames:
            i.pack_forget()

        self.visual.pack(fill="both", expand=True)
        self.visual.resultado.config(text="")

    def Chama_RList(self):
        for i in self.frames:
            i.pack_forget()

        self.lista.pack(fill="both", expand=True)
        self.lista.lista.delete(0, END)

class FrameRCad(Frame):
    def __init__(self, container):
        super().__init__(container)
        self.hospedeDAO = DAOFactory.getHospedeDAO()
        self.quartoDAO = DAOFactory.getQuartoDAO()
        self.produtoDAO = DAOFactory.getProdutoDAO()
        self.reservaDAO = DAOFactory.getReservaDAO()

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
        elif (not self.hospede.isdigit()) or (not self.quarto.isdigit()):
            self.msg.config(text="Erro: ID invalido", fg="red")
        else:
            try:
                h = self.hospedeDAO.carregar(int(self.hospede))
                q = self.quartoDAO.carregar(int(self.quarto))
                if(q.disponivel == False):
                    self.msg.config(text="Quarto Indisponivel", fg="red")
                    return
                checkin = self.entrada
                checkout = self.saida
                reserva = Reserva(h, q, checkin, checkout)
                reserva.id = IDManager.proximo_id_reserva()
                self.reservaDAO.salvar(reserva)

                self.msg.config(text="Reserva cadastrada com sucesso.", fg="black")
                self.after(3000, lambda: self.msg.config(text=""))
                self.Ehospede.delete(0, END)
                self.Equarto.delete(0, END)
                self.Eentrada.delete(0, END)
                self.Esaida.delete(0, END)
            except PersistenceException as e:
                self.msg.config(text=str(e), fg="red")
            except ValueError as e:
                self.msg.config(text=str(e), fg="red")

class FrameREdit(Frame):
    def __init__(self, container):
        super().__init__(container)
        self.hospedeDAO = DAOFactory.getHospedeDAO()
        self.quartoDAO = DAOFactory.getQuartoDAO()
        self.produtoDAO = DAOFactory.getProdutoDAO()
        self.reservaDAO = DAOFactory.getReservaDAO()
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
        checkin = self.Eentrada.get()
        checkout = self.Esaida.get()
        if(not self.Eid.get().isdigit()):
            self.msg.config(text="ID invalido", fg="red")
            return
        try:
            id = int(self.Eid.get())
            r = self.reservaDAO.carregar(id)
            r.validar_datas(checkin, checkout)
            r.checkin = checkin
            r.checkout = checkout
            self.reservaDAO.atualizar(r)
            self.msg.config(text="Reserva atualizada com sucesso.", fg="black")
            self.after(3000, lambda: self.msg.config(text=""))

        except PersistenceException as e:
            self.msg.config(text=str(e), fg="red")
        except ValueError as e:
            self.msg.config(text=str(e), fg="red")
        except Exception as e:
            self.msg.config(text=str(e), fg="red")

        
class FrameRRemove(Frame):
    def __init__(self, container):
        super().__init__(container)
        self.reservaDAO = DAOFactory.getReservaDAO()
        linha_id = Frame(self)
        linha_id.pack(anchor="w", pady=5)

        Label(linha_id, text="ID:", width=12, anchor="e").pack(side="left")
        self.Eid = Entry(linha_id, width=10)
        self.Eid.pack(side="left")

        Button(self, text="Cancelar Reserva", command=self.remove).pack(pady=10)

        self.msg = Label(self)
        self.msg.pack()

    def remove(self):
        if not self.Eid.get().isdigit():
            self.msg.config(text="ID Invalido", fg="red")
        else:
            try:
                id = int(self.Eid.get())
                self.reservaDAO.apagar(id)
                self.msg.config(text="Reserva cancelada com sucesso.")
                self.Eid.delete(0, END)
                self.after(3000, lambda: self.msg.config(text=""))
            except PersistenceException as e:
                self.msg.config(text=str(e), fg="red")


class FrameRVisual(Frame):
    def __init__(self, container):
        super().__init__(container)
        self.reservaDAO = DAOFactory.getReservaDAO()
        linha_id = Frame(self)
        linha_id.pack(anchor="w", pady=5)

        Label(linha_id, text="ID:", width=12, anchor="e").pack(side="left")
        self.Eid = Entry(linha_id, width=10)
        self.Eid.pack(side="left")

        Button(self, text="Visualizar", command=self.visualizar).pack(pady=10)

        self.resultado = Label(self, justify="left")
        self.resultado.pack(anchor="w")

    def visualizar(self):
        id = self.Eid.get()
        if(not id.isdigit()):
            self.resultado.config(text="ID invalido", fg="red")
            return
        else:
            try:
                reserva = self.reservaDAO.carregar(int(id))
                self.resultado.config(text=str(reserva), fg="black")
                self.Eid.delete(0, END)
            except PersistenceException as e:
                self.resultado.config(text=str(e), fg="red")
            except Exception as e:
                self.resultado.config(text=str(e), fg="red")

class FrameRList(Frame):
    def __init__(self, container):
        super().__init__(container)
        self.reservaDAO = DAOFactory.getReservaDAO()
        Button(self, text="Listar Reservas", command=self.listar).pack(pady=10)

        self.lista = Listbox(self, width=120, height=15)
        self.lista.pack()

    def listar(self):
        self.lista.delete(0, END)
        try:
            reservas = []
            reservas = self.reservaDAO.carregarTodos()
            for r in reservas:
                self.lista.insert(END, f"id = {r.id} | hospede = {r.hospede.nome} | categoria = {r.quarto.tipo} check-in = {r.checkin} | checkout = {r.checkout}")
        except PersistenceException as e:
                self.lista.insert(END, str(e))
                self.lista.itemconfig(0, fg="red")
        except Exception as e:
                self.lista.insert(END, str(e))
                self.lista.itemconfig(0, fg="red")
