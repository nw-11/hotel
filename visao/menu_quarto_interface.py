from tkinter import *
from modelo.quarto import Quarto
from persistencia.dao_factory import DAOFactory
from persistencia.id_manager import IDManager
from persistencia.persistence_exception import PersistenceException
from visao.tabela_utils import TabelaOrdenavel


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

        self.cad.msg.config(text="")
        self.cad.pack(fill="both", expand=True)

    def Chama_QEdit(self):
        for i in self.frames:
            i.pack_forget()
        self.edit.msg.config(text="")
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
        self.list.limpar_tela()

    def Chama_QDisponiveis(self):
        for i in self.frames:
            i.pack_forget()

        self.disponiveis.pack(fill="both", expand=True)
        self.disponiveis.limpar_tela()

class FrameQCad(Frame):
    def __init__(self, container):
        super().__init__(container)
        self.dao = DAOFactory.getQuartoDAO()
        
        linha_num = Frame(self)
        linha_num.pack(anchor="w", pady=5)

        Label(linha_num, text="Número:", width=12, anchor="e").pack(side="left")
        self.Enum = Entry(linha_num, width=10)
        self.Enum.pack(side="left")

        #por estética, limitei à 3 tipos de quarto
        linha_tipo = Frame(self)
        linha_tipo.pack(anchor="w", pady=5)

        Label(linha_tipo, text="Tipo:", width=12, anchor="e").pack(side="left")
        self.tipo = StringVar(value="Standart")
        OptionMenu(linha_tipo, self.tipo, "Standart", "Luxo", "Master").pack(side="left")

        linha_valor = Frame(self)
        linha_valor.pack(anchor="w", pady=5)

        Label(linha_valor, text="Valor:", width=12, anchor="e").pack(side="left")
        self.Evalor = Entry(linha_valor, width=15)
        self.Evalor.pack(side="left")

        Button(self, text="Salvar", command=self.save).pack(pady=10)

        self.msg = Label(self)
        self.msg.pack()

    def save(self):
        num = self.Enum.get()
        tipo = self.tipo.get()
        val = self.Evalor.get().strip()

        if num == "" or val == "":
            self.msg.config(text="Erro: Informações insuficientes.",fg="red")
        elif not num.isdigit():
            self.msg.config(text="Erro: Numero invalido", fg="red")

        else:
            try:
                val = float(val)
                if(val <= 0):
                    raise ValueError
                quarto = Quarto(num, tipo, val, True)
                quarto.id = IDManager.proximo_id_quarto()
                self.dao.salvar(quarto)

                self.msg.config(text="Quarto cadastrado com sucesso.")
                self.after(3000, lambda: self.msg.config(text=""))

                self.Enum.delete(0, END)
                self.Evalor.delete(0, END)
            except PersistenceException as e:
                self.msg.config(text=str(e), fg="red")
            except ValueError:
                self.msg.config(text="Valor Inválido", fg="red")
                self.Enum.delete(0, END)
                self.Evalor.delete(0, END)
            except Exception as e:
                self.msg.config(text=str(e), fg="red")

class FrameQEdit(Frame):
    def __init__(self, container):
        super().__init__(container)
        self.dao = DAOFactory.getQuartoDAO()
        linha_id = Frame(self)
        linha_id.pack(anchor="w", pady=5)

        Label(linha_id, text="ID:", width=12, anchor="e").pack(side="left")
        self.Eid = Entry(linha_id, width=10)
        self.Eid.pack(side="left")

        #por estética, limitei à 3 tipos de quarto
        linha_tipo = Frame(self)
        linha_tipo.pack(anchor="w", pady=5)

        Label(linha_tipo, text="Tipo:", width=12, anchor="e").pack(side="left")
        self.tipo = StringVar(value="Standart")
        OptionMenu(linha_tipo, self.tipo, "Standart", "Luxo", "Master").pack(side="left")

        linha_valor = Frame(self)
        linha_valor.pack(anchor="w", pady=5)

        Label(linha_valor, text="Valor:", width=12, anchor="e").pack(side="left")
        self.Evalor = Entry(linha_valor, width=15)
        self.Evalor.pack(side="left")

        Button(self, text="Salvar Alterações", command=self.save).pack(pady=10)

        self.msg = Label(self)
        self.msg.pack()

    def save(self):
        id = self.Eid.get()
        tipo = self.tipo.get()
        val = self.Evalor.get().strip()
        if(not id.isdigit()):
            self.msg.config(text="ID invalido", fg="red")
        else:
            try:
                val = float(val)
                if(val <= 0):
                    raise ValueError
                q = self.dao.carregar(int(id))
                q.tipo = tipo
                q.diaria = val

                self.dao.atualizar(q)
                self.msg.config(text="Quarto atualizado com sucesso.",fg="black")
                self.after(3000, lambda: self.msg.config(text=""))
                self.Eid.delete(0, END)
                self.Evalor.delete(0, END)
            except PersistenceException as e:
                self.msg.config(text=str(e), fg="red")
                self.Eid.delete(0, END)
                self.Evalor.delete(0, END)
            except ValueError:
                self.msg.config(text="Preco invalido", fg="red")
                self.Eid.delete(0, END)
                self.Evalor.delete(0, END)
                

