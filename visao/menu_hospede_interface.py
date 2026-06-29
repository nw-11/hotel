from tkinter import *
from modelo.hospede import Hospede
from persistencia.dao_factory import DAOFactory
from persistencia.id_manager import IDManager
from persistencia.persistence_exception import PersistenceException
from visao.tabela_utils import TabelaOrdenavel


#Frames referentes à Hospedagem------------------------------------------------
class FrameHospedes(Frame):
    def __init__(self, container, container2):
        super().__init__(container)

        #Label(self, text="Menu de Hóspedes", font=("Arial", 20)).pack()
        Button(self, text="Cadastrar\nHóspede", width=10, height=2, command=self.Chama_Cad).pack(side="left")
        Button(self, text="Editar\nHóspede", width=10, height=2, command=self.Chama_HEdit).pack(side="left")
        Button(self, text="Remover\nHóspedes", width=10, height=2, command=self.Chama_HRemove).pack(side="left")
        Button(self, text="Visualizar\npor ID", width=10, height=2, command=self.Chama_HVisual).pack(side="left")
        Button(self, text="Listar\nhóspedes", width=10, height=2, command=self.Chama_HList).pack(side="left")
        Button(self, text="Busca\npor nome", width=10, height=2, command=self.Chama_HSearch).pack(side="left")

        #argumentos da lista de frames de hospede
        self.cad = FrameCad(container2)
        self.edit = FrameHEdit(container2)
        self.remove = FrameHRemove(container2)
        self.visual = FrameHVisual(container2)
        self.list = FrameHList(container2)
        self.search = FrameHSearch(container2)

        self.frames = {self.cad, self.edit, self.remove, self.visual, self.list, self.search}


    def Chama_Cad(self):
        for i in self.frames:
            i.pack_forget()
            
        self.cad.pack(fill="both", expand=True)

    def Chama_HEdit(self):
        for i in self.frames:
            i.pack_forget()

        self.edit.pack(fill="both", expand=True)   

    def Chama_HRemove(self):
        for i in self.frames:
            i.pack_forget()

        self.remove.pack(fill="both", expand=True)    

    def Chama_HVisual(self):
        for i in self.frames:
            i.pack_forget()

        self.visual.msg.config(text="")
        self.visual.Eid.delete(0, END)
        self.visual.pack(fill="both", expand=True)    

    def Chama_HList(self):
        for i in self.frames:
            i.pack_forget()
        self.list.limpar_tela()
        self.list.pack(fill="both", expand=True)   

    def Chama_HSearch(self):
        for i in self.frames:
            i.pack_forget()
        
        self.search.Enome.delete(0, END)
        self.search.limpar_tela()
        self.search.pack(fill="both", expand=True)    
                
class FrameCad(Frame):
    def __init__(self, container2):
        super().__init__(container2)
        self.dao = DAOFactory.getHospedeDAO()

        #Padrão: Enome, Ecpf, Eemail, Etel = variáveis de Entry
        #        linha_nome, linha_cpf, linha_email, linha_tel = variáveis que armazenam o dado de Entry
        
        #nome
        linha_nome = Frame(self)
        linha_nome.pack(anchor="w", pady=5)

        Label(linha_nome, text="Nome:", width=12, anchor="e").pack(side="left")
        self.Enome = Entry(linha_nome, width=40)
        self.Enome.pack(side="left")

        #cpf
        linha_cpf = Frame(self)
        linha_cpf.pack(anchor="w", pady=5)

        Label(linha_cpf, text="CPF:", width=12, anchor="e").pack(side="left")
        self.Ecpf = Entry(linha_cpf, width=20)
        self.Ecpf.pack(side="left")

        #email
        linha_email = Frame(self)
        linha_email.pack(anchor="w", pady=5)

        Label(linha_email, text="E-mail:", width=12, anchor="e").pack(side="left")
        self.Eemail = Entry(linha_email, width=40)
        self.Eemail.pack(side="left")

        #tel
        linha_tel = Frame(self)
        linha_tel.pack(anchor="w", pady=5)

        Label(linha_tel, text="Telefone:", width=12, anchor="e").pack(side="left")
        self.Etel = Entry(linha_tel, width=20)
        self.Etel.pack(side="left")

        #botão save
        Button(self, text="Salvar", command=self.save).pack(pady=10)
        self.msg = Label(self, text="Erro: Informações insuficientes.")
        self.msg_exists = False

    def save(self):

        #recebendo informações do Entry
        self.nome = self.Enome.get()
        self.cpf = self.Ecpf.get()
        self.email = self.Eemail.get()
        self.tel = self.Etel.get()

        if (self.nome == "" or self.cpf == "" or self.email == "" or self.tel == ""):
            self.msg["text"] = "Erro: Informações insuficientes."
            if (self.msg_exists == False):
                self.msg.pack()
                self.msg_exists = True
                
        elif((not self.cpf.isdigit()) or len(self.cpf) != 11):
            self.msg["text"] = "Erro: CPF Inválido"
            self.msg["fg"] = "red"
            self.msg.pack()
            self.msg_exists = True

        elif(not self.tel.isdigit() or (len(self.tel) < 10 or len(self.tel) > 11)):
            self.msg["text"] = "Erro: Telefone inválido"
            self.msg["fg"] = "red"
            self.msg.pack()
            self.msg_exists = True

        elif "@" not in self.email or "." not in self.email.split("@")[-1]:
            self.msg["text"] = "Erro: E-mail inválido"
            self.msg["fg"] = "red"
            self.msg.pack()
            self.msg_exists = True

        else:
            try:
                h = Hospede(self.nome, self.cpf, self.email, self.tel)
                h.id = IDManager.proximo_id_hospede()
                self.dao.salvar(h)
                self.msg.config(text="Hóspede cadastrado com sucesso.", fg="black")
                self.msg.pack()
                self.after(3000, lambda: self.msg.config(text=""))
                self.msg_exists = False

                self.Enome.delete(0, END)
                self.Ecpf.delete(0, END)
                self.Eemail.delete(0, END)
                self.Etel.delete(0, END)

            except Exception as e:
                self.msg["text"] = str(e)
                self.msg["fg"] = "red"
                self.msg.pack()
                self.msg_exists = True

