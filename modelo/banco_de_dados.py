class Bancodedados:
    _hospedes_ = []             #"o banco de dados vao ser listas por enquanto, so vai salvar na memoria ram mesmo"
    _quartos_ = []
    _reservas_ = []

    proximoidhospede = 1
    proximoidquarto = 1
    proximoidreserva = 1
    
    @classmethod
    def atualiza_hospede(cls, hospede):
        ########
        return

    @classmethod
    def salva_hospede(cls, hospede):
        if(hospede.id == None):
            hospede.id = cls.proximoidhospede
            cls.proximoidhospede += 1
            cls._hospedes_.append(hospede)
        else:
            cls.atualiza_hospede(hospede)
    
    @classmethod
    def apaga_hospede(cls, hospede):
        if(hospede in cls._hospedes_):
            cls._hospedes_.remove(hospede)
        else:
            #########
            return
        
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