class FrameQRemove(Frame):
    def __init__(self, container):
        super().__init__(container)
        self.dao = DAOFactory.getQuartoDAO()
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
            self.msg.config(text="Informe um ID.",fg="black")
        elif not self.Eid.get().isdigit():
            self.msg.config(text="ID invalido",fg="red")
        else:
            try:
                id = self.Eid.get()
                self.dao.apagar(int(id))
                self.msg.config(text="Quarto removido com sucesso.",fg="black")
                self.Eid.delete(0, END)
                self.after(3000, lambda: self.msg.config(text=""))
            except PersistenceException as e:
                self.msg.config(text=str(e),fg="red")
            except Exception as e:
                self.msg.config(text=str(e),fg="red")

class FrameQVisual(Frame):
    def __init__(self, container):
        super().__init__(container)
        self.dao = DAOFactory.getQuartoDAO()
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
            self.resultado.config(text="ID invalido",fg="red")
        else:
            try:
                id = int(id)
                q = self.dao.carregar(id)
                self.resultado.config(text=str(q),fg="black")
                self.Eid.delete(0, END)
            except PersistenceException as e:
                self.resultado.config(text=str(e),fg="red")
                self.Eid.delete(0, END)

class FrameQList(Frame):
    def __init__(self, container):
        super().__init__(container)
        self.dao = DAOFactory.getQuartoDAO()
        Button(self, text="Listar Quartos", command=self.listar).pack(pady=10)

        self.tabela = TabelaOrdenavel(
            self,
            [
                ("id", "ID", 60, lambda quarto: quarto.id),
                ("numero", "Numero", 100, lambda quarto: quarto.numero),
                ("tipo", "Tipo", 140, lambda quarto: quarto.tipo),
                ("diaria", "Diaria", 100, lambda quarto: quarto.diaria),
                ("disponivel", "Disponivel", 120, lambda quarto: quarto.disponivel),
            ]
        )
        self.tabela.pack(fill="both", expand=True, padx=10, pady=10)

    def listar(self):
        try:
            self.tabela.carregar(self.dao.carregarTodos())
        except PersistenceException as e:
            self.tabela.mostrar_erro(str(e))

    def limpar_tela(self):
        self.tabela.limpar()

class FrameQDisponiveis(Frame):
    def __init__(self, container):
        super().__init__(container)
        self.dao = DAOFactory.getQuartoDAO()
        Button(self, text="Listar Disponiveis", command=self.listar).pack(pady=10)

        self.tabela = TabelaOrdenavel(
            self,
            [
                ("id", "ID", 60, lambda quarto: quarto.id),
                ("numero", "Numero", 100, lambda quarto: quarto.numero),
                ("tipo", "Tipo", 140, lambda quarto: quarto.tipo),
                ("diaria", "Diaria", 100, lambda quarto: quarto.diaria),
                ("disponivel", "Disponivel", 120, lambda quarto: quarto.disponivel),
            ]
        )
        self.tabela.pack(fill="both", expand=True, padx=10, pady=10)

    def listar(self):
        try:
            quartos = self.dao.filtrar(lambda quarto: quarto.disponivel)
            if len(quartos) == 0:
                self.tabela.mostrar_erro("Nenhum quarto disponivel")
                return
            self.tabela.carregar(quartos)
        except PersistenceException as e:
            self.tabela.mostrar_erro(str(e))

    def limpar_tela(self):
        self.tabela.limpar()