class FrameHEdit(Frame):
    def __init__(self, container):
        super().__init__(container)
        self.dao = DAOFactory.getHospedeDAO()
        
        linha_id = Frame(self)
        linha_id.pack(anchor="w", pady=5)

        Label(linha_id, text="ID:", width=12, anchor="e").pack(side="left")
        self.Eid = Entry(linha_id, width=10)
        self.Eid.pack(side="left")

        linha_nome = Frame(self)
        linha_nome.pack(anchor="w", pady=5)

        Label(linha_nome, text="Nome:", width=12, anchor="e").pack(side="left")
        self.Enome = Entry(linha_nome, width=40)
        self.Enome.pack(side="left")

        linha_cpf = Frame(self)
        linha_cpf.pack(anchor="w", pady=5)

        Label(linha_cpf, text="CPF:", width=12, anchor="e").pack(side="left")
        self.Ecpf = Entry(linha_cpf, width=20)
        self.Ecpf.pack(side="left")

        linha_email = Frame(self)
        linha_email.pack(anchor="w", pady=5)

        Label(linha_email, text="E-mail:", width=12, anchor="e").pack(side="left")
        self.Eemail = Entry(linha_email, width=40)
        self.Eemail.pack(side="left")

        linha_tel = Frame(self)
        linha_tel.pack(anchor="w", pady=5)

        Label(linha_tel, text="Telefone:", width=12, anchor="e").pack(side="left")
        self.Etel = Entry(linha_tel, width=20)
        self.Etel.pack(side="left")

        Button(self, text="Salvar Alterações", command=self.save).pack(pady=10)

        self.msg = Label(self)
        self.msg.pack()
        self.msg_exists = False

    def save(self):

        #recebendo informações do Entry
        self.id = self.Eid.get()
        self.nome = self.Enome.get()
        self.cpf = self.Ecpf.get()
        self.email = self.Eemail.get()
        self.tel = self.Etel.get()

        if (self.id == "" or self.nome == "" or self.cpf == "" or self.email == "" or self.tel == ""):
            self.msg["text"] = "Erro: Informações insuficientes."
            self.msg["fg"] = "red"
            self.msg.pack()
            self.msg_exists = True

        elif not self.id.isdigit():
            self.msg["text"] = "ID inválido."
            self.msg["fg"] = "red"
            self.msg.pack()
            self.msg_exists = True

        elif((not self.cpf.isdigit()) or len(self.cpf) != 11):
            self.msg["text"] = "Erro: CPF Inválido"
            self.msg["fg"] = "red"
            self.msg.pack()
            self.msg_exists = True

        elif(not self.tel.isdigit() or (len(self.tel) < 10 or len(self.tel) > 11)):
            self.msg["text"] = "Erro: Telefone inválido"
            self.msg["fg"] = "red"
            self.msg.pack()
            self.msg_exists = True

        elif "@" not in self.email or "." not in self.email.split("@")[-1]:
            self.msg["text"] = "Erro: E-mail inválido"
            self.msg["fg"] = "red"
            self.msg.pack()
            self.msg_exists = True
        else:
            try:
                h = self.dao.carregar(int(self.id))
                h.nome = self.nome
                h.cpf = self.cpf
                h.email = self.email
                h.telefone = self.tel
                
                self.dao.atualizar(h)

                self.msg.pack_forget()
                self.msg.config(text="Hóspede atualizado com sucesso.", fg="black")
                self.msg.pack()
                self.after(3000, lambda: self.msg.config(text=""))
                self.msg_exists=False

                self.Eid.delete(0,END)
                self.Enome.delete(0, END)
                self.Ecpf.delete(0, END)
                self.Eemail.delete(0, END)
                self.Etel.delete(0, END)
            except PersistenceException as e:

                self.msg["text"] = str(e)
                self.msg.pack()
                self.msg_exists = True


