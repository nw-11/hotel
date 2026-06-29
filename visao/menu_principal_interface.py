#from visao.menu_hospede import Menu_Hospede
#from visao.menu_quarto import Menu_Quarto
#from visao.menu_reserva import Menu_Reserva
#from visao.menu_produto import Menu_Produto
#from visao.menu_principal import Menu_Principal
from tkinter import *
import os
from visao.menu_hospede_interface import *
from visao.menu_quarto_interface import *
from visao.menu_produto_interface import *
from visao.menu_reserva_interface import *

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

        self.frames = {self.mp, self.fh, self.fq, self.fr, self.fp}


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

        for i in self.fq.frames:
            i.pack_forget()
        for i in self.fp.frames:
            i.pack_forget()
        for i in self.fr.frames:
            i.pack_forget()

    def Chama_Quarto(self):
        for i in self.frames:
            i.pack_forget() 

        self.fq.pack()
        self.fq.tkraise()

        for i in self.fh.frames:
            i.pack_forget()
        for i in self.fp.frames:
            i.pack_forget()
        for i in self.fr.frames:
            i.pack_forget()

    def Chama_Prod(self):
        for i in self.frames:
            i.pack_forget()

        self.fp.pack()
        self.fp.tkraise()

        for i in self.fh.frames:
            i.pack_forget()
        for i in self.fq.frames:
            i.pack_forget()
        for i in self.fr.frames:
            i.pack_forget()

    def Chama_Res(self):
        for i in self.frames:
            i.pack_forget()
    
        self.fr.pack()
        self.fr.tkraise()

        for i in self.fh.frames:
            i.pack_forget()
        for i in self.fq.frames:
            i.pack_forget()
        for i in self.fp.frames:
            i.pack_forget()

    def Chama_Std(self):
        for i in self.frames:
            i.pack_forget()
        self.mp.pack()
        self.mp.tkraise()

        for i in self.fh.frames:
            i.pack_forget()
        for i in self.fq.frames:
            i.pack_forget()
        for i in self.fp.frames:
            i.pack_forget()
        for i in self.fr.frames:
            i.pack_forget()
    #--------------------------------------------------------

#Classes e configurações de cada frame----------------------------------------
    #Frame Standby
class FrameStandby(Frame):
    def __init__(self, container, container2):
        super().__init__(container, width=400, height=600, bg="green")

        diretorio_atual = os.path.dirname(__file__)
        caminho_imagem = os.path.join(diretorio_atual, "Ventana.png")
        self.img = PhotoImage(file=caminho_imagem)
        Label(self, image=self.img).pack()


