from tkinter import *

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

        self.visual.pack(fill="both", expand=True)    

    def Chama_HList(self):
        for i in self.frames:
            i.pack_forget()

        self.list.pack(fill="both", expand=True)   

    def Chama_HSearch(self):
        for i in self.frames:
            i.pack_forget()

        self.search.pack(fill="both", expand=True)    
                
class FrameCad(Frame):
    def __init__(self, container2):
        super().__init__(container2)

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
            if (self.msg_exists == False):
                self.msg["text"] = "Erro: Informações insuficientes."
                self.msg.pack()
                self.msg_exists = True


        else:
            self.msg.pack_forget()
            self.msg = Label(self, text="Hóspede cadastrado com sucesso.")
            self.msg.pack()
            self.after(3000, lambda: self.msg.config(text=""))
            self.msg_exists=False
            
            self.Enome.delete(0, END)
            self.Ecpf.delete(0, END)
            self.Eemail.delete(0, END)
            self.Etel.delete(0, END)
        #deve-se colocar Hospede(self.nome, self.cpf, self.email, self.tel) no banco de dados

class FrameHEdit(Frame):
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
            if (self.msg_exists == False):
                self.msg["text"] = "Erro: Informações insuficientes."
                self.msg.pack()
                self.msg_exists = True
        else:
            self.msg.pack_forget()
            self.msg.config(text="Hóspede atualizado com sucesso.")
            self.msg.pack()
            self.after(3000, lambda: self.msg.config(text=""))
            self.msg_exists=False


            self.Eid.delete(0,END)
            self.Enome.delete(0, END)
            self.Ecpf.delete(0, END)
            self.Eemail.delete(0, END)
            self.Etel.delete(0, END)

class FrameHRemove(Frame):
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
            self.msg.config(text="Hóspede removido com sucesso.")
            self.Eid.delete(0, END)

        self.after(3000, lambda: self.msg.config(text=""))

class FrameHVisual(Frame):
    def __init__(self, container):
        super().__init__(container)

        linha_id = Frame(self)
        linha_id.pack(anchor="w", pady=5)

        Label(linha_id, text="ID:", width=12, anchor="e").pack(side="left")
        self.Eid = Entry(linha_id, width=10)
        self.Eid.pack(side="left")

        Button(self, text="Visualizar", command=self.visualizar).pack(pady=10)

        self.resultado = Label(self, justify="left")
        self.resultado.pack(anchor="w", padx=20)

    def visualizar(self):
        #colocar método para visualizar hóspede por id
        pass            

class FrameHList(Frame):
    def __init__(self, container):
        super().__init__(container)

        Button(self, text="Listar Hóspedes", command=self.listar).pack(pady=10)

        self.lista = Listbox(self, width=60, height=15)
        self.lista.pack()

    def listar(self):
        pass
        #colocar método para listar todos os hóspedes disponíveis no banco de dados

class FrameHSearch(Frame):
    def __init__(self, container):
        super().__init__(container)

        linha_nome = Frame(self)
        linha_nome.pack(anchor="w", pady=5)

        Label(linha_nome, text="Nome:", width=12, anchor="e").pack(side="left")
        self.Enome = Entry(linha_nome, width=40)
        self.Enome.pack(side="left")

        Button(self, text="Buscar", command=self.buscar).pack(pady=10)

        self.lista = Listbox(self, width=60, height=10)
        self.lista.pack()

    def buscar(self):
        #colocar método para buscar por nome
        pass