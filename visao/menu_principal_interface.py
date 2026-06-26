#from visao.menu_hospede import Menu_Hospede
#from visao.menu_quarto import Menu_Quarto
#from visao.menu_reserva import Menu_Reserva
#from visao.menu_produto import Menu_Produto
#from visao.menu_principal import Menu_Principal
from tkinter import *


class Janela:
    def __init__(self):
        #Parâmetros da janela
        self.janela = Tk()
        self.janela.geometry("800x600")
        self.janela.resizable(False, False)
        self.janela.title("Ventana - Administrador Hoteleiro v3.0")



        #menu superior
        mainmenu = Menu(self.janela, bg="green", fg="White", font=("DejaVu Sans", 12, "bold")) 
        self.janela.option_add('*tearOff', FALSE)
        self.janela.config(menu=mainmenu) 
        menu = Menu(mainmenu)
        mainmenu.add_cascade(label='Menu', menu=menu)
        menu.add_command(label='Hóspedes', command=self.Chama_Hosp)
        menu.add_command(label='Quartos', command=self.Chama_Quarto)
        menu.add_command(label='Reservas', command=self.Chama_Res)
        menu.add_command(label='Produtos', command=self.Chama_Prod)
        menu.add_command(label='Configurações', command=self.Chama_Conf)
        menu.add_command(label='Standby', command=self.Chama_Std)
        menu["bg"] = "green"
        menu["fg"] = "white"

        #menu intermediário
        self.fOptions = Frame(self.janela)
        self.fOptions.pack(fill="x")
        self.fOptions["bg"] = "#5dcf2c"

        #funcionalidades do programa
        self.fContent = Frame(self.janela)
        self.fContent.pack(fill="both", expand=True)


        self.mp = FrameStandby(self.fOptions, self.fContent)
        self.fh = FrameHospedes(self.fOptions, self.fContent)
        self.fq = FrameQuartos(self.fOptions, self.fContent)
        self.fp = FrameProdutos(self.fOptions, self.fContent)
        self.fr = FrameReservas(self.fOptions, self.fContent)
        self.fc = FrameConfiguracoes(self.fOptions, self.fContent)

        self.frames = {self.mp, self.fh, self.fq, self.fr, self.fp, self.fc}


        #por padrão, começaremos em standby
        self.Chama_Std()


    #funções para que ocorram a troca-----------------------
    def Chama_Hosp(self):
        #Fazemos um for para percorrer todos os painéis dentro da lista
        for i in self.frames:
            #pack_forget() "some" com o painel
            i.pack_forget()

        self.fh.pack()
        #tkraise faz com que ressurja o painel novamente
        self.fh.tkraise()

    def Chama_Quarto(self):
        for i in self.frames:
            i.pack_forget()

        self.fq.pack()
        self.fq.tkraise()

    def Chama_Prod(self):
        for i in self.frames:
            i.pack_forget()

        self.fp.pack()
        self.fp.tkraise()

    def Chama_Res(self):
        for i in self.frames:
            i.pack_forget()
    
        self.fr.pack()
        self.fr.tkraise()

    def Chama_Conf(self):
        for i in self.frames:
            i.pack_forget()

        self.fc.pack()
        self.fc.tkraise()

    def Chama_Std(self):
        for i in self.frames:
            i.pack_forget()
        self.mp.pack()
        self.mp.tkraise()
    #--------------------------------------------------------

#Classes e configurações de cada frame----------------------------------------
    #Frame Standby
class FrameStandby(Frame):
    def __init__(self, container, container2):
        super().__init__(container, width=400, height=600, bg="green")

        self.img = PhotoImage(file="Ventana.png")
        Label(self, image=self.img).pack()

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
        self.edit = FrameHEdit()
        self.remove = FrameHRemove()
        self.visual = FrameHVisual()
        self.list = FrameHList()
        self.search = FrameHSearch()

        self.frames = {self.cad, self.edit, self.remove, self.visual, self.list, self.search}



    def Chama_Cad(self):
        for i in self.frames:
            i.pack_forget()
            
        self.cad.pack(fill="both", expand=True)

    def Chama_HEdit(self):
        for i in self.frames:
            i.pack_forget()   

    def Chama_HRemove(self):
        for i in self.frames:
            i.pack_forget()    

    def Chama_HVisual(self):
        for i in self.frames:
            i.pack_forget()    

    def Chama_HList(self):
        for i in self.frames:
            i.pack_forget()   

    def Chama_HSearch(self):
        for i in self.frames:
            i.pack_forget()    
                
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

    def save(self):
        self.nome = self.Enome.get()
        self.cpf = self.Ecpf.get()
        self.email = self.Eemail.get()
        self.tel = self.Etel.get()
        #return Hospede(self.nome, self.cpf, self.email, self.tel)

class FrameHEdit(Frame):
    pass

class FrameHRemove(Frame):
    pass

class FrameHVisual(Frame):
    pass

class FrameHList(Frame):
    pass

class FrameHSearch(Frame):
    pass

        
    #Frames Quartos---------------------------------------------------------------                
class FrameQuartos(Frame):
    def __init__(self, container, container2):
        super().__init__(container)


        Button(self, text="Cadastrar\nQuarto", width=10, height=2).pack(side="left")
        Button(self, text="Editar\nQuarto", width=10, height=2).pack(side="left")
        Button(self, text="Remover\nQuartos", width=10, height=2).pack(side="left")
        Button(self, text="Visualizar\npor ID", width=10, height=2).pack(side="left")
        Button(self, text="Listar\nQuartos", width=10, height=2).pack(side="left")
        Button(self, text="Listar\ndisponíveis", width=10, height=2).pack(side="left")

    #Frames Produtos--------------------------------------------------------------
class FrameProdutos(Frame):
    def __init__(self, container, container2):
        super().__init__(container)


        Button(self, text="Cadastrar\nProduto", width=10, height=2).pack(side="left")
        Button(self, text="Editar\nProduto", width=10, height=2).pack(side="left")
        Button(self, text="Remover\nProdutos", width=10, height=2).pack(side="left")
        Button(self, text="Visualizar\npor ID", width=10, height=2).pack(side="left")
        Button(self, text="Listar\nProdutos", width=10, height=2).pack(side="left")

    #Frames Reservas--------------------------------------------------------------
class FrameReservas(Frame):
    def __init__(self, container, container2):
        super().__init__(container)

        Button(self, text="Nova\nReserva", width=10, height=2).pack(side="left")
        Button(self, text="Editar\nReserva", width=10, height=2).pack(side="left")
        Button(self, text="Cancelar\nReservas", width=10, height=2).pack(side="left")
        Button(self, text="Visualizar\npor ID", width=10, height=2).pack(side="left")
        Button(self, text="Listar\nReservas", width=10, height=2).pack(side="left")

    #Frames Configurações---------------------------------------------------------
class FrameConfiguracoes(Frame):
    def __init__(self, container, container2):
        super().__init__(container)

        Button(self, text="Trocar banco\nde dados", width=10, height=2).pack(side="left")



#DEBUGGING INTERFACE
bob = Janela()
bob.janela.mainloop()