class FrameHRemove(Frame):
    def __init__(self, container):
        super().__init__(container)
        self.dao = DAOFactory.getHospedeDAO()

        linha_id = Frame(self)
        linha_id.pack(anchor="w", pady=5)

        Label(linha_id, text="ID:", width=12, anchor="e").pack(side="left")
        self.Eid = Entry(linha_id, width=10)
        self.Eid.pack(side="left")

        Button(self, text="Remover", command=self.remove).pack(pady=10)

        self.msg = Label(self)
        self.msg.pack()

    def remove(self):
        self.id = self.Eid.get()
        if self.id == "":
            self.msg.config(text="Informe um ID.")
        elif not self.id.isdigit():
            self.msg.config(text="Informe um ID.")
        else:
            try:
                self.dao.apagar(int(self.id))
                self.msg.config(text="Hóspede removido com sucesso.")
                self.Eid.delete(0, END)
                self.after(3000, lambda: self.msg.config(text=""))
            except PersistenceException as e:
                self.msg["text"] = str(e)
                self.msg.pack()
                self.msg_exists = True
                

class FrameHVisual(Frame):
    def __init__(self, container):
        super().__init__(container)
        self.dao = DAOFactory.getHospedeDAO()

        linha_id = Frame(self)
        linha_id.pack(anchor="w", pady=5)

        Label(linha_id, text="ID:", width=12, anchor="e").pack(side="left")
        self.Eid = Entry(linha_id, width=10)
        self.Eid.pack(side="left")

        Button(self, text="Visualizar", command=self.visualizar).pack(pady=10)

        self.msg = Label(self)
        self.msg.pack()

    def visualizar(self):
        self.id = self.Eid.get()
        if self.id == "":
            self.msg.config(text="Informe um ID.", fg="red")
        elif not self.id.isdigit():
            self.msg.config(text="Informe um ID.", fg="red")
        else:
            try:
                h = self.dao.carregar(int(self.id))
                self.msg.config(text=f"Hóspede: {h.nome} | Email: {h.email} | CPF : {h.cpf} | Telefone {h.telefone}", fg="black")
            except PersistenceException as e:
                self.msg["text"] = str(e)
                self.msg["fg"] = "red"
                self.msg.pack()
                self.msg_exists = True
              

class FrameHList(Frame):
    def __init__(self, container):
        super().__init__(container)
        self.dao = DAOFactory.getHospedeDAO()
        Button(self, text="Listar Hospedes", command=self.listar).pack(pady=10)

        self.tabela = TabelaOrdenavel(
            self,
            [
                ("id", "ID", 60, lambda hospede: hospede.id),
                ("nome", "Nome", 220, lambda hospede: hospede.nome),
                ("cpf", "CPF", 130, lambda hospede: hospede.cpf),
                ("email", "E-mail", 220, lambda hospede: hospede.email),
                ("telefone", "Telefone", 120, lambda hospede: hospede.telefone),
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

class FrameHSearch(Frame):
    def __init__(self, container):
        super().__init__(container)
        self.dao = DAOFactory.getHospedeDAO()

        frame_busca = Frame(self)
        frame_busca.pack(anchor="w", padx=20, pady=20)

        Label(frame_busca, text="Nome:", width=12, anchor="e").pack(side="left")
        self.Enome = Entry(frame_busca, width=40)
        self.Enome.pack(side="left")

        Button(frame_busca, text="Buscar", command=self.buscar).pack(side="left", padx=10)

        self.tabela = TabelaOrdenavel(
            self,
            [
                ("id", "ID", 60, lambda hospede: hospede.id),
                ("nome", "Nome", 220, lambda hospede: hospede.nome),
                ("cpf", "CPF", 130, lambda hospede: hospede.cpf),
                ("email", "E-mail", 220, lambda hospede: hospede.email),
                ("telefone", "Telefone", 120, lambda hospede: hospede.telefone),
            ]
        )
        self.tabela.pack(fill="both", expand=True, padx=10, pady=10)

    def buscar(self):
        self.tabela.limpar()
        try:
            hospedes = self.dao.carregarTodos()
            nome = self.Enome.get().lower()
            encontrados = []
            for hospede in hospedes:
                hospede_nome_lower = hospede.nome.lower()
                if hospede_nome_lower == nome:
                    encontrados.append(hospede)
                    continue

                nomecompletohospede = hospede_nome_lower.split()
                nomedabusca = nome.split()
                if any(nome_busca == nome_hospede for nome_hospede in nomecompletohospede for nome_busca in nomedabusca):
                    encontrados.append(hospede)

            if len(encontrados) == 0:
                raise ValueError

            self.tabela.carregar(encontrados)

        except PersistenceException as e:
            self.tabela.mostrar_erro(str(e))

        except Exception:
            self.tabela.mostrar_erro("Hospede nao encontrado")

    def limpar_tela(self):
        self.tabela.limpar()
