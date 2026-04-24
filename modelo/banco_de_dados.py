class Bancodedados:
    _hospedes_ = []             #as variaveis vao ficar aqui mesmo, nao vamos declarar o banco de dados com um objeto, vamos apenas usar a classe.
    _quartos_ = []
    _reservas_ = []             #o banco de dados vao ser listas por enquanto, so vai salvar na memoria ram mesmo"

    proximoidhospede = 1
    proximoidquarto = 1                          #IDs pra salvar os objetos nas listas, com um ID
    proximoidreserva = 1

#MÉTODOS DO HÓSPEDE------------------------------------------------------

    @classmethod
    def atualiza_hospede(cls, hospede):
        ########                                     #vazio, porque como estamos lidando com listas, tudo vai atualizar na memoria ram                             
                                                    #mas vou deixar aq pra quando formos usar sqlite, colocarmos a logica aqui.
                                                    #EDIT 1: GUILHERME - fiz um edit_Hospede que atua como atualiza hóspede, mas tá acoplado com
                                                    #uma interface. Como não sei como funciona o sqlite, eu deixei assim pra começarmos a usar o programa
        return                                      


    @classmethod
    def salva_hospede(cls, hospede):             #OBS: o cls, serve pra alterar variaveis ou usar metodos da classe, independendo do objeto
                                                            #assim, nosso banco de dados é uma coisa só
        if(hospede.id is None):
            hospede.id = cls.proximoidhospede           #salva o hospede na lista de hospedes com um id
            cls.proximoidhospede += 1               
            cls._hospedes_.append(hospede)
        else:
            cls.atualiza_hospede(hospede)       #se o ID ja existir, ele vai atualizar.
    
    @classmethod
    def apaga_hospede(cls, hospede):
        if(hospede in cls._hospedes_):
            cls._hospedes_.remove(hospede)      #apaga o hospede da lista
            return True
        else:
            #########               #se o hospede nao existir a gente deve mostrar alguma mensagem talvez
            return False
        
    @classmethod
    def busca_hospede(cls, id):
        for hospede in cls._hospedes_:
            if id == hospede.id:
                return hospede
        return None
    
    @classmethod
    def lista_hospedes(cls):
        return cls._hospedes_
    
#MÉTODOS DO QUARTO---------------------------------------------------------    
    
    @classmethod
    def atualiza_quarto(cls, quarto):      
        #####                                   
        return
    
    @classmethod

    def salva_quarto(cls, quarto):
        if(quarto.id == None):
            quarto.id = cls.proximoidquarto     
            cls.proximoidquarto += 1
            cls._quartos_.append(quarto)
        else:
            cls.atualiza_quarto(quarto)


    @classmethod
    def apaga_quarto(cls, quarto):
        if(quarto in cls._quartos_):
            cls._quartos_.remove(quarto)
        else:
            ########
            return
  